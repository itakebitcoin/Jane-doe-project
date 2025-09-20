#!/usr/bin/env python3
"""
Quick test script for CLI
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def simulate_cli_search():
    """Simulate a CLI search"""
    print("Testing CLI search functionality...")
    
    # Import here to avoid path issues
    from src.models import SearchCriteria, PhysicalCharacteristics, Sex
    from src.search import SearchEngine
    
    # Create search engine
    search_engine = SearchEngine()
    
    # Create criteria similar to what CLI would create
    criteria = SearchCriteria()
    criteria.physical_characteristics = PhysicalCharacteristics()
    criteria.physical_characteristics.sex = Sex.FEMALE
    criteria.physical_characteristics.height_min = 64  # 5'4"
    criteria.physical_characteristics.height_max = 68  # 5'8"
    
    print(f"Searching with criteria:")
    print(f"  Sex: {criteria.physical_characteristics.sex.value}")
    print(f"  Height: {criteria.physical_characteristics.height_min}-{criteria.physical_characteristics.height_max} inches")
    print(f"  Databases to search: {criteria.databases}")
    
    # Perform search
    results = search_engine.search(criteria)
    
    print(f"\nSearch Results: {len(results)} matches found")
    
    for i, result in enumerate(results, 1):
        record = result.person_record
        confidence = result.confidence_score
        print(f"\nMatch #{i} - Confidence: {confidence:.1%}")
        print(f"  Case ID: {record.case_id}")
        print(f"  Database: {record.database_source}")
        if record.physical_characteristics.height_min:
            print(f"  Height: {record.physical_characteristics.height_min}-{record.physical_characteristics.height_max} inches")
        if record.physical_characteristics.sex:
            print(f"  Sex: {record.physical_characteristics.sex.value}")
        print(f"  Match reasons: {', '.join(result.match_reasons)}")

if __name__ == "__main__":
    simulate_cli_search()