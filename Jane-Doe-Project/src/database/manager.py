from typing import List
from .base import DatabaseInterface
from .namus import NamUsInterface
from .doenetwork import DoeNetworkInterface
from .mock import MockDatabaseInterface
from ..models import PersonRecord, SearchCriteria


class DatabaseManager:
    """Manages multiple database interfaces"""
    
    def __init__(self, use_mock_data: bool = True):
        self.databases = {}
        
        # Add mock database for testing/demo purposes
        if use_mock_data:
            self.databases['MockDB'] = MockDatabaseInterface()
        
        # Add real databases (may not work without proper web scraping setup)
        self.databases['NamUs'] = NamUsInterface()
        self.databases['DoeNetwork'] = DoeNetworkInterface()
    
    def get_available_databases(self) -> List[str]:
        """Get list of available database names"""
        available = []
        for name, db in self.databases.items():
            if db.is_available():
                available.append(name)
        return available
    
    def search_all(self, criteria: SearchCriteria) -> List[PersonRecord]:
        """Search all available databases"""
        all_records = []
        
        # Determine which databases to search
        databases_to_search = criteria.databases if criteria.databases else self.get_available_databases()
        
        for db_name in databases_to_search:
            if db_name in self.databases:
                try:
                    records = self.databases[db_name].search(criteria)
                    all_records.extend(records)
                except Exception as e:
                    print(f"Error searching {db_name}: {e}")
            
        return all_records
    
    def search_database(self, database_name: str, criteria: SearchCriteria) -> List[PersonRecord]:
        """Search a specific database"""
        if database_name not in self.databases:
            raise ValueError(f"Database {database_name} not found")
        
        return self.databases[database_name].search(criteria)
    
    def get_record(self, database_name: str, case_id: str) -> PersonRecord:
        """Get a specific record from a database"""
        if database_name not in self.databases:
            raise ValueError(f"Database {database_name} not found")
        
        return self.databases[database_name].get_record(case_id)