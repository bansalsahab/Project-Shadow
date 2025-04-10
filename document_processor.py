import os
import re
import json
import hashlib
import docx
from nltk.tokenize import sent_tokenize
import streamlit as st

class DocumentProcessor:
    """Handles document loading, parsing and chunking with advanced techniques"""

    @staticmethod
    def read_docx(file_path):
        """Read DOCX file and extract text while preserving some structure"""
        doc = docx.Document(file_path)
        sections = []
        
        current_heading = "Introduction"
        current_section = []
        
        for para in doc.paragraphs:
            # Check if it's a heading by style
            if para.style.name.startswith('Heading'):
                # Save previous section if it exists
                if current_section:
                    sections.append({
                        "heading": current_heading,
                        "content": "\n".join(current_section)
                    })
                    current_section = []
                
                current_heading = para.text
            elif para.text.strip():
                current_section.append(para.text)
        
        # Add the last section
        if current_section:
            sections.append({
                "heading": current_heading,
                "content": "\n".join(current_section)
            })
        
        return sections

    @staticmethod
    def semantic_chunking(text, min_size=100, max_size=1000):
        """Chunk text based on semantic boundaries like sentences and paragraphs"""
        # First split by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            # If the paragraph itself is too large, split it by sentences
            if len(para) > max_size:
                sentences = sent_tokenize(para)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) <= max_size:
                        current_chunk += " " + sentence if current_chunk else sentence
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = sentence
            else:
                # Check if adding this paragraph would exceed max size
                if len(current_chunk) + len(para) <= max_size:
                    current_chunk += "\n\n" + para if current_chunk else para
                else:
                    if current_chunk and len(current_chunk) >= min_size:
                        chunks.append(current_chunk)
                    current_chunk = para
        
        # Add the last chunk if it exists
        if current_chunk and len(current_chunk) >= min_size:
            chunks.append(current_chunk)
            
        return chunks

    @staticmethod
    def process_document(file_path, doc_id, force_reprocess=False):
        """Process a document and store chunks with metadata"""
        # Create unique ID for the document based on path
        doc_hash = hashlib.md5(file_path.encode()).hexdigest()
        chunk_file = f"data/chunks/{doc_id}_{doc_hash}.json"
        
        # Check if processed chunks already exist
        if os.path.exists(chunk_file) and not force_reprocess:
            with open(chunk_file, 'r') as f:
                return json.load(f)
        
        # Process document based on type
        if file_path.endswith('.docx'):
            sections = DocumentProcessor.read_docx(file_path)
            
            # Create chunks with metadata
            chunks = []
            for section in sections:
                section_chunks = DocumentProcessor.semantic_chunking(section["content"])
                
                for i, chunk_text in enumerate(section_chunks):
                    # Detect security level in the chunk
                    security_level = 1  # Default level
                    if re.search(r"level\s*[5-9]|clearance\s*[5-9]", chunk_text.lower(), re.IGNORECASE):
                        security_level = 4  # Map to our highest level
                    elif re.search(r"level\s*[34]|clearance\s*[34]", chunk_text.lower(), re.IGNORECASE):
                        security_level = 3
                    elif re.search(r"level\s*2|clearance\s*2", chunk_text.lower(), re.IGNORECASE):
                        security_level = 2
                    elif re.search(r"level\s*1|clearance\s*1", chunk_text.lower(), re.IGNORECASE):
                        security_level = 1
                    
                    # Extract operation information if present
                    operations = []
                    if re.search(r"operation\s+\w+|project\s+\w+|protocol\s+\w+", chunk_text.lower(), re.IGNORECASE):
                        op_matches = re.findall(r"operation\s+(\w+)|project\s+(\w+)|protocol\s+(\w+)", chunk_text, re.IGNORECASE)
                        for match in op_matches:
                            ops = [op for op in match if op]
                            operations.extend(ops)
                    
                    chunk = {
                        "id": f"{doc_id}_{section['heading']}_{i}",
                        "text": chunk_text,
                        "document": doc_id,
                        "section": section["heading"],
                        "security_level": security_level,
                        "operations": operations,
                        "position": i
                    }
                    chunks.append(chunk)
            
            # Save chunks to file
            with open(chunk_file, 'w') as f:
                json.dump(chunks, f)
            
            return chunks
        else:
            st.error(f"Unsupported file format for {file_path}")
            return []
