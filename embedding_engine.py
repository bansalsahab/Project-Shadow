import os
import pickle
import streamlit as st
import google.generativeai as genai

class EmbeddingEngine:
    """Handles creation and retrieval of embeddings"""
    
    def __init__(self, model_name="models/embedding-001"):
        self.model_name = model_name
    
    def get_embedding(self, text):
        """Get embedding for a text using Google Generative AI"""
        try:
            embedding = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            return embedding["embedding"]
        except Exception as e:
            st.error(f"Error generating embedding: {str(e)}")
            return None
    
    def compute_document_embeddings(self, chunks, doc_id, force_recompute=False):
        """Compute embeddings for document chunks and store them"""
        embeddings_file = f"data/embeddings/{doc_id}_embeddings.pkl"
        
        # Check if embeddings already exist
        if os.path.exists(embeddings_file) and not force_recompute:
            with open(embeddings_file, 'rb') as f:
                return pickle.load(f)
        
        # Compute embeddings for all chunks
        embeddings = {}
        for chunk in chunks:
            chunk_id = chunk["id"]
            embedding = self.get_embedding(chunk["text"])
            if embedding:
                embeddings[chunk_id] = embedding
                
        # Save embeddings to file
        with open(embeddings_file, 'wb') as f:
            pickle.dump(embeddings, f)
        
        return embeddings
