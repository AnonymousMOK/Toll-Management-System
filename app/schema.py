from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# This is what the ANPR Camera sends to our API
class VehicleArrivalRequest(BaseModel):
    lane_id: int
    captured_plate: str
    e_tag_id: Optional[str] = None  # The tag is optional (only overhead scanners read this)

# This is what our API returns back to the Lane Controller Screen
class ArrivalResponse(BaseModel):
    status: str
    message: str
    passage_id: UUID
    requires_qr: bool
    qr_token: Optional[str] = None