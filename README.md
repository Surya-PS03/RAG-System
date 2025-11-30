# RAG System

A Retrieval-Augmented Generation (RAG) system built with FastAPI that enables intelligent question answering over documents. The system processes documents (PDF, DOCX, EML), creates vector embeddings, and uses LLM-powered retrieval to answer questions based on document content.

## Features

- **Document Processing**: Supports PDF, DOCX, and EML file formats
- **Intelligent Chunking**: Uses recursive character text splitting for optimal context preservation
- **Vector Search**: FAISS-based vector storage with HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
- **Multi-Query Retrieval**: Generates multiple search queries for improved retrieval accuracy
- **LLM Integration**: Powered by Together AI with Llama 3.2 models
- **REST API**: FastAPI-based endpoint with Bearer token authentication
- **Streaming Downloads**: Efficient file handling for large documents

## Project Structure

```
RAG-System/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── utils/
│   ├── parsing.py          # Document parsing utilities
│   ├── chunking.py         # Text chunking logic
│   ├── vectorizing.py      # Vector embedding and FAISS indexing
│   ├── retrieving.py       # Multi-query retrieval logic
│   ├── output.py           # Response generation
│   └── Wrapper/
│       ├── TogetherWrapper.py    # Together AI client wrapper
│       └── langchainWrapper.py   # LangChain compatibility wrapper
├── hackrx/
│   └── files/              # Temporary file storage for downloaded documents
└── LICENSE                 # MIT License
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Surya-PS03/RAG-System.git
   cd RAG-System
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   BEARER_TOKEN=your_bearer_token_here
   TOGETHER_API_KEY=your_together_api_key_here
   ```

## Usage

### Starting the Server

```bash
python main.py
```

The server will start at `http://0.0.0.0:8000`.

### API Endpoint

**POST** `/hackrx/run`

#### Request Headers
```
Authorization: Bearer <your_bearer_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "documents": "https://example.com/path/to/document.pdf",
  "questions": [
    "What is the coverage amount?",
    "When does the policy expire?"
  ]
}
```

#### Response
```json
{
  "answers": [
    "The coverage amount is $500,000 as stated in Section 2.1.",
    "The policy expires on December 31, 2025."
  ]
}
```

### Example with cURL

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Authorization: Bearer your_bearer_token" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/policy.pdf",
    "questions": ["What is covered under this policy?"]
  }'
```

## How It Works

1. **Document Download**: The system downloads the document from the provided URL
2. **Parsing**: Documents are parsed using LangChain's unstructured loaders
3. **Chunking**: Text is split into chunks of 400 characters with 50-character overlap
4. **Vectorization**: Chunks are embedded using HuggingFace's all-MiniLM-L6-v2 model and stored in FAISS
5. **Retrieval**: Multi-query retrieval generates formal document-style queries for improved accuracy
6. **Response Generation**: The LLM generates answers grounded in the retrieved context

## Dependencies

Key dependencies include:
- **FastAPI** & **Uvicorn**: Web framework and ASGI server
- **LangChain**: Document processing and LLM orchestration
- **FAISS**: Vector similarity search
- **HuggingFace**: Text embeddings
- **Together AI**: LLM inference
- **Unstructured**: Document parsing

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BEARER_TOKEN` | Authentication token for API access |
| `TOGETHER_API_KEY` | API key for Together AI services |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Surya Pratap Singh**

---

*Built for intelligent document question-answering using state-of-the-art RAG techniques.*
