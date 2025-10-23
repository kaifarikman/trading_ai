from pydantic import BaseModel


class User(BaseModel):
    peer_id: int
    ref_status: bool
    pressed_start: bool
    selected_learning: bool
    selected_signals: bool