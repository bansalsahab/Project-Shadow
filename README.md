# Project SHADOW - Intelligence Retrieval System

An advanced intelligence retrieval assistant designed to process classified queries while enforcing strict security protocols and providing transparent, structured responses.

## Project Overview

This system provides a secure interface for intelligence retrieval with the following advanced features:

### Core Features
- **Vector Similarity Retrieval**: Breaks down content into meaningful chunks and uses embeddings to retrieve the most relevant information.
- **Graph Traversal**: Identifies key entities and relationships, creating a knowledge graph for contextual information retrieval.
- **Security Protocol Enforcement**: Rigorous checking of agent clearance levels before returning sensitive information.
- **Transparent Response Structure**: Clearly labels information sources and provides justifications for retrieval steps.

### Enhanced Features
- **Advanced Semantic Chunking**: Documents are chunked based on semantic boundaries like paragraphs and section headings rather than fixed-size splits.
- **Operation & Protocol Detection**: Automatically identifies and extracts mentions of classified operations and protocols in the documents.
- **Intelligent Query Mapping**: Analyzes queries to determine intent, extract entities, and expand queries to improve retrieval accuracy.
- **Entity Recognition System**: Identifies key entities like operations, protocols, safehouses, and techniques mentioned in queries.
- **Multi-Level Security Clearance**: Maps user clearance levels to the RAW classification system used in the documents.
- **Query Expansion System**: Transforms the original query into multiple variations to improve retrieval coverage.
- **Persistent Storage Architecture**: Caches processed chunks and embeddings for faster response times on repeated queries.
  
## Data Flow Diagram
![diagram-export-4-12-2025-12_18_25-AM](https://github.com/user-attachments/assets/2fdb4284-b84e-4e9d-9fca-405ebfaffe4c)


## Project Structure

The codebase has been modularized for better organization and maintainability:

- **app.py**: Main Streamlit application that provides the user interface and orchestrates the overall information retrieval workflow.
- **utils.py**: Common utilities, environment setup, and configuration.
- **document_processor.py**: Handles document loading, parsing, and chunking with advanced techniques.
- **embedding_engine.py**: Creates and manages embeddings using Google's Generative AI API.
- **query_processor.py**: Analyzes queries to extract intent, entities, and expands them for better retrieval.
- **security_protocol.py**: Enforces security protocols and clearance levels for information access.
- **retrieval_engine.py**: Retrieves relevant chunks of information using vector similarity.
- **response_generator.py**: Generates final responses using Google's Gemini LLM.

## Requirements

- Python 3.8+
- Google Gemini API Key (configured in .env file)
- Required Python packages (see requirements.txt)

## Setup and Running

1. Create a `.env` file in the project root with your Google API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python -m streamlit run app.py
   ```

## Usage

1. Run the Streamlit application:
```
streamlit run app.py
```

2. Open your browser and navigate to http://localhost:8501
3. Select your clearance level from the sidebar
4. Enter your query in the text area
5. Click "Submit Query" to process your query

## Advanced Usage

### Configurable Settings
The application provides advanced settings in the sidebar:
- **Force document reprocessing**: Forces the system to reprocess documents even if cached chunks exist
- **Chunking Strategy**: Choose between semantic and fixed-size chunking
- **Number of results**: Control how many chunks to retrieve
- **Debug information**: View detailed information about query processing and retrieval

### Extending the System
The modular pipeline architecture makes it easy to extend the system with new capabilities:
- Add new document types by creating parsers in the DocumentProcessor class
- Implement new query understanding strategies in the QueryProcessor class
- Create additional security protocols in the SecurityProtocol class
- Enhance the retrieval engine with additional algorithms

## Security Features

- Multi-level clearance checking for sensitive information
- Access denial for queries beyond an agent's clearance level
- Transparent justification for information retrieval
- Source labeling for all retrieved information
- Security level detection within document chunks
- RAW-specific security protocols implementation

## Example Query

"What is the status of Operation Phantom Veil, and what are the recommended counter-surveillance techniques?"


## Notes

This project implements a sophisticated retrieval system using the following advanced techniques:
1. **Semantic Chunking**: Breaking documents at meaningful boundaries
2. **Query Intent Detection**: Understanding what the user is asking for
3. **Entity Recognition**: Identifying key elements like operations and protocols
4. **Security Protocols**: Enforcing strict access control
5. **Modular Architecture**: Allowing for easy extension and modification
