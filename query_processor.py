import re
from sklearn.feature_extraction.text import TfidfVectorizer

class QueryProcessor:
    """Handles query understanding, expansion and mapping"""
    
    def __init__(self):
        # Common query patterns and their mappings
        self.query_templates = {
            "status": {
                "patterns": ["status", "current state", "progress", "where are we", "how is it going"],
                "expansion": "What is the current status, phase, and progress details of {}?"
            },
            "technique": {
                "patterns": ["technique", "method", "how to", "procedure", "protocol", "measures", "counter"],
                "expansion": "What are the recommended techniques, methods, and protocols for {}?"
            },
            "security": {
                "patterns": ["security", "protection", "safeguard", "defend", "secure"],
                "expansion": "What are the security measures and protection protocols for {}?"
            },
            "location": {
                "patterns": ["where", "location", "place", "site", "safehouse", "facility"],
                "expansion": "What is the location or access information for {}?"
            },
            "extraction": {
                "patterns": ["extract", "escape", "evacuate", "exit", "remove"],
                "expansion": "What are the extraction procedures and protocols for {}?"
            }
        }
        
        # Operation name detection
        self.operations = [
            "Phantom Veil", "Eclipse", "Hollow Stone", "Void", "Glass Veil", 
            "Red Mist", "Vortex", "Shadow Horizon", "Blue Cipher", "Whispering Gate"
        ]
        
        # Protocol detection
        self.protocols = [
            "S-29", "Zeta", "Shadow Step", "Ghost-Step", "Omega Wave", "Eclipse",
            "Vortex", "Red Mist", "The Silent Room", "Cipher Delta"
        ]
        
        # Initialize TF-IDF vectorizer for keyword extraction
        self.vectorizer = TfidfVectorizer(
            max_features=10,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def analyze_query(self, query):
        """Analyze the query to extract intent, entities, and key terms"""
        analysis = {
            "original_query": query,
            "intent": "information",  # Default intent
            "entities": {
                "operations": [],
                "protocols": [],
                "targets": [],
                "locations": []
            },
            "keywords": []
        }
        
        # Detect query intent
        if re.search(r"how to|procedure|protocol for|steps for", query, re.IGNORECASE):
            analysis["intent"] = "procedure"
        elif re.search(r"where|location|access|find", query, re.IGNORECASE):
            analysis["intent"] = "location"
        elif re.search(r"status|progress|update on|current state", query, re.IGNORECASE):
            analysis["intent"] = "status"
        elif re.search(r"security|protection|safeguard|risk", query, re.IGNORECASE):
            analysis["intent"] = "security"
        
        # Detect operations mentioned in query
        for operation in self.operations:
            if re.search(r"\b" + re.escape(operation) + r"\b", query, re.IGNORECASE):
                analysis["entities"]["operations"].append(operation)
        
        # Detect protocols mentioned in query
        for protocol in self.protocols:
            if re.search(r"\b" + re.escape(protocol) + r"\b", query, re.IGNORECASE):
                analysis["entities"]["protocols"].append(protocol)
        
        # Detect potential locations
        location_patterns = r"base|facility|compound|safehouse|region|area|zone|sector|building"
        locations = re.findall(r"([A-Za-z]+ (?:" + location_patterns + r"))", query, re.IGNORECASE)
        analysis["entities"]["locations"] = locations
        
        # Extract key terms using TF-IDF if there's enough text
        if len(query.split()) > 3:
            try:
                # Prepare the vectorizer with the query
                self.vectorizer.fit_transform([query])
                # Get feature names
                feature_names = self.vectorizer.get_feature_names_out()
                # Take top features as keywords
                analysis["keywords"] = feature_names.tolist()
            except:
                # Fallback to simple keyword extraction
                words = query.lower().split()
                stop_words = ["the", "a", "an", "is", "are", "and", "or", "for", "in", "on", "at", "to"]
                analysis["keywords"] = [word for word in words if len(word) > 3 and word not in stop_words][:5]
        
        return analysis
    
    def expand_query(self, query, analysis):
        """Expand the query based on analysis to improve retrieval"""
        expanded_queries = [query]  # Always include original query
        
        # Add intent-based expansions
        for intent_type, template in self.query_templates.items():
            for pattern in template["patterns"]:
                if pattern in query.lower():
                    # Fill in the template with entities if available
                    for entity_type in ["operations", "protocols"]:
                        entities = analysis["entities"][entity_type]
                        if entities:
                            for entity in entities:
                                expanded_queries.append(template["expansion"].format(entity))
        
        # Add entity-focused queries
        for operation in analysis["entities"]["operations"]:
            expanded_queries.append(f"information about {operation}")
            expanded_queries.append(f"{operation} details")
        
        for protocol in analysis["entities"]["protocols"]:
            expanded_queries.append(f"{protocol} protocol details")
            expanded_queries.append(f"how to implement {protocol}")
        
        # Add keyword-based expansions using different combinations
        keywords = analysis["keywords"]
        if len(keywords) >= 3:
            for i in range(len(keywords)-2):
                keyword_query = f"{keywords[i]} {keywords[i+1]} {keywords[i+2]}"
                expanded_queries.append(keyword_query)
        
        # Ensure expanded queries are unique
        expanded_queries = list(set(expanded_queries))
        
        return expanded_queries
