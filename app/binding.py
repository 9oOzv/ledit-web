from pydantic import BaseModel


class Binding(BaseModel):
    id: str
    device_id: str
    effect_id: str
