from typing import List, Tuple
from fuzzywuzzy import fuzz
from ..models import PersonRecord, SearchCriteria, SearchResult, PhysicalCharacteristics, Location


class MatchingEngine:
    """Engine for matching search criteria to person records"""
    
    def __init__(self):
        self.weight_config = {
            'height': 0.2,
            'weight': 0.2,
            'race': 0.15,
            'sex': 0.15,
            'age': 0.15,
            'location': 0.1,
            'distinguishing_marks': 0.05
        }
    
    def calculate_match_score(self, record: PersonRecord, criteria: SearchCriteria) -> Tuple[float, List[str]]:
        """Calculate match score between 0.0 and 1.0"""
        scores = {}
        match_reasons = []
        
        # Physical characteristics matching
        if criteria.physical_characteristics:
            pc_score, pc_reasons = self._match_physical_characteristics(
                record.physical_characteristics, criteria.physical_characteristics
            )
            scores.update(pc_score)
            match_reasons.extend(pc_reasons)
        
        # Location matching
        if criteria.location:
            location_score, location_reasons = self._match_location(
                record.location_found, criteria.location
            )
            scores['location'] = location_score
            match_reasons.extend(location_reasons)
        
        # Calculate weighted average
        total_score = 0.0
        total_weight = 0.0
        
        for category, score in scores.items():
            if score > 0:  # Only include categories with valid matches
                weight = self.weight_config.get(category, 0.1)
                total_score += score * weight
                total_weight += weight
        
        # Normalize by actual weights used
        final_score = total_score / total_weight if total_weight > 0 else 0.0
        
        return final_score, match_reasons
    
    def _match_physical_characteristics(self, record_pc: PhysicalCharacteristics, 
                                       criteria_pc: PhysicalCharacteristics) -> Tuple[dict, List[str]]:
        """Match physical characteristics"""
        scores = {}
        reasons = []
        
        # Height matching
        if criteria_pc.height_min or criteria_pc.height_max:
            height_score = self._match_height_range(record_pc, criteria_pc)
            if height_score > 0:
                scores['height'] = height_score
                reasons.append(f"Height match (score: {height_score:.2f})")
        
        # Weight matching
        if criteria_pc.weight_min or criteria_pc.weight_max:
            weight_score = self._match_weight_range(record_pc, criteria_pc)
            if weight_score > 0:
                scores['weight'] = weight_score
                reasons.append(f"Weight match (score: {weight_score:.2f})")
        
        # Race matching
        if criteria_pc.race and record_pc.race:
            if criteria_pc.race == record_pc.race:
                scores['race'] = 1.0
                reasons.append("Exact race match")
            else:
                # Partial matching for related races
                race_score = self._fuzzy_race_match(criteria_pc.race, record_pc.race)
                if race_score > 0.5:
                    scores['race'] = race_score
                    reasons.append(f"Similar race match (score: {race_score:.2f})")
        
        # Sex matching
        if criteria_pc.sex and record_pc.sex:
            if criteria_pc.sex == record_pc.sex:
                scores['sex'] = 1.0
                reasons.append("Exact sex match")
        
        # Age matching
        if criteria_pc.age_min or criteria_pc.age_max:
            age_score = self._match_age_range(record_pc, criteria_pc)
            if age_score > 0:
                scores['age'] = age_score
                reasons.append(f"Age match (score: {age_score:.2f})")
        
        # Distinguishing marks
        if criteria_pc.distinguishing_marks and record_pc.distinguishing_marks:
            marks_score = self._match_distinguishing_marks(
                record_pc.distinguishing_marks, criteria_pc.distinguishing_marks
            )
            if marks_score > 0:
                scores['distinguishing_marks'] = marks_score
                reasons.append(f"Distinguishing marks match (score: {marks_score:.2f})")
        
        return scores, reasons
    
    def _match_height_range(self, record_pc: PhysicalCharacteristics, 
                           criteria_pc: PhysicalCharacteristics) -> float:
        """Match height ranges with tolerance"""
        record_height = self._get_height_value(record_pc)
        if not record_height:
            return 0.0
        
        criteria_min = criteria_pc.height_min or 0
        criteria_max = criteria_pc.height_max or 100  # 100 inches = ~8 feet
        
        # Perfect match
        if criteria_min <= record_height <= criteria_max:
            return 1.0
        
        # Calculate distance from range
        if record_height < criteria_min:
            distance = criteria_min - record_height
        else:
            distance = record_height - criteria_max
        
        # Allow 3-inch tolerance with declining score
        tolerance = 3
        if distance <= tolerance:
            return max(0.0, 1.0 - (distance / tolerance))
        
        return 0.0
    
    def _match_weight_range(self, record_pc: PhysicalCharacteristics, 
                           criteria_pc: PhysicalCharacteristics) -> float:
        """Match weight ranges with tolerance"""
        record_weight = self._get_weight_value(record_pc)
        if not record_weight:
            return 0.0
        
        criteria_min = criteria_pc.weight_min or 0
        criteria_max = criteria_pc.weight_max or 500
        
        # Perfect match
        if criteria_min <= record_weight <= criteria_max:
            return 1.0
        
        # Calculate distance from range
        if record_weight < criteria_min:
            distance = criteria_min - record_weight
        else:
            distance = record_weight - criteria_max
        
        # Allow 20-pound tolerance with declining score
        tolerance = 20
        if distance <= tolerance:
            return max(0.0, 1.0 - (distance / tolerance))
        
        return 0.0
    
    def _match_age_range(self, record_pc: PhysicalCharacteristics, 
                        criteria_pc: PhysicalCharacteristics) -> float:
        """Match age ranges with tolerance"""
        record_age = self._get_age_value(record_pc)
        if not record_age:
            return 0.0
        
        criteria_min = criteria_pc.age_min or 0
        criteria_max = criteria_pc.age_max or 120
        
        # Perfect match
        if criteria_min <= record_age <= criteria_max:
            return 1.0
        
        # Calculate distance from range
        if record_age < criteria_min:
            distance = criteria_min - record_age
        else:
            distance = record_age - criteria_max
        
        # Allow 5-year tolerance with declining score
        tolerance = 5
        if distance <= tolerance:
            return max(0.0, 1.0 - (distance / tolerance))
        
        return 0.0
    
    def _match_location(self, record_location: Location, criteria_location: Location) -> Tuple[float, List[str]]:
        """Match location with fuzzy string matching"""
        if not record_location or not criteria_location:
            return 0.0, []
        
        scores = []
        reasons = []
        
        # State matching (most important)
        if criteria_location.state and record_location.state:
            if criteria_location.state.upper() == record_location.state.upper():
                scores.append(1.0)
                reasons.append("Exact state match")
            else:
                # Fuzzy match for state names and abbreviations
                state_score = fuzz.ratio(criteria_location.state.lower(), 
                                       record_location.state.lower()) / 100.0
                if state_score > 0.3:  # Lower threshold for state abbreviations
                    scores.append(state_score)
                    reasons.append(f"Similar state match (score: {state_score:.2f})")
        
        # County matching
        if criteria_location.county and record_location.county:
            county_score = fuzz.ratio(criteria_location.county.lower(), 
                                    record_location.county.lower()) / 100.0
            if county_score > 0.7:
                scores.append(county_score * 0.7)  # Weight county less than state
                reasons.append(f"County match (score: {county_score:.2f})")
        
        # City matching
        if criteria_location.city and record_location.city:
            city_score = fuzz.ratio(criteria_location.city.lower(), 
                                  record_location.city.lower()) / 100.0
            if city_score > 0.7:
                scores.append(city_score * 0.5)  # Weight city less than county
                reasons.append(f"City match (score: {city_score:.2f})")
        
        # Return average of all location scores
        final_score = sum(scores) / len(scores) if scores else 0.0
        return final_score, reasons
    
    def _match_distinguishing_marks(self, record_marks: List[str], criteria_marks: List[str]) -> float:
        """Match distinguishing marks using fuzzy string matching"""
        if not record_marks or not criteria_marks:
            return 0.0
        
        best_scores = []
        
        for criteria_mark in criteria_marks:
            mark_scores = []
            for record_mark in record_marks:
                score = fuzz.partial_ratio(criteria_mark.lower(), record_mark.lower()) / 100.0
                mark_scores.append(score)
            
            if mark_scores:
                best_scores.append(max(mark_scores))
        
        return sum(best_scores) / len(best_scores) if best_scores else 0.0
    
    def _fuzzy_race_match(self, race1, race2) -> float:
        """Fuzzy matching for race categories"""
        # This could be enhanced with more sophisticated race similarity logic
        race1_str = race1.value if hasattr(race1, 'value') else str(race1)
        race2_str = race2.value if hasattr(race2, 'value') else str(race2)
        
        return fuzz.ratio(race1_str.lower(), race2_str.lower()) / 100.0
    
    def _get_height_value(self, pc: PhysicalCharacteristics) -> float:
        """Get single height value from characteristics"""
        if pc.height_min and pc.height_max:
            return (pc.height_min + pc.height_max) / 2
        return pc.height_min or pc.height_max
    
    def _get_weight_value(self, pc: PhysicalCharacteristics) -> float:
        """Get single weight value from characteristics"""
        if pc.weight_min and pc.weight_max:
            return (pc.weight_min + pc.weight_max) / 2
        return pc.weight_min or pc.weight_max
    
    def _get_age_value(self, pc: PhysicalCharacteristics) -> float:
        """Get single age value from characteristics"""
        if pc.age_min and pc.age_max:
            return (pc.age_min + pc.age_max) / 2
        return pc.age_min or pc.age_max