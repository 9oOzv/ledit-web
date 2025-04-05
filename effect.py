from pydantic import BaseModel, field_validator
import json


max_effect_number = 100
max_effect_parameters = 4


class Effect(BaseModel):
    id: str
    name: str
    number: int
    parameters: list[float]

    @field_validator("number")
    def number_validator(cls, number):
        if number < 1 or number > max_effect_number:
            raise ValueError(f"Unsupported effect number: {number}")
        return number

    @field_validator("parameters", mode="before")
    def parameters_validator(cls, parameters):
        if isinstance(parameters, str):
            parameters = json.loads(parameters)
        if len(parameters) > max_effect_parameters:
            raise ValueError(f"Too many parameters:{len(parameters)}")
        return parameters
