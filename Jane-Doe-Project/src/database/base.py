from abc import ABC, abstractmethod
from typing import List, Optional
from ..models import PersonRecord, SearchCriteria


class DatabaseInterface(ABC):
    """Abstract base class for database interfaces"""
    
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> List[PersonRecord]:
        """Search the database with given criteria"""
        pass
    
    @abstractmethod
    def get_record(self, case_id: str) -> Optional[PersonRecord]:
        """Get a specific record by case ID"""
        pass
    
    @abstractmethod
    def get_database_name(self) -> str:
        """Return the name of this database"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the database is currently available"""
        pass