import re
from typing import Optional, Tuple, List


def validate_height_input(height_str: str) -> Optional[int]:
    """
    Validate and convert height input to inches.
    Accepts formats like: 5'8", 5'8, 5 8, 68, 68"
    """
    if not height_str or not height_str.strip():
        return None
    
    height_str = height_str.strip().replace('"', '').replace("'", "'")
    
    # Try feet'inches format
    feet_inches_match = re.match(r"(\d+)'?\s*(\d+)?", height_str)
    if feet_inches_match:
        feet = int(feet_inches_match.group(1))
        inches = int(feet_inches_match.group(2)) if feet_inches_match.group(2) else 0
        
        # Validate reasonable ranges
        if 3 <= feet <= 8 and 0 <= inches <= 11:
            return feet * 12 + inches
    
    # Try plain inches
    inches_match = re.match(r"(\d+)", height_str)
    if inches_match:
        inches = int(inches_match.group(1))
        # Validate reasonable range (36-96 inches = 3'-8')
        if 36 <= inches <= 96:
            return inches
    
    return None


def validate_weight_input(weight_str: str) -> Optional[int]:
    """
    Validate and convert weight input to pounds.
    """
    if not weight_str or not weight_str.strip():
        return None
    
    weight_str = weight_str.strip().lower()
    weight_str = re.sub(r'(lbs?|pounds?)', '', weight_str).strip()
    
    try:
        weight = int(weight_str)
        # Validate reasonable range
        if 50 <= weight <= 500:
            return weight
    except ValueError:
        pass
    
    return None


def validate_age_input(age_str: str) -> Optional[int]:
    """
    Validate age input.
    """
    if not age_str or not age_str.strip():
        return None
    
    try:
        age = int(age_str.strip())
        # Validate reasonable range
        if 0 <= age <= 120:
            return age
    except ValueError:
        pass
    
    return None


def validate_state_code(state_str: str) -> Optional[str]:
    """
    Validate state code and return standardized 2-letter code.
    """
    if not state_str or not state_str.strip():
        return None
    
    state_str = state_str.strip().upper()
    
    # US state codes
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'DC'  # District of Columbia
    }
    
    if state_str in valid_states:
        return state_str
    
    # Try to match full state names to codes
    state_names = {
        'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR',
        'CALIFORNIA': 'CA', 'COLORADO': 'CO', 'CONNECTICUT': 'CT', 'DELAWARE': 'DE',
        'FLORIDA': 'FL', 'GEORGIA': 'GA', 'HAWAII': 'HI', 'IDAHO': 'ID',
        'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA', 'KANSAS': 'KS',
        'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME', 'MARYLAND': 'MD',
        'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS',
        'MISSOURI': 'MO', 'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV',
        'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ', 'NEW MEXICO': 'NM', 'NEW YORK': 'NY',
        'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', 'OHIO': 'OH', 'OKLAHOMA': 'OK',
        'OREGON': 'OR', 'PENNSYLVANIA': 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
        'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN', 'TEXAS': 'TX', 'UTAH': 'UT',
        'VERMONT': 'VT', 'VIRGINIA': 'VA', 'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV',
        'WISCONSIN': 'WI', 'WYOMING': 'WY', 'DISTRICT OF COLUMBIA': 'DC'
    }
    
    return state_names.get(state_str)


def parse_height_range(height_str: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse height range input like "5'6\" - 5'10\"" or "66-70"
    Returns tuple of (min_height, max_height) in inches
    """
    if not height_str or not height_str.strip():
        return None, None
    
    height_str = height_str.strip()
    
    # Check for range indicators
    range_separators = ['-', 'to', 'through', '–', '—']
    range_separator = None
    
    for sep in range_separators:
        if sep in height_str.lower():
            range_separator = sep
            break
    
    if range_separator:
        parts = height_str.lower().split(range_separator)
        if len(parts) == 2:
            min_height = validate_height_input(parts[0].strip())
            max_height = validate_height_input(parts[1].strip())
            return min_height, max_height
    
    # Single value
    height = validate_height_input(height_str)
    return height, height


def parse_weight_range(weight_str: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse weight range input like "150 - 180" or "150-180 lbs"
    Returns tuple of (min_weight, max_weight) in pounds
    """
    if not weight_str or not weight_str.strip():
        return None, None
    
    weight_str = weight_str.strip()
    
    # Check for range indicators
    range_separators = ['-', 'to', 'through', '–', '—']
    range_separator = None
    
    for sep in range_separators:
        if sep in weight_str.lower():
            range_separator = sep
            break
    
    if range_separator:
        parts = weight_str.lower().split(range_separator)
        if len(parts) == 2:
            min_weight = validate_weight_input(parts[0].strip())
            max_weight = validate_weight_input(parts[1].strip())
            return min_weight, max_weight
    
    # Single value
    weight = validate_weight_input(weight_str)
    return weight, weight


def parse_age_range(age_str: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Parse age range input like "25 - 35" or "30"
    Returns tuple of (min_age, max_age)
    """
    if not age_str or not age_str.strip():
        return None, None
    
    age_str = age_str.strip()
    
    # Check for range indicators
    range_separators = ['-', 'to', 'through', '–', '—']
    range_separator = None
    
    for sep in range_separators:
        if sep in age_str.lower():
            range_separator = sep
            break
    
    if range_separator:
        parts = age_str.lower().split(range_separator)
        if len(parts) == 2:
            min_age = validate_age_input(parts[0].strip())
            max_age = validate_age_input(parts[1].strip())
            return min_age, max_age
    
    # Single value
    age = validate_age_input(age_str)
    return age, age


def sanitize_string(input_str: str, max_length: int = 1000) -> str:
    """
    Sanitize string input to prevent injection attacks and limit length.
    """
    if not input_str:
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\';\\]', '', input_str)
    
    # Limit length
    sanitized = sanitized[:max_length]
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    return sanitized


def format_height_display(height_inches: int) -> str:
    """
    Format height in inches for display as feet'inches"
    """
    if not height_inches:
        return "Unknown"
    
    feet = height_inches // 12
    inches = height_inches % 12
    
    if inches == 0:
        return f"{feet}'"
    else:
        return f"{feet}'{inches}\""


def format_confidence_score(score: float) -> str:
    """
    Format confidence score as percentage with appropriate color coding.
    """
    percentage = score * 100
    
    if percentage >= 80:
        return f"HIGH ({percentage:.0f}%)"
    elif percentage >= 60:
        return f"MEDIUM ({percentage:.0f}%)"
    elif percentage >= 40:
        return f"LOW ({percentage:.0f}%)"
    else:
        return f"VERY LOW ({percentage:.0f}%)"


def clean_text_for_matching(text: str) -> str:
    """
    Clean text for better fuzzy matching by normalizing case and removing extra spaces.
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common punctuation that doesn't affect matching
    text = re.sub(r'[.,;:!?()]', '', text)
    
    return text.strip()


def validate_distinguishing_marks(marks: List[str]) -> List[str]:
    """
    Validate and clean distinguishing marks input.
    """
    if not marks:
        return []
    
    cleaned_marks = []
    for mark in marks:
        if mark and mark.strip():
            cleaned_mark = sanitize_string(mark.strip(), max_length=200)
            if cleaned_mark:
                cleaned_marks.append(cleaned_mark)
    
    return cleaned_marks