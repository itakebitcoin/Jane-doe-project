from typing import List
from ..models import PersonRecord, SearchCriteria, SearchResult
from ..database import DatabaseManager
from .matching import MatchingEngine


class SearchEngine:
    """Main search engine that coordinates database searches and matching"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.matcher = MatchingEngine()
        self.min_confidence_threshold = 0.3  # Minimum confidence to include in results
    
    def search(self, criteria: SearchCriteria, max_results: int = 50) -> List[SearchResult]:
        """Perform search across all databases and return ranked results"""
        # Get records from databases
        records = self.db_manager.search_all(criteria)
        
        # Calculate match scores
        search_results = []
        for record in records:
            confidence_score, match_reasons = self.matcher.calculate_match_score(record, criteria)
            
            if confidence_score >= self.min_confidence_threshold:
                result = SearchResult(
                    person_record=record,
                    confidence_score=confidence_score,
                    match_reasons=match_reasons
                )
                search_results.append(result)
        
        # Sort by confidence score (highest first)
        search_results.sort(key=lambda x: x.confidence_score, reverse=True)
        
        # Return top results
        return search_results[:max_results]
    
    def search_database(self, database_name: str, criteria: SearchCriteria, 
                       max_results: int = 50) -> List[SearchResult]:
        """Search a specific database"""
        records = self.db_manager.search_database(database_name, criteria)
        
        search_results = []
        for record in records:
            confidence_score, match_reasons = self.matcher.calculate_match_score(record, criteria)
            
            if confidence_score >= self.min_confidence_threshold:
                result = SearchResult(
                    person_record=record,
                    confidence_score=confidence_score,
                    match_reasons=match_reasons
                )
                search_results.append(result)
        
        search_results.sort(key=lambda x: x.confidence_score, reverse=True)
        return search_results[:max_results]
    
    def get_available_databases(self) -> List[str]:
        """Get list of available databases"""
        return self.db_manager.get_available_databases()
    
    def set_confidence_threshold(self, threshold: float):
        """Set minimum confidence threshold for results"""
        self.min_confidence_threshold = max(0.0, min(1.0, threshold))