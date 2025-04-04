from pydantic import BaseModel, field_validator
from .device import Device
from .effect import Effect
from .binding import Binding


class Store(BaseModel):
    devices: list[Device]
    effects: list[Effect]
    bindings: list[Binding]

    @field_validator("devices")
    def devices_validator(cls, devices):
        if len(devices) != len({device.id for device in devices}):
            raise ValueError("Multiple devices with the same id")
        return devices

    @field_validator("effects")
    def effects_validator(cls, effects):
        if len(effects) != len({effect.id for effect in effects}):
            raise ValueError("Multiple effects with the same id")
        return effects

    @field_validator("bindings")
    def bindings_validator(cls, bindings):
        for binding in bindings:
            if binding.device_id not in {device.id for device in cls.devices}:
                raise ValueError(f"Unknown device: {binding.device_id}")
            if binding.effect_id not in {effect.id for effect in cls.effects}:
                raise ValueError(f"Unknown effect: {binding.effect_id}")
        if len(bindings) != len({binding.device_id for binding in bindings}):
            raise ValueError("Multiple bindings for the same device")
        return bindings

    def update_device(
        self,
        device: Device | dict,
        id: str | None = None,
    ):
        if isinstance(device, dict):
            device = Device.parse_obj(device)
        for i, existing_device in enumerate(self.devices):
            if existing_device.id == id:
                self.devices[i] = device
                return
        self.devices.append(device)

    def update_effect(
        self,
        effect: Effect | dict,
        id: str | None = None,
    ):
        if isinstance(effect, dict):
            effect = Effect.parse_obj(effect)
        for i, existing_effect in enumerate(self.effects):
            if existing_effect.id == id:
                self.effects[i] = effect
                return
        self.effects.append(effect)

    def update_binding(
        self,
        binding: Binding | dict,
        id: str | None = None,
    ):
        if isinstance(binding, dict):
            binding = Binding.parse_obj(binding)
        for i, existing_binding in enumerate(self.bindings):
            if existing_binding.device_id == id:
                self.bindings[i] = binding
                return
        self.bindings.append(binding)
