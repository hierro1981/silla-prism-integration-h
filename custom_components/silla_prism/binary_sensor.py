"""Contains numbers configurations for Prism wallbox integration."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
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
    _LOGGER.debug("async_setup_entry for binary sensors: %s", entry_data)
    binsens = [
        PrismBinarySensor(entry_data.topic, description)
        for description in BINARYSENSORS
    ]
    async_add_entities(binsens)


class PrismBinarySensor(PrismBaseEntity, BinarySensorEntity):
    """Prism number entity."""

    entity_description: BinarySensorEntityDescription

    def __init__(self, base_topic: str, description: EntityDescription) -> None:
        """Init Prism select."""
        super().__init__(base_topic, description)
        self._attr_is_on = False
        self._unsubscribe = None

    async def _subscribe_topic(self):
        """Subscribe to mqtt topic."""
        _LOGGER.debug("_subscribe_topic: %s", self._topic)
        self._unsubscribe = await self.hass.components.mqtt.async_subscribe(
            self._topic, self.message_received
        )

    async def _unsubscribe_topic(self):
        """Unsubscribe to mqtt topic."""
        _LOGGER.debug("_unsubscribe_topic: %s", self._topic)
        if self._unsubscribe is not None:
            await self._unsubscribe()

    def _message_received(self, msg) -> None:
        """Update the sensor with the most recent event."""
        _LOGGER.debug(
            "PrismBinarySensor._message_received %s %s", self._topic, msg.payload
        )
        self.schedule_expiration_callback()

        if self._topic == "input/touch":
            # Handle input touch button
            self._attr_is_on = msg.payload != "0"
            self.schedule_update_ha_state()
        else:
            # Handle online presence
            if not self._attr_is_on:
                self._attr_is_on = True
                self.schedule_update_ha_state()

    def message_received(self, msg) -> None:
        """Update the sensor with the most recent event."""
        self.hass.loop.call_soon_threadsafe(self._message_received, msg)

    async def async_added_to_hass(self) -> None:
        """Subscribe to mqtt."""
        _LOGGER.debug("async_added_to_hass")
        await self._subscribe_topic()

    async def async_will_remove_from_hass(self) -> None:
        """Unsubscribe from mqtt."""
        _LOGGER.debug("async_will_remove_from_hass")
        await super().async_will_remove_from_hass()
        self.cleanup_expiration_trigger()
        if self._unsubscribe is not None:
            await self._unsubscribe_topic()


BINARYSENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="energy_data/power_grid",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        has_entity_name=True,
        translation_key="online",
    ),
)


# BinarySensorEntityDescription(
#    key="input/touch",
#    entity_category=EntityCategory.CONFIG,
#    device_class=BinarySensorDeviceClass.MOTION,
#    has_entity_name=True,
#    translation_key="input_touch",
# ),""",
