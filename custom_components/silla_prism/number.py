"""Contains numbers configurations for Prism wallbox integration."""

import logging

from homeassistant.components import mqtt
from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.components.number.const import NumberDeviceClass, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .domain_data import DomainData
from .entity import PrismBaseEntity
from .entry_data import RuntimeEntryData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add entities for passed config_entry in HA."""
    entry_data: RuntimeEntryData = DomainData.get(hass).get_entry_data(entry)
    _LOGGER.debug("async_setup_entry for numbers: %s", entry_data)
    selects = [
        PrismNumber(hass, entry_data.topic, description) for description in NUMBERS
    ]
    async_add_entities(selects)


class PrismNumber(PrismBaseEntity, NumberEntity):
    """Prism number entity."""

    entity_description: NumberEntityDescription

    def __init__(
        self, hass: HomeAssistant, base_topic: str, description: EntityDescription
    ) -> None:
        """Init Prism select."""
        super().__init__(base_topic, description)
        self._hass: HomeAssistant = hass

    @property
    def native_value(self) -> float | None:
        """Return the entity value to represent the entity state."""
        return 6

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("set number value %f", value)
        await mqtt.async_publish(self._hass, self._topic, int(value))


NUMBERS: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key="set_current_user",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.CURRENT,
        native_min_value=6,
        native_max_value=16,
        mode=NumberMode.BOX,
        has_entity_name=True,
        translation_key="set_current_user",
    ),
    NumberEntityDescription(
        key="set_current_limit",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.CURRENT,
        native_min_value=6,
        native_max_value=16,
        has_entity_name=True,
        translation_key="set_current_limit",
    ),
)
