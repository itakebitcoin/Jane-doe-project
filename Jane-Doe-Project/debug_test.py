#!/usr/bin/env python3
"""
Debug script to test the search functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models import SearchCriteria, PhysicalCharacteristics, Location, Race, Sex
from src.database import DatabaseManager, MockDatabaseInterface
from src.search import SearchEngine

def test_mock_database():
    """Test the mock database directly"""
    print("=== Testing Mock Database ===")
    
    mock_db = MockDatabaseInterface()
    print(f"Database name: {mock_db.get_database_name()}")
    print(f"Is available: {mock_db.is_available()}")
    
    # Test with basic criteria
    criteria = SearchCriteria()
    criteria.physical_characteristics = PhysicalCharacteristics()
    criteria.physical_characteristics.sex = Sex.FEMALE
    criteria.physical_characteristics.height_min = 64
    criteria.physical_characteristics.height_max = 66
    
    results = mock_db.search(criteria)
    print(f"Mock DB returned {len(results)} results")
    
    for result in results:
        print(f"  - Case {result.case_id}: {result.physical_characteristics.sex.value if result.physical_characteristics.sex else 'Unknown sex'}")

def test_database_manager():
    """Test the database manager"""
    print("\n=== Testing Database Manager ===")
    
    db_manager = DatabaseManager(use_mock_data=True)
    available_dbs = db_manager.get_available_databases()
    print(f"Available databases: {available_dbs}")
    
    # Test search through manager
    criteria = SearchCriteria()
    criteria.physical_characteristics = PhysicalCharacteristics()
    criteria.physical_characteristics.sex = Sex.FEMALE
    
    all_results = db_manager.search_all(criteria)
    print(f"Database manager returned {len(all_results)} total results")

def test_search_engine():
    """Test the search engine"""
    print("\n=== Testing Search Engine ===")
    
    search_engine = SearchEngine()
    available_dbs = search_engine.get_available_databases()
    print(f"Search engine sees databases: {available_dbs}")
    
    # Test search
    criteria = SearchCriteria()
    criteria.physical_characteristics = PhysicalCharacteristics()
    criteria.physical_characteristics.sex = Sex.FEMALE
    criteria.physical_characteristics.height_min = 64
    criteria.physical_characteristics.height_max = 66
    
    search_results = search_engine.search(criteria)
    print(f"Search engine returned {len(search_results)} results")
    
    for result in search_results:
        print(f"  - Case {result.person_record.case_id}: Confidence {result.confidence_score:.2f}")

def test_broad_search():
    """Test with very broad criteria"""
    print("\n=== Testing Broad Search ===")
    
    search_engine = SearchEngine()
    
    # Very broad criteria - should match several records
    criteria = SearchCriteria()
    criteria.physical_characteristics = PhysicalCharacteristics()
    # No specific criteria - should return all mock records
    
    search_results = search_engine.search(criteria)
    print(f"Broad search returned {len(search_results)} results")

if __name__ == "__main__":
    print("Jane Doe Search System - Debug Test")
    print("=" * 50)
    
    try:
        test_mock_database()
        test_database_manager()
        test_search_engine()
        test_broad_search()
        
        print("\n=== Debug Complete ===")
        print("If you see results above, the system is working!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()