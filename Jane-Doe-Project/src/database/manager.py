from typing import List
from .base import DatabaseInterface
from .namus import NamUsInterface
from .doenetwork import DoeNetworkInterface
from ..models import PersonRecord, SearchCriteria


class DatabaseManager:
    """Manages multiple database interfaces"""
    def __init__(self):
        self.databases = {}
        
        # Add real databases
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
        
        # Determine which databases to search - if the specified databases 
        # aren't available, use all available databases
        if criteria.databases:
            # Check if any of the requested databases are actually available
            available_dbs = self.get_available_databases()
            requested_and_available = [db for db in criteria.databases if db in available_dbs]
            
            if requested_and_available:
                databases_to_search = requested_and_available
            else:
                # None of the requested databases are available, use all available
                databases_to_search = available_dbs
        else:
            databases_to_search = self.get_available_databases()
        
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