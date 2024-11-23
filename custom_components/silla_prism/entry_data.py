"""Runtime entry data for Silla Prism stored in hass.data."""
from typing import List
from dataclasses import dataclass
from homeassistant.helpers.device_registry import DeviceInfo


@dataclass(slots=True)
class RuntimeEntryData:
    """Store runtime data for esphome config entries."""

    topic: str
    ports: int
    vsensors: bool
    serial: str
    devices: List[DeviceInfo]

