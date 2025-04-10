import google.generativeai as genai
import streamlit as st

class ResponseGenerator:
    """Generates final responses using LLM"""
    
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model_name = model_name
    
    def generate_response(self, query, query_analysis, relevant_chunks, user_level):
        """Generate a comprehensive response using Gemini"""
        try:
            # Format the context from relevant chunks
            context = ""
            for i, chunk in enumerate(relevant_chunks):
                context += f"\nChunk {i+1}:\n{chunk['text']}\n"
            
            # Detect entities from the query analysis
            entities = []
            for entity_type, entity_list in query_analysis["entities"].items():
                entities.extend(entity_list)
            
            # Construct system prompt with security context
            system_prompt = f"""You are Project SHADOW's Intelligence Retrieval Assistant powered by Google's AI.
You are assisting an intelligence officer with clearance level {user_level}.
            
Only provide information that is appropriate for this clearance level.
Always maintain operational security and confidentiality protocols.
            
Use only the information provided in the context. If you don't have enough information,
acknowledge this without making up details. Provide factual, direct answers.
            
Format your responses in a clear, structured manner using markdown.
If relevant, organize information into sections with headings."""
            
            # Construct the user message that includes context and query
            user_message = f"""Query: {query}
            
Context information:
{context}
            
Based on the context information above, please provide a comprehensive response to my query.
If the information in the context is not sufficient, please indicate this clearly."""
            
            # Create the Gemini model
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            
            # Generate the response
            response = model.generate_content(user_message)
            
            return response.text
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return f"I encountered an error while generating a response: {str(e)}"
