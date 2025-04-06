import os
import time
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
from tqdm import tqdm

repo_path = "../monolith"
model_name = "llama2:70b"


def load_files_from_repo(repo_path):
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.rs', '.toml', '.md', '.udl', '.xlsx')):
                code_files.append(os.path.join(root, file))
    return code_files

def index_files(files):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    embedding_model = OllamaEmbeddings(model=model_name)
    client = QdrantClient(url="http://localhost:6333")

    try:
        client.delete_collection("monolith")
        print("Deleted existing collection 'monolith'")
        time.sleep(1)
    except Exception as e:
        print(f"Collection may not exist yet: {e}")

    dimension = len(embedding_model.embed_query("test"))
    client.create_collection(
        collection_name="monolith",
        vectors_config=models.VectorParams(
            size=dimension,
            distance=models.Distance.COSINE
        )
    )
    print("Created new collection 'monolith'")

    all_texts, all_metadatas = [], []

    for file in tqdm(files, desc="Reading files"):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                chunks = splitter.split_text(content)

                for i, chunk in enumerate(chunks):
                    all_texts.append(chunk)
                    all_metadatas.append({"source": file, "chunk": i})
        except Exception as e:
            print(f"Error reading {file}: {e}")

    batch_size = 100
    for i in tqdm(range(0, len(all_texts), batch_size), desc="Indexing"):
        batch_texts = all_texts[i:i+batch_size]
        batch_metadatas = all_metadatas[i:i+batch_size]

        embeddings = [embedding_model.embed_query(text) for text in batch_texts]

        points = [
            models.PointStruct(
                id=i+j,
                vector=embedding,
                payload={"text": text, **metadata}
            ) for j, (embedding, text, metadata) in enumerate(zip(embeddings, batch_texts, batch_metadatas))
        ]

        client.upsert(collection_name="monolith", points=points)

    print(f"✅ Indexing complete. Added {len(all_texts)} chunks to Qdrant.")

if __name__ == "__main__":
    files = load_files_from_repo(repo_path)
    print(f"Found {len(files)} files to index.")
    index_files(files)
