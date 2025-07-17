
# Azure RAG System with Ollama Integration

**Advanced RAG system for Azure networking documentation with local LLM inference**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-orange.svg)](https://ollama.ai/)

An intelligent Azure networking knowledge assistant that processes technical documentation to provide accurate, context-aware responses. Built with Ollama + llama3.1:8b for completely local, privacy-focused deployment.

## 🚀 Key Features

- **🤖 Local LLM Inference**: Uses Ollama + llama3.1:8b for cost-effective, privacy-focused deployment
- **📚 Document Processing**: Intelligent chunking and vectorization of Azure networking documentation
- **🔍 Semantic Search**: Advanced vector similarity search using OpenAI embeddings
- **🛡️ Azure Networking Expertise**: Specialized knowledge of VNets, Load Balancers, NSGs, Front Door, and more
- **💻 Hardware Optimized**: Designed for efficient resource usage on MacBook Pro and similar hardware
- **🔬 Diagnostic Tools**: Built-in analysis to see exactly how RAG retrieval and generation works
- **📊 Performance Monitoring**: Real-time response time tracking and system optimization

## 🏗️ System Architecture

```
User Query → Vector Search (Chroma) → Context Retrieval → LLM Generation (Ollama) → Response
     ↓              ↓                      ↓                    ↓
PDF/Markdown → Document Chunks → Vector Embeddings → Llama3.1:8b → Formatted Answer
```

## 📁 Project Structure

```
azure-multimodal-rag/
├── scripts/
│   ├── 01-01-utility-convert-pdf-to-markdown.py    # PDF to Markdown conversion
│   ├── 02-01-rag-langchain-textSplitChunkOptimization.py  # Document processing
│   ├── 03-01-rag-vector-store-chroma.py            # Vector database creation
│   └── 04-01-rag-local-llm-ollama.py              # 🆕 Ollama RAG integration
├── data/
│   ├── raw/markdown/                                # Source documentation
│   ├── processed/documents_chunks.pkl              # Processed text chunks
│   └── vector_store/chroma_db/                     # Vector database
└── logs/                                           # System logs
```

## 🛠️ Quick Start

### Prerequisites

- **Python 3.9+**
- **Ollama** installed
- **OpenAI API key** (for embeddings)
- **32GB RAM recommended** for optimal performance

### 1. Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the model (4.9GB download)
ollama pull llama3.1:8b
```

### 2. Setup Python Environment

```bash
# Clone repository
git clone <repository-url>
cd azure-multimodal-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Set OpenAI API key for embeddings
export OPENAI_API_KEY="your-api-key-here"
```

### 4. Process Documents and Create Vector Database

```bash
# Step 1: Process documents into chunks
cd scripts/
python3 02-01-rag-langchain-textSplitChunkOptimization.py

# Step 2: Create vector database
python3 03-01-rag-vector-store-chroma.py
```

### 5. Run the RAG System

```bash
# Start the complete RAG system
python3 04-01-rag-local-llm-ollama.py
```

## 🎯 Usage Examples

### Interactive Chat
```bash
💬 Your question: What is Azure Load Balancer backend pool?

📋 Answer: An Azure Load Balancer backend pool is a collection of virtual machines 
or instances that receive traffic distributed by the load balancer...

📚 Sources (3 documents):
  1. [load-balancer] 02-study-guide-az-load-balancer.md
```

### Diagnostic Mode
```bash
💬 Your question: debug what is nsg

🔍 QUERY: what is nsg
📝 COMPLETE PROMPT SENT TO MODEL:
[Shows exact context from vector database]

🤖 MODEL RESPONSE:
[Shows model's complete response]
```

## 📊 Performance Specifications

### Hardware Requirements
- **CPU**: 4+ cores (8-core i9 recommended)
- **RAM**: 16GB minimum, 32GB recommended
- **Storage**: 10GB for models and data
- **GPU**: Optional (Metal acceleration on macOS)

### Expected Performance
- **Response Time**: 3-8 seconds per query
- **Model Size**: 4.9GB (llama3.1:8b)
- **Memory Usage**: 8-12GB during inference
- **Document Coverage**: 475+ processed chunks

## 🔧 Configuration Options

### Model Selection
```bash
# Different model options
ollama pull llama3.1:8b          # Balanced (recommended)
ollama pull llama3.1:13b         # Higher quality
ollama pull phi3:mini            # Faster inference
```

### System Optimization
```python
# Customize in the script
model_name = "llama3.1:8b"       # Model selection
search_kwargs = {"k": 5}         # Context chunks
temperature = 0.1                # Response focus
```

## 🧪 Built-in Features

### Menu Options
1. **💬 Interactive Chat** - Natural conversation interface
2. **🧪 Performance Test** - System validation with Azure queries
3. **📊 System Info** - Hardware and model statistics
4. **🔬 Simple Diagnostic** - RAG pipeline analysis
5. **🚪 Exit** - Clean shutdown

### Special Commands
- `debug <question>` - Shows complete prompt and response analysis
- `help` - Display example questions by category
- `stats` - System performance information
- `quit` - Exit the session

## 📚 Knowledge Base

Currently includes documentation for:
- **Azure Virtual Networks (VNets)** - Peering, subnets, connectivity
- **Azure Load Balancer** - Backend pools, health probes, configuration
- **Network Security Groups (NSGs)** - Rules, priorities, best practices
- **Azure Front Door** - WAF, health probes, routing methods
- **Azure DDoS Protection** - Features and configuration

## 🔍 Diagnostic Capabilities

The system includes advanced diagnostic tools to understand RAG behavior:

- **Vector Database Analysis** - See exact chunks retrieved
- **Prompt Inspection** - View complete context sent to model
- **Response Analysis** - Understand model generation process
- **Performance Metrics** - Track response times and accuracy

## 🚀 Future Enhancements

- **Multi-Modal Processing** - Image and diagram analysis capability
- **Additional Models** - Support for vision-language models
- **Expanded Knowledge** - More Azure services and scenarios
- **API Interface** - REST API for integration
- **Advanced Analytics** - Query pattern analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** for local LLM infrastructure
- **LangChain** for RAG framework
- **Chroma** for vector database
- **Meta** for Llama 3.1 models

## 📞 Support

For questions and support:
- Open an issue on GitHub
- Check the diagnostic tools for troubleshooting
- Review the logs in the `logs/` directory

---

**Built for Azure professionals who need accurate, local, and private access to Azure networking knowledge.** 🎯