import sys
import os
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def ask(query, conversation_history=None):
    """
    Ask a question about the codebase, maintaining conversation history
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
    
    # Generate an embedding for the query
    query_embedding = embedding_model.embed_query(query)
    
    # Search for similar vectors in Qdrant
    search_results = client.search(
        collection_name="monolith",
        query_vector=query_embedding,
        limit=15  # Adjust as needed
    )
    
    # Extract the text and metadata from the search results
    context_chunks = []
    for result in search_results:
        text = result.payload.get("text", "")
        source = result.payload.get("source", "Unknown")
        chunk_num = result.payload.get("chunk", 0)
        score = result.score
        
        context_chunks.append(f"[Source: {source}, Chunk: {chunk_num}, Score: {score:.2f}]\n{text}\n")
    
    # Join the context chunks
    context = "\n".join(context_chunks)
    
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

def interactive_mode():
    """
    Run in interactive mode, maintaining conversation history
    """
    conversation_history = []
    print("🤖 Code Assistant - Interactive Mode")
    print("Type 'exit', 'quit', or 'q' to end the conversation")
    
    while True:
        query = input("\n💬 Question: ")
        if query.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        
        conversation_history = ask(query, conversation_history)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command-line mode
        query = " ".join(sys.argv[1:])
        ask(query)
    else:
        # No arguments, enter interactive mode
        interactive_mode()
