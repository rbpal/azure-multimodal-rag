#!/usr/bin/env python3
"""
Azure RAG Project - Ollama Integration
File: scripts/04-01-rag-local-llm-ollama.py

Integrates Ollama + llama3.1:8b with existing vector store for complete RAG pipeline.
Built to work with your existing document processing and vector store setup.
"""

import os
import sys
import pickle
from pathlib import Path
import time
import requests
import subprocess
import json
from typing import List, Dict, Any

# LangChain imports
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager

# Suppress warnings to keep output clean
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from langchain._api import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

class AzureRAGOllama:
    """Complete RAG system with Ollama integration for Azure documentation"""
    
    def __init__(self, 
                 vector_db_path: str = None,
                 model_name: str = "llama3.1:8b",
                 collection_name: str = "azure_docs",
                 ollama_host: str = "http://localhost:11434"):
        """
        Initialize RAG system with Ollama
        
        Args:
            vector_db_path: Path to existing Chroma vector database
            model_name: Ollama model name
            collection_name: Chroma collection name
            ollama_host: Ollama server URL
        """
        # Set up paths relative to script location (matching your structure)
        base_path = Path(__file__).parent.parent
        self.vector_db_path = vector_db_path or str(base_path / "data" / "vector_store" / "chroma_db")
        self.chunks_file = base_path / "data" / "processed" / "documents_chunks.pkl"
        
        self.model_name = model_name
        self.collection_name = collection_name
        self.ollama_host = ollama_host
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        
        print(f"🚀 Azure RAG System with Ollama")
        print(f"📚 Vector DB: {self.vector_db_path}")
        print(f"🤖 Model: {self.model_name}")
        print(f"🔗 Ollama: {self.ollama_host}")
        
    def check_ollama_status(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            # Check if ollama command exists
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("❌ Ollama not found. Please install it first:")
                print("   curl -fsSL https://ollama.ai/install.sh | sh")
                return False
            
            print(f"✅ Ollama version: {result.stdout.strip()}")
            
            # Check if Ollama service is running
            try:
                response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
                if response.status_code == 200:
                    print("✅ Ollama service is running")
                    return True
                else:
                    print("🔄 Starting Ollama service...")
                    return self.start_ollama_service()
            except requests.exceptions.ConnectionError:
                print("🔄 Starting Ollama service...")
                return self.start_ollama_service()
                
        except FileNotFoundError:
            print("❌ Ollama not found. Please install it first:")
            print("   curl -fsSL https://ollama.ai/install.sh | sh")
            return False
        except subprocess.TimeoutExpired:
            print("⚠️  Ollama command timed out, but continuing...")
            return True
        except Exception as e:
            print(f"❌ Error checking Ollama: {e}")
            return False
    
    def start_ollama_service(self) -> bool:
        """Start Ollama service if not running"""
        try:
            # Start Ollama serve in background
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            # Wait for service to start
            print("⏳ Waiting for Ollama service to start...")
            for i in range(15):
                try:
                    response = requests.get(f"{self.ollama_host}/api/tags", timeout=2)
                    if response.status_code == 200:
                        print("✅ Ollama service started successfully")
                        return True
                except:
                    time.sleep(1)
            
            print("⚠️  Ollama service may not be fully ready, but continuing...")
            return True
            
        except Exception as e:
            print(f"❌ Error starting Ollama service: {e}")
            return False
    
    def check_model_availability(self) -> bool:
        """Check if the required model is available"""
        try:
            print(f"🔍 Checking for model: {self.model_name}")
            
            # List available models
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json()
                existing_models = [model['name'] for model in models.get('models', [])]
                
                if self.model_name in existing_models:
                    print(f"✅ Model {self.model_name} is available")
                    return True
                else:
                    print(f"❌ Model {self.model_name} not found")
                    print("Available models:", existing_models)
                    print(f"💡 Please run: ollama pull {self.model_name}")
                    return False
            else:
                print(f"❌ Could not check models (status: {response.status_code})")
                return False
                
        except Exception as e:
            print(f"❌ Error checking model availability: {e}")
            return False
    
    def load_vector_store(self) -> bool:
        """Load existing Chroma vector database"""
        try:
            print(f"📚 Loading vector store from: {self.vector_db_path}")
            
            # Check if vector store exists
            if not Path(self.vector_db_path).exists():
                print(f"❌ Vector store not found at {self.vector_db_path}")
                print("💡 Please run 03-01-rag-vector-store-chroma.py first")
                return False
            
            # Initialize OpenAI embeddings (same as used during creation)
            embeddings = OpenAIEmbeddings()
            
            # Load existing Chroma database
            self.vectorstore = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=embeddings,
                collection_name=self.collection_name
            )
            
            # Test vector store
            collection = self.vectorstore._collection
            count = collection.count()
            print(f"✅ Vector store loaded successfully. Document count: {count}")
            
            # Quick test search
            test_results = self.vectorstore.similarity_search("Azure", k=1)
            if test_results:
                print(f"✅ Vector search working. Sample doc type: {test_results[0].metadata.get('doc_type', 'Unknown')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            print("💡 Make sure you have OPENAI_API_KEY set and vector store created")
            return False
    
    def initialize_ollama_llm(self) -> bool:
        """Initialize Ollama LLM"""
        try:
            print(f"🤖 Initializing Ollama LLM: {self.model_name}")
            
            # Setup streaming callback for real-time responses
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            
            # Initialize Ollama LLM with optimized settings for your MacBook Pro
            self.llm = Ollama(
                model=self.model_name,
                base_url=self.ollama_host,
                callback_manager=callback_manager,
                temperature=0.1,      # Lower for more focused technical responses
                top_p=0.9,           # Nucleus sampling
                repeat_penalty=1.1,   # Reduce repetition
                stop=["</s>", "Human:", "Assistant:", "###", "\n\nHuman:", "\n\nAssistant:"],
                # Ollama-specific optimizations
                num_ctx=4096,        # Context window
                num_predict=2048,    # Max tokens to generate
                num_thread=8,        # Use all 8 cores of your i9
            )
            
            # Test LLM with a simple query
            print("🧪 Testing Ollama LLM connection...")
            try:
                test_response = self.llm("Respond with exactly: 'Ollama LLM ready!'")
                print(f"✅ LLM test successful: {test_response.strip()}")
                return True
            except Exception as e:
                print(f"❌ LLM test failed: {e}")
                return False
            
        except Exception as e:
            print(f"❌ Error initializing Ollama LLM: {e}")
            return False
    
    def create_rag_chain(self) -> bool:
        """Create RAG chain combining retrieval and generation"""
        try:
            print("🔗 Creating RAG chain...")
            
            # Optimized prompt template for Azure technical documentation
            prompt_template = """You are an expert Azure cloud engineer assistant. Use the following context from Azure documentation to answer the question accurately and comprehensively.

Context from Azure Documentation:
{context}

Question: {question}

Instructions:
- Provide clear, technical answers based on the Azure documentation context
- Include specific configuration steps when relevant
- Mention any prerequisites or important considerations
- Use proper Azure terminology and best practices
- If the context doesn't contain enough information, state this clearly
- Keep responses concise but comprehensive

Answer:"""

            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create retrieval QA chain with optimized settings
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 5}  # Retrieve top 5 most relevant chunks
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            
            print("✅ RAG chain created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating RAG chain: {e}")
            return False
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system with performance monitoring"""
        try:
            start_time = time.time()
            print(f"\n🔍 Processing query: {question}")
            print("💭 Searching documentation and generating response...")
            
            # Get response from RAG chain
            response = self.qa_chain({"query": question})
            
            processing_time = time.time() - start_time
            
            # Extract source documents
            source_docs = []
            if "source_documents" in response:
                for doc in response["source_documents"]:
                    source_docs.append({
                        "content": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                        "metadata": doc.metadata,
                        "doc_type": doc.metadata.get("doc_type", "Unknown"),
                        "source": doc.metadata.get("source", "Unknown").split('/')[-1]
                    })
            
            print(f"\n⏱️  Query processed in {processing_time:.2f} seconds")
            
            return {
                "question": question,
                "answer": response["result"],
                "source_documents": source_docs,
                "num_sources": len(source_docs),
                "processing_time": processing_time
            }
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return {
                "question": question,
                "answer": f"Error processing query: {e}",
                "source_documents": [],
                "num_sources": 0,
                "processing_time": 0
            }
    
    def interactive_chat(self):
        """Enhanced interactive chat interface"""
        print("\n" + "="*90)
        print("🚀 Azure RAG System - Interactive Chat")
        print("="*90)
        print(f"🤖 Model: {self.model_name}")
        print(f"💻 Hardware: MacBook Pro 8-core i9, 32GB RAM")
        print(f"📚 Knowledge Base: Azure networking documentation")
        print("="*90)
        print("Ask questions about Azure VNets, Load Balancers, NSGs, Front Door, etc.")
        print("Commands: 'quit'/'exit'/'q' to end, 'help' for examples, 'stats' for info")
        print("="*90 + "\n")
        
        query_count = 0
        total_time = 0
        
        while True:
            try:
                question = input("💬 Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    if query_count > 0:
                        avg_time = total_time / query_count
                        print(f"\n📊 Session Stats: {query_count} queries, avg {avg_time:.2f}s per query")
                    print("\n👋 Thank you for using Azure RAG System!")
                    break
                
                if question.lower() == 'help':
                    self.show_example_questions()
                    continue
                
                if question.lower() == 'stats':
                    self.show_system_info()
                    continue
                
                if not question:
                    continue
                
                # Get response with timing
                result = self.query(question)
                query_count += 1
                total_time += result["processing_time"]
                
                # Display answer
                print(f"\n📋 Answer:")
                print(result["answer"])
                
                # Display sources
                if result["source_documents"]:
                    print(f"\n📚 Sources ({result['num_sources']} documents):")
                    for i, doc in enumerate(result["source_documents"], 1):
                        doc_type = doc["doc_type"]
                        source = doc["source"]
                        content_preview = doc['content'][:150] + "..." if len(doc['content']) > 150 else doc['content']
                        print(f"  {i}. [{doc_type}] {source}")
                        print(f"     {content_preview}")
                
                print("\n" + "-" * 90)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def show_example_questions(self):
        """Show categorized example questions"""
        categories = {
            "🌐 Virtual Networks": [
                "What is Azure Virtual Network peering?",
                "How to configure VNet subnets?",
                "Azure VNet connectivity options"
            ],
            "⚖️ Load Balancers": [
                "What is Azure Load Balancer backend pool?",
                "Differences between Basic and Standard Load Balancer",
                "How to configure health probes?"
            ],
            "🛡️ Network Security": [
                "How to configure network security groups?",
                "Azure NSG rule priorities explained",
                "Best practices for NSG configuration"
            ],
            "🚪 Azure Front Door": [
                "What is Azure Front Door?",
                "How to set up Azure Front Door?",
                "Azure WAF with Front Door configuration"
            ]
        }
        
        print("\n💡 Example Questions by Category:")
        print("-" * 70)
        for category, questions in categories.items():
            print(f"\n{category}")
            for q in questions:
                print(f"  • {q}")
        print("-" * 70)
    
    def show_system_info(self):
        """Show system and model information"""
        try:
            print(f"\n📊 System Information:")
            print(f"  Model: {self.model_name}")
            print(f"  Ollama Host: {self.ollama_host}")
            print(f"  Vector Store: {self.vector_db_path}")
            print(f"  Collection: {self.collection_name}")
            
            # Try to get model info
            try:
                response = requests.get(f"{self.ollama_host}/api/show", 
                                      json={"name": self.model_name}, timeout=5)
                if response.status_code == 200:
                    model_info = response.json()
                    if 'details' in model_info:
                        details = model_info['details']
                        print(f"  Parameters: {details.get('parameter_size', 'Unknown')}")
                        print(f"  Quantization: {details.get('quantization_level', 'Unknown')}")
            except:
                print("  Model details: Could not retrieve")
            
        except Exception as e:
            print(f"  Error retrieving system info: {e}")
    
    def run_performance_test(self):
        """Run performance test with Azure-specific queries"""
        test_queries = [
            "What is Azure Load Balancer?",
            "How to configure NSG rules?",
            "Azure VNet peering setup process",
            "What are Azure Front Door health probes?",
            "Azure DDoS Protection features"
        ]
        
        print("\n🧪 Performance Test - Azure RAG System")
        print("="*80)
        
        total_time = 0
        successful_queries = 0
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}/5: {query}")
            print("-" * 60)
            
            result = self.query(query)
            
            if result["processing_time"] > 0:
                successful_queries += 1
                total_time += result["processing_time"]
                
                print(f"✅ Success: {result['processing_time']:.2f}s")
                print(f"📊 Sources: {result['num_sources']} documents")
                print(f"📝 Answer length: {len(result['answer'])} chars")
                print(f"🎯 Sample: {result['answer'][:100]}...")
            else:
                print(f"❌ Failed")
        
        if successful_queries > 0:
            avg_time = total_time / successful_queries
            print(f"\n🎯 Performance Summary:")
            print(f"  Model: {self.model_name}")
            print(f"  Success rate: {successful_queries}/{len(test_queries)} ({successful_queries/len(test_queries)*100:.1f}%)")
            print(f"  Average response time: {avg_time:.2f}s")
            print(f"  Total test time: {total_time:.2f}s")
        
        print("="*80)

def main():
    """Main function with comprehensive setup and error handling"""
    try:
        print("🚀 Azure RAG System - Ollama Integration")
        print("="*60)
        
        # Initialize RAG system
        rag_system = AzureRAGOllama()
        
        # Step 1: Check Ollama installation and service
        print("\n📋 Step 1: Checking Ollama...")
        if not rag_system.check_ollama_status():
            print("❌ Ollama setup failed. Please install Ollama and try again.")
            return False
        
        # Step 2: Check model availability
        print("\n📋 Step 2: Checking model...")
        if not rag_system.check_model_availability():
            print(f"❌ Model {rag_system.model_name} not available.")
            print(f"💡 Run: ollama pull {rag_system.model_name}")
            return False
        
        # Step 3: Load vector store
        print("\n📋 Step 3: Loading vector store...")
        if not rag_system.load_vector_store():
            print("❌ Vector store loading failed.")
            return False
        
        # Step 4: Initialize Ollama LLM
        print("\n📋 Step 4: Initializing LLM...")
        if not rag_system.initialize_ollama_llm():
            print("❌ LLM initialization failed.")
            return False
        
        # Step 5: Create RAG chain
        print("\n📋 Step 5: Creating RAG chain...")
        if not rag_system.create_rag_chain():
            print("❌ RAG chain creation failed.")
            return False
        
        print("\n✅ All systems ready! Azure RAG with Ollama is operational.")
        
        # Main menu
        while True:
            print("\n" + "="*70)
            print("🔧 Azure RAG System - Main Menu")
            print("="*70)
            print("1. 💬 Interactive Chat")
            print("2. 🧪 Performance Test")
            print("3. 📊 System Info")
            print("4. 🚪 Exit")
            print("="*70)
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                rag_system.interactive_chat()
            elif choice == '2':
                rag_system.run_performance_test()
            elif choice == '3':
                rag_system.show_system_info()
            elif choice == '4':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-4.")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
        return True
    except Exception as e:
        print(f"❌ Fatal error in main: {e}")
        return False

if __name__ == "__main__":
    main()