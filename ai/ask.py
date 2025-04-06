import sys
import os
import re
from pathlib import Path
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.prompts import PromptTemplate

def ask(query, conversation_history=None, focus_on_code=True, file_filter=None):
    """
    Ask a question about the codebase, maintaining conversation history
    
    Args:
        query: The question to ask
        conversation_history: Previous conversation history
        focus_on_code: If True, prioritize code files over README/docs
        file_filter: Optional regex pattern to filter source files
    """
    model_name = "llama2:70b"

    # Initialize the embedding model
    embedding_model = OllamaEmbeddings(model=model_name)
    
    # Create a Qdrant client
    client = QdrantClient(url="http://localhost:6333")
    
    # If no conversation history provided, try to load from file
    if conversation_history is None:
        history_file = "conversation_history.txt"
        conversation_history = []
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                lines = f.readlines()
                for i in range(0, len(lines), 2):
                    if i+1 < len(lines):
                        human = lines[i].strip()
                        ai = lines[i+1].strip()
                        if human.startswith("Human: "):
                            human = human[7:]
                        if ai.startswith("AI: "):
                            ai = ai[4:]
                        conversation_history.append({"human": human, "ai": ai})
    
    # Analyze the query to determine if it's about specific files or functions
    code_focus = focus_on_code or is_code_specific_query(query)
    file_pattern = extract_file_pattern(query) or file_filter
    
    # Generate an embedding for the query
    query_embedding = embedding_model.embed_query(query)
    
    # Search for similar vectors in Qdrant
    search_results = client.search(
        collection_name="monolith",
        query_vector=query_embedding,
        limit=50  # Retrieve more results initially for filtering
    )
    
    # Apply filters based on query analysis
    if code_focus:
        # Prioritize actual code files over READMEs and docs
        search_results = prioritize_code_files(search_results)
    
    if file_pattern:
        # Filter results to match specific file pattern
        search_results = filter_by_file_pattern(search_results, file_pattern)
    
    # Limit to top 15 results after filtering
    search_results = search_results[:15]
    
    # Extract the text and metadata from the search results
    context_chunks = []
    files_included = set()
    
    for result in search_results:
        text = result.payload.get("text", "")
        source = result.payload.get("source", "Unknown")
        chunk_num = result.payload.get("chunk", 0)
        score = result.score
        
        # Track which files we're including
        files_included.add(source)
        
        # Format source path for better readability
        source_display = format_source_path(source)
        
        context_chunks.append(f"[Source: {source_display}, Chunk: {chunk_num}, Score: {score:.2f}]\n{text}\n")
    
    # Join the context chunks
    context = "\n".join(context_chunks)
    
    # Print a summary of the files included in the context
    print(f"\n🔍 Including content from {len(files_included)} files:")
    for file in sorted(files_included):
        print(f"  - {format_source_path(file)}")
    
    # Create a template that includes conversation history and code context
    template = """You are a code analysis assistant with deep expertise in Rust programming. You are examining code from the Monolith project.

IMPORTANT INSTRUCTIONS:
1. ONLY analyze code that is explicitly present in the context below.
2. DO NOT invent, assume, or make up ANY code or functionality that is not explicitly shown.
3. When asked about specific functions, methods, or code patterns, FIRST check if they appear in the context.
4. If relevant code is not in the context, clearly state: "I cannot find the implementation of [specific code] in the retrieved context."
5. STOP yourself from making general statements about the project's structure when the context doesn't support it.

Previous conversation:
{chat_history}

Below is the EXACT code context retrieved from the codebase:

{context}

When examining this code:
- Focus on analyzing the ACTUAL CODE in the context, not just READMEs or documentation.
- Quote specific code snippets to support your explanations.
- If asked about "self.data_processor.process_data()" or similar patterns, ONLY discuss them if they appear verbatim in the context.
- First state which files contain relevant code for the question, if any.
- If the code shows TODOs, placeholders, or incomplete implementations, point this out specifically.

Answer the following question by analyzing ONLY the provided code context:
Question: {question}
"""
    
    # Format chat history for inclusion in the prompt
    chat_history_text = ""
    for exchange in conversation_history:
        chat_history_text += f"Human: {exchange['human']}\nAI: {exchange['ai']}\n\n"
    
    # Create the prompt template
    PROMPT = PromptTemplate(
        template=template,
        input_variables=["context", "question", "chat_history"]
    )
    
    # Format the prompt with the context, query, and chat history
    formatted_prompt = PROMPT.format(
        context=context,
        question=query,
        chat_history=chat_history_text
    )
    
    # Create the LLM
    llm = OllamaLLM(
        model=model_name,
        temperature=0.1,  # Lower temperature for more factual responses
        top_p=0.95,       # Slight adjustment
        max_tokens=4096,  # Keep this the same
        num_ctx=8192,     # Keep this the same
        repeat_penalty=1.2,  # Add a repeat penalty to reduce repetition
        presence_penalty=0.5,  # Encourage new content
    )
    
    # Get the answer from the LLM
    response = llm.invoke(formatted_prompt)
    
    # Update conversation history
    conversation_history.append({"human": query, "ai": response})
    
    # Save updated conversation history
    with open("conversation_history.txt", "w") as f:
        for exchange in conversation_history:
            f.write(f"Human: {exchange['human']}\n")
            f.write(f"AI: {exchange['ai']}\n")
    
    print("\n✅ Answer:\n")
    print(response)
    
    return conversation_history

def is_code_specific_query(query):
    """Determine if the query is specifically about code implementation"""
    code_indicators = [
        r'\b\w+::\w+\b',          # Pattern like module::function
        r'\bfunction\b',           # Explicit mention of function
        r'\bmethod\b',             # Explicit mention of method
        r'\bclass\b',              # Explicit mention of class
        r'\bstruct\b',             # Explicit mention of struct
        r'\bimplementation\b',     # Explicit mention of implementation
        r'\bcode\b',               # Explicit mention of code
        r'\bimpl\b',               # Rust implementation blocks
        r'\bfn\b',                 # Rust function definition
        r'\blib.rs\b',             # Rust library file
        r'\bmain.rs\b',            # Rust main file
        r'\.\w+\(',                # Method call
        r'\w+\.\w+\.\w+',          # Nested attribute access
    ]
    
    for pattern in code_indicators:
        if re.search(pattern, query, re.IGNORECASE):
            return True
            
    return False

def extract_file_pattern(query):
    """Extract file pattern if the query is about specific files"""
    # Look for explicit file mentions
    file_patterns = [
        r'in\s+(\w+[-\w]*\.rs)',            # "in some_file.rs"
        r'the\s+(\w+[-\w]*\.rs)',           # "the some_file.rs"
        r'file\s+(\w+[-\w]*\.rs)',          # "file some_file.rs"
        r'(\w+[-\w]*\.rs)\s+file',          # "some_file.rs file"
        r'(\w+[-\w/]*\.rs)',                # any .rs file mention
        r'(\w+[-_]\w+)(?:\s+crate|\s+module)', # "some_name crate/module"
        r'monolith-(\w+)',                  # monolith-component
    ]
    
    for pattern in file_patterns:
        matches = re.search(pattern, query, re.IGNORECASE)
        if matches:
            file_hint = matches.group(1)
            # Convert to regex pattern for flexible matching
            if file_hint.endswith('.rs'):
                return f".*{re.escape(file_hint)}$"
            else:
                return f".*{re.escape(file_hint)}.*"
    
    return None

def prioritize_code_files(search_results):
    """Prioritize actual code files over READMEs and documentation"""
    # Define file priority (lower is better)
    def get_file_priority(filepath):
        path = filepath.lower()
        if path.endswith('.rs'):
            # Prioritize source files
            return 0
        elif path.endswith('.toml'):
            # Config files
            return 1
        elif 'readme' in path.lower() or 'changelog' in path.lower():
            # Documentation files - lower priority
            return 3
        else:
            # Other files
            return 2
    
    # Sort results by file priority, then by score
    sorted_results = sorted(
        search_results,
        key=lambda r: (
            get_file_priority(r.payload.get("source", "")),
            -r.score  # Negative score for descending sort
        )
    )
    
    return sorted_results

def filter_by_file_pattern(search_results, pattern):
    """Filter search results to only include files matching the pattern"""
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        return [r for r in search_results if regex.search(r.payload.get("source", ""))]
    except re.error:
        # If regex is invalid, return all results
        print(f"Warning: Invalid file pattern '{pattern}'. Ignoring filter.")
        return search_results

def format_source_path(path):
    """Format source path for better readability"""
    try:
        # Convert to Path object for easier manipulation
        p = Path(path)
        
        # Check if path contains 'monolith' to extract the crate name
        parts = p.parts
        for i, part in enumerate(parts):
            if 'monolith' in part:
                # Return crate name + file path
                crate = part
                rel_path = '/'.join(parts[i+1:])
                return f"{crate}/{rel_path}"
        
        # If no monolith part found, return the filename
        return p.name
    except:
        return path

def parse_args():
    """Parse command line arguments"""
    import argparse
    parser = argparse.ArgumentParser(description="Code-aware AI assistant for the Monolith project")
    parser.add_argument("query", nargs="*", help="Question to ask")
    parser.add_argument("--docs", action="store_true", help="Include documentation (READMEs) in search results")
    parser.add_argument("--file", type=str, help="Focus on specific file pattern", default=None)
    return parser.parse_args()

def interactive_mode(focus_on_code=True, file_filter=None):
    """
    Run in interactive mode, maintaining conversation history
    """
    conversation_history = []
    print("🤖 Code Assistant - Interactive Mode")
    print("Type 'exit', 'quit', or 'q' to end the conversation")
    
    # Print current settings
    settings_msg = []
    if focus_on_code:
        settings_msg.append("Prioritizing code files")
    else:
        settings_msg.append("Including documentation files")
    
    if file_filter:
        settings_msg.append(f"Focusing on files matching: {file_filter}")
    
    if settings_msg:
        print("Settings: " + ", ".join(settings_msg))
    
    print("\nSpecial commands:")
    print("  !code - Toggle code-focus mode")
    print("  !file <pattern> - Set file filter")
    print("  !clear - Clear file filter")
    
    while True:
        query = input("\n💬 Question: ")
        
        # Check for special commands
        if query.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        elif query.lower() == "!code":
            focus_on_code = not focus_on_code
            print(f"{'Prioritizing code files' if focus_on_code else 'Including documentation files'}")
            continue
        elif query.lower().startswith("!file "):
            file_filter = query[6:].strip()
            print(f"Set file filter to: {file_filter}")
            continue
        elif query.lower() == "!clear":
            file_filter = None
            print("Cleared file filter")
            continue
        
        conversation_history = ask(query, conversation_history, focus_on_code, file_filter)

if __name__ == "__main__":
    args = parse_args()
    
    if args.query:
        # Command-line mode
        query = " ".join(args.query)
        ask(query, focus_on_code=not args.docs, file_filter=args.file)
    else:
        # No arguments, enter interactive mode
        interactive_mode(focus_on_code=True)