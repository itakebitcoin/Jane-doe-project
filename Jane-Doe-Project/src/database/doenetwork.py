import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
import re
import time

from .base import DatabaseInterface
from ..models import PersonRecord, SearchCriteria, PhysicalCharacteristics, Location, Race, Sex


class DoeNetworkInterface(DatabaseInterface):
    """Interface for searching Doe Network database"""
    
    def __init__(self):
        self.base_url = "https://www.doenetwork.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_database_name(self) -> str:
        return "DoeNetwork"
    
    def is_available(self) -> bool:
        """Check if Doe Network is available"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def search(self, criteria: SearchCriteria) -> List[PersonRecord]:
        """Search Doe Network database with given criteria"""
        try:
            # Doe Network typically requires browsing by state/region
            records = []
            
            if criteria.location and criteria.location.state:
                records.extend(self._search_by_state(criteria, criteria.location.state))
            else:
                # Search all states (be respectful with rate limiting)
                states = self._get_available_states()
                for state in states[:5]:  # Limit to first 5 states for demo
                    time.sleep(1)  # Rate limiting
                    records.extend(self._search_by_state(criteria, state))
            
            return records
            
        except Exception as e:
            print(f"Error searching Doe Network: {e}")
            return []
    
    def get_record(self, case_id: str) -> Optional[PersonRecord]:
        """Get a specific record by case ID"""
        try:
            # Doe Network case URLs vary by state
            # This would need to be implemented based on case ID format
            return None
            
        except Exception as e:
            print(f"Error getting Doe Network record {case_id}: {e}")
            return None
    
    def _get_available_states(self) -> List[str]:
        """Get list of available states from Doe Network"""
        try:
            response = self.session.get(f"{self.base_url}/cases/", timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract state links (implementation depends on site structure)
            state_links = soup.find_all('a', href=re.compile(r'/cases/.*\.html'))
            states = []
            
            for link in state_links:
                href = link.get('href', '')
                # Extract state abbreviation from URL
                state_match = re.search(r'/([A-Z]{2})\.html', href)
                if state_match:
                    states.append(state_match.group(1))
            
            return list(set(states))  # Remove duplicates
            
        except Exception as e:
            print(f"Error getting states: {e}")
            return ['CA', 'TX', 'NY', 'FL', 'PA']  # Default states
    
    def _search_by_state(self, criteria: SearchCriteria, state: str) -> List[PersonRecord]:
        """Search cases in a specific state"""
        try:
            # Get state page
            state_url = f"{self.base_url}/cases/{state}.html"
            response = self.session.get(state_url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find case links
            case_links = soup.find_all('a', href=re.compile(r'case.*\.html'))
            records = []
            
            for link in case_links:
                try:
                    case_url = link.get('href')
                    if case_url:
                        record = self._parse_case_from_link(case_url, state)
                        if record and self._matches_criteria(record, criteria):
                            records.append(record)
                except Exception as e:
                    print(f"Error parsing case link: {e}")
                    continue
            
            return records
            
        except Exception as e:
            print(f"Error searching state {state}: {e}")
            return []
    
    def _parse_case_from_link(self, case_url: str, state: str) -> Optional[PersonRecord]:
        """Parse case information from a case URL"""
        try:
            if not case_url.startswith('http'):
                case_url = f"{self.base_url}/{case_url.lstrip('/')}"
            
            response = self.session.get(case_url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract case ID from URL
            case_id = re.search(r'([^/]+)\.html$', case_url)
            case_id = case_id.group(1) if case_id else case_url
            
            record = PersonRecord(
                case_id=case_id,
                database_source="DoeNetwork",
                case_url=case_url,
                last_updated=datetime.now()
            )
            
            # Parse case details
            text_content = soup.get_text()
            record.physical_characteristics = self._extract_characteristics_from_text(text_content)
            record.location_found = Location(state=state)
            record.circumstances = self._extract_circumstances_from_text(text_content)
            
            return record
            
        except Exception as e:
            print(f"Error parsing case from {case_url}: {e}")
            return None
    
    def _extract_characteristics_from_text(self, text: str) -> PhysicalCharacteristics:
        """Extract physical characteristics from case text"""
        characteristics = PhysicalCharacteristics()
        
        # Height extraction
        height_patterns = [
            r'(\d+)\s*(?:feet|ft|\')\s*(\d+)\s*(?:inches|in|\")',
            r'(\d+)\'\s*(\d+)\"',
            r'Height:\s*(\d+)\'\s*(\d+)\"'
        ]
        
        for pattern in height_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                feet, inches = int(match.group(1)), int(match.group(2))
                height = feet * 12 + inches
                characteristics.height_min = characteristics.height_max = height
                break
        
        # Weight extraction
        weight_match = re.search(r'(?:Weight|weighs?):\s*(\d+)\s*(?:pounds|lbs|lb)', text, re.IGNORECASE)
        if weight_match:
            weight = int(weight_match.group(1))
            characteristics.weight_min = characteristics.weight_max = weight
        
        # Race extraction
        for race in Race:
            if race.value.lower() in text.lower():
                characteristics.race = race
                break
        
        # Sex extraction
        for sex in Sex:
            if sex.value.lower() in text.lower():
                characteristics.sex = sex
                break
        
        # Age extraction
        age_match = re.search(r'(?:Age|aged?):\s*(\d+)(?:\s*-\s*(\d+))?', text, re.IGNORECASE)
        if age_match:
            age_min = int(age_match.group(1))
            age_max = int(age_match.group(2)) if age_match.group(2) else age_min
            characteristics.age_min = age_min
            characteristics.age_max = age_max
        
        return characteristics
    
    def _extract_circumstances_from_text(self, text: str) -> Optional[str]:
        """Extract circumstances from case text"""
        # Look for common circumstance indicators
        circumstances_patterns = [
            r'(?:Found|Discovered|Located):\s*([^\n]+)',
            r'(?:Circumstances|Details):\s*([^\n]+)',
            r'(?:Body was|Remains were)\s*([^\n]+)'
        ]
        
        for pattern in circumstances_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _matches_criteria(self, record: PersonRecord, criteria: SearchCriteria) -> bool:
        """Check if record matches search criteria"""
        if not criteria.physical_characteristics:
            return True
        
        pc_criteria = criteria.physical_characteristics
        pc_record = record.physical_characteristics
        
        # Height check
        if pc_criteria.height_min and pc_record.height_max:
            if pc_record.height_max < pc_criteria.height_min:
                return False
        
        if pc_criteria.height_max and pc_record.height_min:
            if pc_record.height_min > pc_criteria.height_max:
                return False
        
        # Weight check
        if pc_criteria.weight_min and pc_record.weight_max:
            if pc_record.weight_max < pc_criteria.weight_min:
                return False
        
        if pc_criteria.weight_max and pc_record.weight_min:
            if pc_record.weight_min > pc_criteria.weight_max:
                return False
        
        # Race check
        if pc_criteria.race and pc_record.race:
            if pc_criteria.race != pc_record.race:
                return False
        
        # Sex check
        if pc_criteria.sex and pc_record.sex:
            if pc_criteria.sex != pc_record.sex:
                return False
        
        return True