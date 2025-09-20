import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
import re
import time
from urllib.parse import urljoin, quote

from .base import DatabaseInterface
from ..models import PersonRecord, SearchCriteria, PhysicalCharacteristics, Location, Race, Sex


class NamUsInterface(DatabaseInterface):
    """Interface for searching NamUs database"""
    
    def __init__(self):
        self.base_url = "https://www.namus.gov"
        self.search_url = "https://www.namus.gov/UnidentifiedPersons/Search"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_database_name(self) -> str:
        return "NamUs"
    
    def is_available(self) -> bool:
        """Check if NamUs is available"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def search(self, criteria: SearchCriteria) -> List[PersonRecord]:
        """Search NamUs database with given criteria"""
        try:
            # Build search parameters
            params = self._build_search_params(criteria)
            
            # Perform search
            response = self.session.get(self.search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse results
            return self._parse_search_results(response.text)
            
        except Exception as e:
            print(f"Error searching NamUs: {e}")
            return []
    
    def get_record(self, case_id: str) -> Optional[PersonRecord]:
        """Get a specific record by case ID"""
        try:
            # NamUs case URLs are typically: https://www.namus.gov/UnidentifiedPersons/Case#/{case_id}
            case_url = f"{self.base_url}/UnidentifiedPersons/Case#/{case_id}"
            response = self.session.get(case_url, timeout=30)
            response.raise_for_status()
            
            return self._parse_case_details(response.text, case_id, case_url)
            
        except Exception as e:
            print(f"Error getting NamUs record {case_id}: {e}")
            return None
    
    def _build_search_params(self, criteria: SearchCriteria) -> dict:
        """Build search parameters for NamUs API"""
        params = {}
        
        # Physical characteristics
        if criteria.physical_characteristics:
            pc = criteria.physical_characteristics
            
            if pc.sex:
                params['sex'] = pc.sex.value
            
            if pc.race:
                params['race'] = pc.race.value
            
            if pc.height_min:
                params['heightFrom'] = pc.height_min
            if pc.height_max:
                params['heightTo'] = pc.height_max
                
            if pc.weight_min:
                params['weightFrom'] = pc.weight_min
            if pc.weight_max:
                params['weightTo'] = pc.weight_max
                
            if pc.age_min:
                params['ageFrom'] = pc.age_min
            if pc.age_max:
                params['ageTo'] = pc.age_max
        
        # Location
        if criteria.location:
            if criteria.location.state:
                params['state'] = criteria.location.state
            if criteria.location.county:
                params['county'] = criteria.location.county
            if criteria.location.city:
                params['city'] = criteria.location.city
        
        # Date range
        if criteria.date_range_start:
            params['dateFrom'] = criteria.date_range_start.strftime('%m/%d/%Y')
        if criteria.date_range_end:
            params['dateTo'] = criteria.date_range_end.strftime('%m/%d/%Y')
        
        return params
    
    def _parse_search_results(self, html_content: str) -> List[PersonRecord]:
        """Parse search results from NamUs HTML"""
        records = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for case result elements (this is simplified - actual NamUs structure may vary)
            case_elements = soup.find_all('div', class_=['case-result', 'search-result'])
            
            for element in case_elements:
                try:
                    record = self._parse_case_element(element)
                    if record:
                        records.append(record)
                except Exception as e:
                    print(f"Error parsing case element: {e}")
                    continue
            
        except Exception as e:
            print(f"Error parsing search results: {e}")
        
        return records
    
    def _parse_case_element(self, element) -> Optional[PersonRecord]:
        """Parse a single case element from search results"""
        try:
            # Extract case ID
            case_link = element.find('a', href=True)
            if not case_link:
                return None
            
            case_id = self._extract_case_id(case_link['href'])
            case_url = urljoin(self.base_url, case_link['href'])
            
            # Create basic record (detailed info requires individual case lookup)
            record = PersonRecord(
                case_id=case_id,
                database_source="NamUs",
                case_url=case_url,
                last_updated=datetime.now()
            )
            
            # Extract basic info from search result
            text = element.get_text(strip=True)
            
            # Try to extract basic characteristics (this is simplified)
            record.physical_characteristics = self._extract_basic_characteristics(text)
            record.location_found = self._extract_basic_location(text)
            
            return record
            
        except Exception as e:
            print(f"Error parsing case element: {e}")
            return None
    
    def _parse_case_details(self, html_content: str, case_id: str, case_url: str) -> Optional[PersonRecord]:
        """Parse detailed case information"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            record = PersonRecord(
                case_id=case_id,
                database_source="NamUs",
                case_url=case_url,
                last_updated=datetime.now()
            )
            
            # Extract detailed information (implementation depends on actual NamUs structure)
            record.physical_characteristics = self._extract_detailed_characteristics(soup)
            record.location_found = self._extract_detailed_location(soup)
            record.circumstances = self._extract_circumstances(soup)
            record.clothing_description = self._extract_clothing(soup)
            record.photos = self._extract_photos(soup)
            
            return record
            
        except Exception as e:
            print(f"Error parsing case details: {e}")
            return None
    
    def _extract_case_id(self, href: str) -> str:
        """Extract case ID from URL"""
        # Extract numeric case ID from URL
        match = re.search(r'/(\d+)/?$', href)
        return match.group(1) if match else href
    
    def _extract_basic_characteristics(self, text: str) -> PhysicalCharacteristics:
        """Extract basic physical characteristics from text"""
        characteristics = PhysicalCharacteristics()
        
        # Simple regex patterns for extracting info
        height_match = re.search(r'(\d+)\s*(?:feet|ft|\')\s*(\d+)\s*(?:inches|in|\")', text, re.IGNORECASE)
        if height_match:
            feet, inches = int(height_match.group(1)), int(height_match.group(2))
            characteristics.height_min = characteristics.height_max = feet * 12 + inches
        
        weight_match = re.search(r'(\d+)\s*(?:pounds|lbs|lb)', text, re.IGNORECASE)
        if weight_match:
            characteristics.weight_min = characteristics.weight_max = int(weight_match.group(1))
        
        # Race and sex detection (simplified)
        for race in Race:
            if race.value.lower() in text.lower():
                characteristics.race = race
                break
        
        for sex in Sex:
            if sex.value.lower() in text.lower():
                characteristics.sex = sex
                break
        
        return characteristics
    
    def _extract_basic_location(self, text: str) -> Location:
        """Extract basic location from text"""
        location = Location()
        
        # Simple state extraction (would need more sophisticated parsing)
        state_match = re.search(r'\b([A-Z]{2})\b', text)
        if state_match:
            location.state = state_match.group(1)
        
        return location
    
    def _extract_detailed_characteristics(self, soup: BeautifulSoup) -> PhysicalCharacteristics:
        """Extract detailed physical characteristics from case page"""
        # This would need to be implemented based on actual NamUs page structure
        return PhysicalCharacteristics()
    
    def _extract_detailed_location(self, soup: BeautifulSoup) -> Location:
        """Extract detailed location from case page"""
        return Location()
    
    def _extract_circumstances(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract circumstances from case page"""
        return None
    
    def _extract_clothing(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract clothing description from case page"""
        return None
    
    def _extract_photos(self, soup: BeautifulSoup) -> List[str]:
        """Extract photo URLs from case page"""
        return []