from dataclasses import dataclass


@dataclass
class JobConfig:
    topic: str
    model_name: str
    model_temperature: float
    save_to_disk: bool
