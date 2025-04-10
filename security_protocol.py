class SecurityProtocol:
    """Handles enforcement of security protocols for information access"""
    
    @staticmethod
    def check_clearance(user_level, required_level):
        """Check if user has clearance for the required level"""
        # Convert user_level to int if it's a string
        if isinstance(user_level, str):
            try:
                user_level = int(user_level)
            except ValueError:
                return False
                
        if isinstance(required_level, str):
            try:
                required_level = int(required_level)
            except ValueError:
                return False
        
        return user_level >= required_level
    
    @staticmethod
    def filter_by_clearance(chunks, user_level):
        """Filter chunks based on user clearance level"""
        filtered_chunks = []
        
        for chunk in chunks:
            required_level = chunk.get("security_level", 1)
            if SecurityProtocol.check_clearance(user_level, required_level):
                filtered_chunks.append(chunk)
        
        return filtered_chunks
