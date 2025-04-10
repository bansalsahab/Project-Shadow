import numpy as np

class RetrievalEngine:
    """Handles retrieval of relevant chunks based on query"""
    
    def __init__(self, embedding_engine):
        self.embedding_engine = embedding_engine
    
    def vector_similarity(self, v1, v2):
        """Compute cosine similarity between two vectors"""
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        # Handle zero vectors to avoid division by zero
        if norm_v1 == 0 or norm_v2 == 0:
            return 0
            
        return dot_product / (norm_v1 * norm_v2)
    
    def retrieve_relevant_chunks(self, query, all_chunks, document_embeddings, top_k=5):
        """Retrieve top-k relevant chunks using embedding similarity"""
        # Get query embedding
        query_embedding = self.embedding_engine.get_embedding(query)
        if not query_embedding:
            return []
        
        # Create a dictionary to map chunk IDs to their indices
        chunk_index_map = {chunk["id"]: i for i, chunk in enumerate(all_chunks)}
        
        # Compute similarities between query and all chunks
        similarities = []
        for chunk_id, chunk_embedding in document_embeddings.items():
            # Check if chunk_id exists in our chunks (it might have been filtered)
            if chunk_id in chunk_index_map:
                similarity = self.vector_similarity(query_embedding, chunk_embedding)
                similarities.append((chunk_id, similarity))
        
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top-k most similar chunks
        top_chunk_ids = [chunk_id for chunk_id, _ in similarities[:top_k]]
        
        # Map chunk IDs back to the original chunks
        relevant_chunks = []
        scores = {}
        
        for chunk_id in top_chunk_ids:
            index = chunk_index_map[chunk_id]
            chunk = all_chunks[index]
            relevant_chunks.append(chunk)
            
            # Store the similarity score for debugging
            score = next((score for id, score in similarities if id == chunk_id), 0)
            scores[chunk_id] = score
        
        return relevant_chunks, scores
