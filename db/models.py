from pydantic import BaseModel


class User(BaseModel):
    peer_id: int
    ref_status: bool
