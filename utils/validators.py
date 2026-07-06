from datetime import date
from typing import Dict, List, Optional

def validate_positive_number(value: float) -> bool:
    try:
        return value > 0
    except (TypeError, ValueError):
        return False

def validate_date_not_future(date_obj: date) -> bool:
    return date_obj <= date.today()

def validate_required_fields(fields: Dict[str, Optional[str]]) -> List[str]:
    missing = []
    for field_name, value in fields.items():
        if not value or not str(value).strip():
            missing.append(field_name)
    return missing