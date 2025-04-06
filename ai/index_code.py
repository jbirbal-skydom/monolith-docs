import os
import time
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm import tqdm
from pathlib import Path

# Configuration
repo_path = "../monolith"
model_name = "llama2:70b"

def is_binary_file(file_path):
    """Check if a file is binary by reading its first few thousand bytes"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(4000)
            return b'\0' in chunk  # Binary files typically contain null bytes
    except:
        return True

def categorize_file(file_path):
    """Categorize the file based on its path and extension"""
    path = file_path.lower()
    
    # Determine file type
    if path.endswith('.rs'):
        file_type = 'rust'
    elif path.endswith('.toml'):
        file_type = 'toml'
    elif path.endswith('.md'):
        file_type = 'markdown'
    elif path.endswith('.udl'):
        file_type = 'udl'
    elif path.endswith('.xlsx'):
        file_type = 'excel'
    else:
        file_type = 'other'
    
    # Determine file category
    if 'readme' in os.path.basename(path).lower():
        category = 'readme'
    elif 'changelog' in os.path.basename(path).lower():
        category = 'changelog'
    elif path.endswith('/src/lib.rs') or path.endswith('/src/main.rs'):
        category = 'core'
    elif '/src/' in path:
        category = 'source'
    elif '/tests/' in path:
        category = 'test'
    elif '/examples/' in path:
        category = 'example'
    else:
        category = 'other'
    
    # Try to extract crate name if it's a monolith component
    crate_name = None
    parts = Path(path).parts
    for i, part in enumerate(parts):
        if 'monolith-' in part.lower():
            crate_name = part
            break
    
    return {
        'file_type': file_type,
        'category': category,
        'crate_name': crate_name
    }

def load_files_from_repo(repo_path):
    """Load all relevant code files from the repository"""
    code_files = []
    skipped_files = []
    binary_files = []
    
    # File extensions to include
    extensions = ('.rs')
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            full_path = os.path.join(root, file)
            
            # Check if file is relevant for indexing
            if file.endswith(extensions):
                # Skip binary files
                if is_binary_file(full_path):
                    binary_files.append(full_path)
                    continue
                    
                # Add file to the list
                code_files.append(full_path)
            else:
                skipped_files.append(full_path)
    
    # Print summary
    print(f"Found {len(code_files)} files to index.")
    print(f"Skipped {len(skipped_files)} non-code files.")
    print(f"Skipped {len(binary_files)} binary files.")
    
    return code_files

def index_files(files):
    """Index files into Qdrant database"""
    # Initialize text splitter - different settings for different file types
    default_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    code_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Smaller chunks for code files
        chunk_overlap=150,
        separators=["\nfn ", "\nimpl ", "\nstruct ", "\nenum ", "\ntrait ", "\n\n", "\n", " ", ""]
    )
    
    # Initialize embedding model
    embedding_model = OllamaEmbeddings(model=model_name)
    
    # Initialize Qdrant client
    client = QdrantClient(url="http://localhost:6333")
    
    # Delete collection if it exists
    try:
        client.delete_collection("monolith")
        print("Deleted existing collection 'monolith'")
        time.sleep(1)
    except Exception as e:
        print(f"Collection may not exist yet: {e}")
    
    # Create a new collection
    dimension = len(embedding_model.embed_query("test"))
    client.create_collection(
        collection_name="monolith",
        vectors_config=models.VectorParams(
            size=dimension,
            distance=models.Distance.COSINE
        )
    )
    print("Created new collection 'monolith'")
    
    # Process files and collect chunks
    all_texts = []
    all_metadatas = []
    file_counts = {'rust': 0, 'toml': 0, 'markdown': 0, 'udl': 0, 'excel': 0, 'other': 0}
    chunk_counts = {'rust': 0, 'toml': 0, 'markdown': 0, 'udl': 0, 'excel': 0, 'other': 0}
    
    for file in tqdm(files, desc="Reading files"):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Categorize file and select appropriate splitter
                file_info = categorize_file(file)
                file_counts[file_info['file_type']] += 1
                
                # Choose splitter based on file type
                splitter = code_splitter if file_info['file_type'] == 'rust' else default_splitter
                chunks = splitter.split_text(content)
                
                # Update chunk count
                chunk_counts[file_info['file_type']] += len(chunks)
                
                # Add file metadata to each chunk
                for i, chunk in enumerate(chunks):
                    metadata = {
                        "source": file,
                        "chunk": i,
                        "file_type": file_info['file_type'],
                        "category": file_info['category'],
                        "crate_name": file_info['crate_name']
                    }
                    
                    all_texts.append(chunk)
                    all_metadatas.append(metadata)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    print(f"Loaded {len(all_texts)} chunks from {len(files)} files")
    print(f"File counts by type: {file_counts}")
    print(f"Chunk counts by type: {chunk_counts}")
    
    # Process in batches
    batch_size = 50  # Reduced batch size for larger models
    total_batches = (len(all_texts) + batch_size - 1) // batch_size
    
    for i in tqdm(range(0, len(all_texts), batch_size), desc="Indexing", total=total_batches):
        batch_texts = all_texts[i:i+batch_size]
        batch_metadatas = all_metadatas[i:i+batch_size]
        
        # Generate embeddings (with error handling)
        embeddings = []
        for text in batch_texts:
            try:
                embedding = embedding_model.embed_query(text)
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error embedding text: {e}")
                # Use a zero vector as a fallback (careful with this)
                embeddings.append(np.zeros(dimension))
        
        # Create points for Qdrant
        points = []
        for j, (embedding, text, metadata) in enumerate(zip(embeddings, batch_texts, batch_metadatas)):
            point_id = i + j
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={"text": text, **metadata}
                )
            )
        
        # Upload points to Qdrant
        if points:
            client.upsert(
                collection_name="monolith",
                points=points
            )
    
    # Create a payload index for faster filtering
    client.create_payload_index(
        collection_name="monolith",
        field_name="file_type",
        field_schema=models.PayloadSchemaType.KEYWORD
    )
    
    client.create_payload_index(
        collection_name="monolith",
        field_name="category",
        field_schema=models.PayloadSchemaType.KEYWORD
    )
    
    client.create_payload_index(
        collection_name="monolith",
        field_name="crate_name",
        field_schema=models.PayloadSchemaType.KEYWORD
    )
    
    print(f"✅ Indexing complete. Added {len(all_texts)} chunks to Qdrant with enhanced metadata.")

if __name__ == "__main__":
    files = load_files_from_repo(repo_path)
    index_files(files)