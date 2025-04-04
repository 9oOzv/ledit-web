from pydantic import BaseModel, field_validator
from ipaddress import IPv4Address, IPv6Address


class Device(BaseModel):
    id: str
    name: str
    ip: IPv4Address | IPv6Address
    port: int

    @field_validator("port")
    def port_validator(cls, port):
        if port < 0 or port > 65535:
            raise ValueError("Port must be between 0 and 65535")
        return port
