from dataclasses import dataclass
from typing import Optional

@dataclass
class Driver:
    Driver_id: Optional[int] = None
    First_name: Optional[str] = None
    Middle_name: Optional[str] = None
    Last_name: Optional[str] = None
    Suffix: Optional[str] = None
    Date_of_birth: Optional[str] = None
    Weight: Optional[float] = None
    Height: Optional[float] = None
    Sex_assigned_at_birth: Optional[str] = None
    Nationality: Optional[str] = None
    Civil_status: Optional[str] = None
    Contact_number: Optional[str] = None
    Blood_type: Optional[str] = None
    House_number: Optional[str] = None
    Street_village: Optional[str] = None
    Barangay: Optional[str] = None
    City_municipality: Optional[str] = None
    Province: Optional[str] = None
    Region: Optional[str] = None
    Zip_code: Optional[str] = None
    License_number: Optional[str] = None
    License_type: Optional[str] = None
    License_status: Optional[str] = None
    Age: Optional[int] = None

    def __str__(self) -> str:
        name = f"{self.First_name or ''} {self.Middle_name or ''} {self.Last_name or ''} {self.Suffix or ''}".strip()
        lines = [
            "\n------------------------------------------------------------------------------------",
            f"Driver ID:      {self.Driver_id or '-'}",
            f"Name:           {name}",
            f"Birthday:       {self.Date_of_birth or '-'}",
            f"Age:            {self.Age if self.Age is not None else '-'}",
            f"Weight:         {self.Weight or '-'} kg",
            f"Height:         {self.Height or '-'} cm",
            f"Sex:            {self.Sex_assigned_at_birth or '-'}",
            f"Nationality:    {self.Nationality or '-'}",
            f"Civil status:   {self.Civil_status or '-'}",
            f"Contact:        {self.Contact_number or '-'}",
            f"Blood type:     {self.Blood_type or '-'}",
            f"Address:        {self.House_number or '-'} {self.Street_village or ''}, {self.Barangay or ''}, {self.City_municipality or ''}, {self.Province or ''}, {self.Region or ''} ({self.Zip_code or ''})",
        ]
        return "\n".join(lines) + "\n"
