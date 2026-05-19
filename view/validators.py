from datetime import datetime
from typing import Optional

def read_int(prompt: str, allow_blank: bool = False) -> Optional[int]:
    while True:
        s = input(prompt).strip()
        if s == '':
            if allow_blank:
                return None
            print('Input required')
            continue
        try:
            return int(s)
        except ValueError:
            print('Please enter a valid integer')

def read_float(prompt: str, allow_blank: bool = False) -> Optional[float]:
    while True:
        s = input(prompt).strip()
        if s == '':
            if allow_blank:
                return None
            print('Input required')
            continue
        try:
            return float(s)
        except ValueError:
            print('Please enter a valid number')

def read_date(prompt: str, allow_blank: bool = False) -> Optional[str]:
    while True:
        s = input(prompt).strip()
        if s == '':
            if allow_blank:
                return None
            print('Input required')
            continue
        try:
            # validate basic ISO date
            datetime.strptime(s, '%Y-%m-%d')
            return s
        except ValueError:
            print('Please enter a date in YYYY-MM-DD format')

def read_str(prompt: str, allow_blank: bool = False) -> Optional[str]:
    s = input(prompt).strip()
    if s == '':
        return None if allow_blank else ''
    return s
