import sys
import os
import re
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

def ask(query, conversation_history=None, codebase_dir="/root/monolith"):
    """
    Ask a question about the Monolith codebase, with all Rust files loaded directly in memory
    
    Args:
        query: The question to ask
        conversation_history: Previous conversation history
        codebase_dir: Directory containing the codebase (default: /root/monolith)
    """
    model_name = "mixtral"  # 32K context window
    
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
    
    # Load all Rust files from the codebase directory
    file_contents = {}
    
    # Walk through the directory and read all Rust files
    for root, dirs, files in os.walk(codebase_dir):
        # Skip hidden directories and common directories to ignore
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['target', 'node_modules']]
        
        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
                
            # Focus on Rust files only
            if not file.endswith('.rs'):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, codebase_dir)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents[rel_path] = content
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    # Format file contents for context
    context_chunks = []
    
    for file_path, content in file_contents.items():
        # Format path for better readability
        context_chunks.append(f"\n[File: {file_path}]\n{content}")
    
    # Join all file contents
    context = "\n".join(context_chunks)
    
    # Print summary of files included
    print(f"\n🔍 Loaded {len(file_contents)} Rust files from {codebase_dir}:")
    for file_path in sorted(file_contents.keys()):
        print(f"  - {file_path}")
    
    # Create a template that includes conversation history and code context
    template = """You are a code analysis assistant with deep expertise in Rust programming. You are examining code from the Monolith project.

IMPORTANT INSTRUCTIONS:
1. You have access to ALL Rust (.rs) files in the Monolith project codebase.
2. Analyze the Rust code to provide comprehensive answers about the project.
3. When asked about specific functions, methods, or code patterns, check across ALL provided files.
4. If relevant code is not in the context, clearly state: "I cannot find the implementation of [specific code] in the provided files."
5. When discussing the project structure, you can reference any of the files provided in the context.

Previous conversation:
{chat_history}

Below is the EXACT code context from the entire Monolith codebase:

{context}

When examining this code:
- You have access to the entire Rust codebase, so feel free to reference any file or function present in the context.
- Quote specific code snippets to support your explanations.
- When asked about specific functions or patterns, search across all files to find references.
- Provide a comprehensive answer that considers all relevant files in the codebase.
- If the code shows TODOs, placeholders, or incomplete implementations, point this out specifically.

Answer the following question about the Monolith project:
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
        num_ctx=32768,    # Set context window to 32K for mixtral
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

def interactive_mode(codebase_dir="/root/monolith"):
    """
    Run in interactive mode, maintaining conversation history
    """
    conversation_history = []
    print("🤖 Monolith Code Assistant - Interactive Mode")
    print("Type 'exit', 'quit', or 'q' to end the conversation")
    
    # Print current settings
    print(f"Settings: Loading ALL Rust (.rs) files from {codebase_dir}")
    
    while True:
        query = input("\n💬 Question: ")
        
        # Check for special commands
        if query.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        
        conversation_history = ask(query, conversation_history, codebase_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Code-aware AI assistant for the Monolith project")
    parser.add_argument("query", nargs="*", help="Question to ask (if not provided, enters interactive mode)")
    parser.add_argument("--dir", type=str, help="Directory containing the Monolith codebase", default="/root/monolith")
    args = parser.parse_args()
    
    if args.query:
        # Command-line mode
        query = " ".join(args.query)
        ask(query, codebase_dir=args.dir)
    else:
        # No arguments, enter interactive mode
        interactive_mode(codebase_dir=args.dir)