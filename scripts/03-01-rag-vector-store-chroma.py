
# imports
import os
from pathlib import Path
import pickle

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
# Also suppress LangChain warnings
from langchain._api import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)




 
 # Load the processed chunks from previous step
def load_chunks(chunks_file):
    """Load the processed document chunks"""
    if chunks_file.exists():
        print(f"Loading chunks from {chunks_file}")
        with open(chunks_file, "rb") as f:
            chunks = pickle.load(f)
        print(f"Loaded {len(chunks)} chunks")
        return chunks
    else:
        print(f"Chunks file not found at {chunks_file}")
        print("Please run 02-01-rag-langchain-textSplitChunkOptimization.py first")
        return None

# Initialize embeddings
def setup_embeddings():
    """Setup embedding model"""
    # Option 1: OpenAI (requires API key)
    # Make sure you have OPENAI_API_KEY in your environment
    try:
        embeddings = OpenAIEmbeddings()
        print("Using OpenAI embeddings")
        return embeddings
    except Exception as e:
        print(f"OpenAI embeddings failed: {e}")
        
    return embeddings
    

# Create vector store
def create_vector_store(chunks, embeddings, persist_dir):
    """Create and populate Chroma vector store"""
    
    # Delete existing directory to avoid duplicates
    if persist_dir.exists():
        import shutil
        print(f"Deleting existing vector store at {persist_dir}")
        shutil.rmtree(persist_dir)
    
    # Create fresh directory
    persist_dir.mkdir(parents=True, exist_ok=True)
    print(f"Creating fresh vector store in {persist_dir}")
   
    
    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_dir),
        collection_name="azure_docs"
    )
    
    print(f"Vector store created with {vectorstore._collection.count()} documents")
    return vectorstore

def test_search(vectorstore):
    """Test the vector store with some queries"""
    
    test_queries = [
        "What is Azure Load Balancer backend pool?",
        "How to configure network security groups?",
        "Azure Virtual Network peering setup",
        "DNS configuration in Azure"
    ]
    
    print("\n" + "="*60)
    print("TESTING SEMANTIC SEARCH")
    print("="*60)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        
        # Perform similarity search
        results = vectorstore.similarity_search(query, k=3)
        
        for i, doc in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Doc Type: {doc.metadata.get('doc_type', 'Unknown')}")
            print(f"Source: {doc.metadata.get('source', 'Unknown').split('/')[-1]}")
            print(f"Content: {doc.page_content[:600]}...")
            print("-" * 30)


# Main function
def main():
    print("Setting up Chroma Vector Database for Azure RAG")
    print("="*50)
    
    # Define paths
    chunks_file = Path(__file__).parent.parent / "data" / "processed" / "documents_chunks.pkl"
    persist_dir = Path(__file__).parent.parent / "data" / "vector_store" / "chroma_db"
    
    # Step 1: Load chunks
    chunks = load_chunks(chunks_file)
    if chunks is None:
        return
    
    # Step 2: Setup embeddings
    embeddings = setup_embeddings()
    
    # Step 3: Create vector store
    vectorstore = create_vector_store(chunks, embeddings, persist_dir)
    
    # Step 4: Test search functionality
    test_search(vectorstore)
    
    print("\n" + "="*50)
    print("Vector store setup complete!")
    print(f"You can now use semantic search on {len(chunks)} chunks")
    print("="*50)

if __name__ == "__main__":
    main()

