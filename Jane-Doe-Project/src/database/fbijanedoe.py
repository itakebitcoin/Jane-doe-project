import requests
from typing import List, Optional
from .base import DatabaseInterface
from ..models import PersonRecord, SearchCriteria

class FBIJaneDoeInterface(DatabaseInterface):
    """Interface for searching the FBI Jane Doe database"""
    def __init__(self):
        self.base_url = "https://www.fbi.gov/wanted/vicap/unidentified-persons/jane-does"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_database_name(self) -> str:
        return "FBIJaneDoe"

    def is_available(self) -> bool:
        try:
            response = self.session.get(self.base_url, timeout=10)
            return response.status_code == 200
        except Exception:
            return False

    def search(self, criteria: SearchCriteria) -> List[PersonRecord]:
        # FBI Jane Doe DB does not support programmatic search at this time.
        # No mock data is returned; always returns an empty list.
        return []

    def get_record(self, case_id: str) -> Optional[PersonRecord]:
        # FBI Jane Doe DB does not support programmatic record retrieval at this time.
        # Always returns None.
        return None
