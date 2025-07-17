
# imports
import os
import glob
import pickle
from pathlib import Path


# import or LangChain
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# vector store
db_name = "vector_db"


# read all text files from the directory and subdirectories using LangChain DirectoryLoader
from pathlib import Path

# Get the current file's directory, go up one level, then to data/raw/markdown
base_path = Path(__file__).parent.parent / "data" / "raw" / "markdown"
folders_path = [d for d in os.listdir(base_path) 
                 if os.path.isdir(os.path.join(base_path, d)) and not d.startswith('.')]
documents_list = []
for folder in folders_path:
    doc_type = os.path.basename(folder)
    #print(f"Processing folder: {doc_type}")
    
    loader = DirectoryLoader(base_path / folder, glob="**/*.md", loader_cls=TextLoader)
    folder_docs = loader.load()
    #print(f"Loaded {len(folder_docs)} documents from {doc_type}")
    
    for doc in folder_docs:
        #print(f"{doc}")
        doc.metadata['doc_type'] = doc_type # Adding additional doc_type to metadata
        documents_list.append(doc)
        #print(f"Document metadata:{doc.metadata} \n\n\n-------\\n")
    
# check | output looks good
# for document in documents_list[:10]:
#     print(f"{document}")
#     pass
# print(f"\n\nTotal documents loaded: {len(documents_list)}")
# print(f"Type of first document: {type(documents_list[0])}")
# print(f"Instance attributes: {documents_list[0].__dict__.keys()}")
# print(f"Content of first document: {documents_list[0]}")


# # check Attributes of the first two documents | output looks good
# for i, document in enumerate(documents_list[:2]):
#     print(f"\nDocument {i}:")
#     print(f"  Type: {type(document)}")
#     print(f"  Attributes: {list(document.__dict__.keys())}")
#     print(f"  Id: {document.id}")
#     print(f"  Metadata: {document.metadata}")
#     print(f"  Content preview: {document.page_content[:100]}...")
#     print(f"  {'-'*60}")
    
    
    
# Initialize text splitter for chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, # Overlap between chunks
    separators=["\n\n", "\n", " ", ""]
)
# Split documents into chunks
documents_chunks = text_splitter.split_documents(documents_list)
# print(f"\n\nTotal documents chunks created: {len(documents_chunks)}\n")

# # Check the first few chunks, note overlap content | output looks good, we can see the overlapping content
# for i, chunk in enumerate(documents_chunks[:5]):
#     print(f"\nChunk {i}:")
#     print(f"  Type: {type(chunk)}")
#     print(f"  Id: {chunk.id}")
#     print(f"  Metadata: {chunk.metadata}")
#     print(f"  Content preview: {chunk.page_content[:5000]}...")
#     print(f"  {'-'*60}\n")
    
    
# printing all doc_type from chunk metadata  | output looks good
# Unique doc_types in chunks: {'load-balancer', 'azure-network-foundation-services', 'azure-vnet', 'azure-network-security-group'}
doc_types = set(chunk.metadata['doc_type'] for chunk in documents_chunks)
#print(f"\n\nUnique doc_types in chunks: {doc_types}\n")



# # Simple text search for word "pool" | output looks good
# # Output missess contextual information, all matches treated equally, we will improve this later using vector database search
# pool_chunks = [chunk for chunk in documents_chunks if "pool" in chunk.page_content.lower()]
# print(f"Found {len(pool_chunks)} chunks containing 'pool':")

# for i, chunk in enumerate(pool_chunks):
#     print(f"\nChunk {i+1}:")
#     print(f"Source: {chunk.metadata.get('source', 'Unknown')}")
#     print(f"Doc type: {chunk.metadata.get('doc_type', 'Unknown')}")
#     print(f"Content preview: {chunk.page_content[:500]}...")
#     print("-" * 50)


# saving chunks to a pickle file
# Save chunks for vector store
chunks_dir = Path(__file__).parent.parent / "data" / "processed"
chunks_dir.mkdir(parents=True, exist_ok=True)

with open(chunks_dir / "documents_chunks.pkl", "wb") as f:
    pickle.dump(documents_chunks, f)
print(f"Saved {len(documents_chunks)} chunks to {chunks_dir / 'documents_chunks.pkl'}")