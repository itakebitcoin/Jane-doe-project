from typing import List, Optional
from datetime import datetime
from .base import DatabaseInterface
from ..models import PersonRecord, SearchCriteria, PhysicalCharacteristics, Location, Race, Sex


class MockDatabaseInterface(DatabaseInterface):
    """Mock database interface for testing purposes"""
    
    def __init__(self, name: str = "MockDB"):
        self.name = name
        self.mock_records = self._create_mock_records()
    
    def get_database_name(self) -> str:
        return self.name
    
    def is_available(self) -> bool:
        return True
    
    def search(self, criteria: SearchCriteria) -> List[PersonRecord]:
        """Return mock records that loosely match criteria"""
        matching_records = []
        
        for record in self.mock_records:
            # Simple matching logic for demo purposes
            if self._basic_match(record, criteria):
                matching_records.append(record)
        
        return matching_records[:10]  # Return up to 10 matches
    
    def get_record(self, case_id: str) -> Optional[PersonRecord]:
        """Get a specific mock record"""
        for record in self.mock_records:
            if record.case_id == case_id:
                return record
        return None
    
    def _create_mock_records(self) -> List[PersonRecord]:
        """Create sample mock records for testing"""
        records = []
        
        # Mock Record 1
        records.append(PersonRecord(
            case_id="MOCK-001",
            database_source=self.name,
            case_url="https://example.com/case/001",
            physical_characteristics=PhysicalCharacteristics(
                height_min=64, height_max=66,  # 5'4" - 5'6"
                weight_min=120, weight_max=140,
                race=Race.WHITE,
                sex=Sex.FEMALE,
                age_min=25, age_max=35,
                hair_color="Brown",
                eye_color="Blue",
                distinguishing_marks=["Small scar on left hand", "Tattoo on ankle"]
            ),
            location_found=Location(
                state="CA",
                county="Los Angeles",
                city="Los Angeles"
            ),
            date_found=datetime(2020, 5, 15),
            circumstances="Found in hiking area",
            clothing_description="Blue jeans, white t-shirt",
            last_updated=datetime.now()
        ))
        
        # Mock Record 2
        records.append(PersonRecord(
            case_id="MOCK-002",
            database_source=self.name,
            case_url="https://example.com/case/002",
            physical_characteristics=PhysicalCharacteristics(
                height_min=68, height_max=70,  # 5'8" - 5'10"
                weight_min=160, weight_max=180,
                race=Race.BLACK_AFRICAN_AMERICAN,
                sex=Sex.MALE,
                age_min=30, age_max=45,
                hair_color="Black",
                eye_color="Brown",
                distinguishing_marks=["Tribal tattoo on arm"]
            ),
            location_found=Location(
                state="TX",
                county="Harris",
                city="Houston"
            ),
            date_found=datetime(2019, 8, 22),
            circumstances="Found near highway",
            clothing_description="Dark jeans, leather jacket",
            last_updated=datetime.now()
        ))
        
        # Mock Record 3
        records.append(PersonRecord(
            case_id="MOCK-003",
            database_source=self.name,
            case_url="https://example.com/case/003",
            physical_characteristics=PhysicalCharacteristics(
                height_min=62, height_max=64,  # 5'2" - 5'4"
                weight_min=110, weight_max=130,
                race=Race.HISPANIC_LATINO,
                sex=Sex.FEMALE,
                age_min=20, age_max=30,
                hair_color="Black",
                eye_color="Brown",
                distinguishing_marks=["Birthmark on shoulder"]
            ),
            location_found=Location(
                state="FL",
                county="Miami-Dade",
                city="Miami"
            ),
            date_found=datetime(2021, 12, 3),
            circumstances="Found in park",
            clothing_description="Red dress, sandals",
            last_updated=datetime.now()
        ))
        
        # Mock Record 4 - Broader characteristics
        records.append(PersonRecord(
            case_id="MOCK-004",
            database_source=self.name,
            case_url="https://example.com/case/004",
            physical_characteristics=PhysicalCharacteristics(
                height_min=66, height_max=68,  # 5'6" - 5'8"
                weight_min=140, weight_max=160,
                race=Race.WHITE,
                sex=Sex.FEMALE,
                age_min=35, age_max=50,
                hair_color="Blonde",
                eye_color="Green"
            ),
            location_found=Location(
                state="NY",
                county="Manhattan",
                city="New York"
            ),
            date_found=datetime(2018, 3, 10),
            circumstances="Found in urban area",
            last_updated=datetime.now()
        ))
        
        # Mock Record 5 - Male, different state
        records.append(PersonRecord(
            case_id="MOCK-005",
            database_source=self.name,
            case_url="https://example.com/case/005",
            physical_characteristics=PhysicalCharacteristics(
                height_min=70, height_max=72,  # 5'10" - 6'0"
                weight_min=170, weight_max=190,
                race=Race.WHITE,
                sex=Sex.MALE,
                age_min=40, age_max=55,
                hair_color="Gray",
                eye_color="Blue",
                distinguishing_marks=["Surgery scar on chest"]
            ),
            location_found=Location(
                state="WA",
                county="King",
                city="Seattle"
            ),
            date_found=datetime(2022, 1, 18),
            circumstances="Found in wooded area",
            last_updated=datetime.now()
        ))
        
        return records
    
    def _basic_match(self, record: PersonRecord, criteria: SearchCriteria) -> bool:
        """Basic matching logic for mock data"""
        # If no criteria set, return some records
        if not self._has_any_criteria(criteria):
            return True
        
        # Check location match
        if criteria.location and criteria.location.state:
            if record.location_found and record.location_found.state:
                if record.location_found.state.upper() != criteria.location.state.upper():
                    return False
        
        # Check basic physical characteristics
        if criteria.physical_characteristics:
            pc_crit = criteria.physical_characteristics
            pc_rec = record.physical_characteristics
            
            # Sex match
            if pc_crit.sex and pc_rec.sex:
                if pc_crit.sex != pc_rec.sex:
                    return False
            
            # Race match
            if pc_crit.race and pc_rec.race:
                if pc_crit.race != pc_rec.race:
                    return False
            
            # Height range check (loose matching)
            if pc_crit.height_min or pc_crit.height_max:
                if pc_rec.height_min and pc_rec.height_max:
                    # Check for any overlap
                    crit_min = pc_crit.height_min or 0
                    crit_max = pc_crit.height_max or 100
                    
                    if not (pc_rec.height_max >= crit_min and pc_rec.height_min <= crit_max):
                        # No overlap, but allow some tolerance (4 inches)
                        if (pc_rec.height_min > crit_max + 4) or (pc_rec.height_max < crit_min - 4):
                            return False
        
        return True
    
    def _has_any_criteria(self, criteria: SearchCriteria) -> bool:
        """Check if any search criteria are set"""
        if criteria.location and (criteria.location.state or criteria.location.county or criteria.location.city):
            return True
        
        if criteria.physical_characteristics:
            pc = criteria.physical_characteristics
            return any([
                pc.height_min, pc.height_max, pc.weight_min, pc.weight_max,
                pc.race, pc.sex, pc.age_min, pc.age_max, pc.distinguishing_marks
            ])
        
        return False