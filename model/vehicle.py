from dataclasses import dataclass
from typing import Optional

@dataclass
class Vehicle:
    Vehicle_id: Optional[int] = None
    Engine_number: Optional[str] = None
    Plate_number: Optional[str] = None
    Chassis_number: Optional[str] = None
    Vehicle_type: Optional[str] = None
    Make: Optional[str] = None
    Model: Optional[str] = None
    Year: Optional[int] = None
    Body_type: Optional[str] = None
    Capacity: Optional[int] = None
    Color: Optional[str] = None
    Driver_id: Optional[int] = None

    def __str__(self) -> str:
        return (
            f"Vehicle ID: {self.Vehicle_id or '-'}\n"
            f"Plate: {self.Plate_number or '-'} | Engine: {self.Engine_number or '-'} | Chassis: {self.Chassis_number or '-'}\n"
            f"Type: {self.Vehicle_type or '-'} | Make: {self.Make or '-'} | Model: {self.Model or '-'} | Year: {self.Year or '-'}\n"
        )
