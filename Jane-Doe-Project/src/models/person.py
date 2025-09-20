from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Race(Enum):
    WHITE = "White"
    BLACK_AFRICAN_AMERICAN = "Black/African American"
    HISPANIC_LATINO = "Hispanic/Latino"
    ASIAN = "Asian"
    NATIVE_AMERICAN = "Native American"
    PACIFIC_ISLANDER = "Pacific Islander"
    MULTIRACIAL = "Multiracial"
    UNKNOWN = "Unknown"


class Sex(Enum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"


@dataclass
class PhysicalCharacteristics:
    """Physical characteristics of a person"""
    height_min: Optional[int] = None  # Height in inches
    height_max: Optional[int] = None
    weight_min: Optional[int] = None  # Weight in pounds
    weight_max: Optional[int] = None
    race: Optional[Race] = None
    sex: Optional[Sex] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    distinguishing_marks: List[str] = None  # Tattoos, scars, etc.
    
    def __post_init__(self):
        if self.distinguishing_marks is None:
            self.distinguishing_marks = []


@dataclass
class Location:
    """Location information for a case"""
    state: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    country: str = "United States"
    coordinates: Optional[tuple] = None  # (latitude, longitude)


@dataclass
class PersonRecord:
    """Represents an unidentified person record"""
    case_id: str
    database_source: str  # NamUs, DoeNetwork, etc.
    case_url: Optional[str] = None
    
    # Basic information
    physical_characteristics: PhysicalCharacteristics = None
    location_found: Location = None
    date_found: Optional[datetime] = None
    
    # Case details
    circumstances: Optional[str] = None
    clothing_description: Optional[str] = None
    personal_items: List[str] = None
    
    # Media
    photos: List[str] = None  # URLs to photos
    sketch_url: Optional[str] = None
    
    # Metadata
    last_updated: Optional[datetime] = None
    case_status: str = "Open"
    
    def __post_init__(self):
        if self.physical_characteristics is None:
            self.physical_characteristics = PhysicalCharacteristics()
        if self.location_found is None:
            self.location_found = Location()
        if self.personal_items is None:
            self.personal_items = []
        if self.photos is None:
            self.photos = []


@dataclass
class SearchCriteria:
    """Search criteria for finding matches"""
    physical_characteristics: PhysicalCharacteristics = None
    location: Location = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    databases: List[str] = None  # Which databases to search
    
    def __post_init__(self):
        if self.physical_characteristics is None:
            self.physical_characteristics = PhysicalCharacteristics()
        if self.location is None:
            self.location = Location()
        if self.databases is None:
            self.databases = ["MockDB", "NamUs", "DoeNetwork"]


@dataclass
class SearchResult:
    """A search result with confidence score"""
    person_record: PersonRecord
    confidence_score: float  # 0.0 to 1.0
    match_reasons: List[str]  # Reasons for the match
    
    def __post_init__(self):
        if self.match_reasons is None:
            self.match_reasons = []