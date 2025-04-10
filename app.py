import streamlit as st
import os
import numpy as np
from pathlib import Path

# Import custom modules
from utils import setup_environment, setup_directories, setup_page
from document_processor import DocumentProcessor
from embedding_engine import EmbeddingEngine
from query_processor import QueryProcessor
from security_protocol import SecurityProtocol
from retrieval_engine import RetrievalEngine
from response_generator import ResponseGenerator

# Setup environment and configure app
api_key = setup_environment()
setup_directories()
setup_page()

# ---------- STREAMLIT UI COMPONENTS ---------- #

# Sidebar
st.sidebar.title("Agent Authentication")
clearance_level = st.sidebar.selectbox(
    "Select Clearance Level",
    ["Level 1 (Basic)", "Level 2 (Intermediate)", "Level 3 (Advanced)", "Level 4 (Executive)"]
)

# Convert text clearance level to numeric for processing
clearance_map = {
    "Level 1 (Basic)": 1,
    "Level 2 (Intermediate)": 2,
    "Level 3 (Advanced)": 3,
    "Level 4 (Executive)": 4
}
user_level = clearance_map.get(clearance_level, 1)

# Options for advanced settings
with st.sidebar.expander("Advanced Settings"):
    force_reprocess = st.checkbox("Force document reprocessing", value=False)
    chunk_strategy = st.radio("Chunking Strategy", ["Semantic", "Fixed-Size"])
    top_k_results = st.slider("Number of results to retrieve", min_value=3, max_value=10, value=5)
    show_debug_info = st.checkbox("Show debug information", value=False)

# Main content
st.title("Project SHADOW - Intelligence Retrieval System")
st.markdown("""
This system processes agent queries while enforcing strict security protocols.
Please enter your query below and ensure you have appropriate clearance.
""")

# Main app logic
query = st.text_area("Enter your query:", "What is the status of Operation Phantom Veil, and what are the recommended counter-surveillance techniques?")

if st.button("Submit Query"):
    with st.spinner("Processing your query..."):
        try:
            # Check for API key
            if not api_key:
                st.error("Google API Key not found. Please add your GOOGLE_API_KEY to the .env file.")
                st.info("Create a .env file with: GOOGLE_API_KEY=your_key_here")
                st.stop()
            
            # Initialize pipeline components
            query_processor = QueryProcessor()
            embedding_engine = EmbeddingEngine()
            retrieval_engine = RetrievalEngine(embedding_engine)
            response_generator = ResponseGenerator()
            
            # Process documents
            document_paths = {
                "Secret_Info_Manual": "SECRET INFO MANUAL.docx",
                "Response_Framework": "RAG CASE RESPONSE FRAMEWORK.docx"
            }
            
            # Process and chunk documents
            all_chunks = []
            for doc_id, doc_name in document_paths.items():
                file_path = str(Path(doc_name).resolve())
                if os.path.exists(file_path):
                    doc_chunks = DocumentProcessor.process_document(file_path, doc_id, force_reprocess)
                    all_chunks.extend(doc_chunks)
                else:
                    st.warning(f"Document not found: {file_path}")
            
            if not all_chunks:
                st.error("No document content was loaded. Please check that the document files exist and are accessible.")
                st.stop()
            
            # Process query
            query_analysis = query_processor.analyze_query(query)
            expanded_queries = query_processor.expand_query(query, query_analysis)
            
            # Apply security protocol - filter chunks by clearance
            allowed_chunks = SecurityProtocol.filter_by_clearance(all_chunks, user_level)
            
            if not allowed_chunks:
                st.warning("Access Denied — Clearance Insufficient.")
                st.stop()
            
            # Compute embeddings for documents
            document_embeddings = {}
            for doc_id in document_paths.keys():
                doc_chunks = [c for c in all_chunks if c["document"] == doc_id]
                if doc_chunks:
                    doc_embeddings = embedding_engine.compute_document_embeddings(
                        doc_chunks,
                        doc_id,
                        force_recompute=force_reprocess
                    )
                    document_embeddings.update(doc_embeddings)
            
            # Retrieve relevant chunks for each expanded query
            all_relevant_chunks = []
            chunk_scores = {}
            
            for expanded_query in expanded_queries:
                relevant_chunks, scores = retrieval_engine.retrieve_relevant_chunks(
                    expanded_query,
                    allowed_chunks,
                    document_embeddings,
                    top_k=top_k_results
                )
                
                # Add to overall collection
                for chunk in relevant_chunks:
                    # Add similarity score to the chunk
                    chunk_id = chunk["id"]
                    if chunk_id in scores:
                        chunk["similarity_score"] = scores[chunk_id]
                    all_relevant_chunks.append(chunk)
                    
                    # Update scores
                    for chunk_id, score in scores.items():
                        if chunk_id not in chunk_scores or score > chunk_scores[chunk_id]:
                            chunk_scores[chunk_id] = score
            
            # Remove duplicates based on chunk_id
            unique_chunks = {}
            for chunk in all_relevant_chunks:
                if chunk["id"] not in unique_chunks or chunk.get("similarity_score", 0) > unique_chunks[chunk["id"]].get("similarity_score", 0):
                    unique_chunks[chunk["id"]] = chunk
            
            # Sort by similarity score
            final_relevant_chunks = sorted(unique_chunks.values(), key=lambda x: x.get("similarity_score", 0), reverse=True)
            
            # Take only top k after combining results from all queries
            final_relevant_chunks = final_relevant_chunks[:top_k_results]
            
            # Generate response
            response = response_generator.generate_response(
                query,
                query_analysis,
                final_relevant_chunks,
                user_level
            )
            
            # Display the response
            st.subheader("Response:")
            st.markdown(response)
            
            # Show debug information if enabled
            if show_debug_info:
                with st.expander("Query Analysis"):
                    st.json(query_analysis)
                
                with st.expander("Expanded Queries"):
                    for i, expanded_query in enumerate(expanded_queries):
                        st.write(f"{i+1}. {expanded_query}")
                
                with st.expander("Retrieved Chunks"):
                    for i, chunk in enumerate(final_relevant_chunks):
                        st.markdown(f"**Chunk {i+1} from {chunk['document']} - {chunk['section']}:**")
                        st.text(f"Similarity: {chunk.get('similarity_score', 0):.4f}")
                        st.text(f"Security Level: {chunk['security_level']}")
                        st.text(chunk['text'][:300] + "..." if len(chunk['text']) > 300 else chunk['text'])
                        st.markdown("---")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
