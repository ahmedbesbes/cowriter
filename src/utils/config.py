from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class JobConfig:
    topic: str
    model_name: str
    model_temperature: float
    save_to_disk: bool


class ContentConfig(BaseModel):
    is_listicle: bool
    topic: str
    listicle_sections: Optional[list]
