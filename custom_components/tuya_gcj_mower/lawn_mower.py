"""Lawn mower platform for Tuya GCJ devices."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.lawn_mower import (
    LawnMowerActivity,
    LawnMowerEntity,
    LawnMowerEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ACTION_DPCODE,
    DOMAIN,
    STATUS_DPCODE,
    STATUS_TO_ACTIVITY,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya GCJ lawn mower entities."""

    manager = entry.runtime_data.manager

    entities = []

    for device in manager.device_map.values():

        _LOGGER.warning(
            "TUYA DEVICE: %s | category=%s",
            device.name,
            device.category,
        )

        if device.category != "gcj":
            continue

        entities.append(
            TuyaGcjLawnMowerEntity(
                device,
                manager,
            )
        )

    if entities:
        async_add_entities(entities)


class TuyaGcjLawnMowerEntity(LawnMowerEntity):
    """Representation of a Tuya GCJ lawn mower."""

    _attr_name = None

    _attr_supported_features = (
        LawnMowerEntityFeature.START_MOWING
        | LawnMowerEntityFeature.PAUSE
        | LawnMowerEntityFeature.DOCK
    )

    def __init__(self, device: Any, manager: Any) -> None:
        """Initialize the mower."""

        self.device = device
        self.manager = manager

        self._attr_unique_id = f"{DOMAIN}_{device.id}"

        self._attr_device_info = {
            "identifiers": {("tuya", device.id)},
            "name": device.name,
            "manufacturer": "Tuya",
            "model": device.product_name,
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.device.online

    @property
    def activity(self) -> LawnMowerActivity | None:
        """Return mower activity."""

        status = self.device.status.get(STATUS_DPCODE)

        if status is None:
            return None

        return STATUS_TO_ACTIVITY.get(status)

    async def async_start_mowing(self) -> None:
        """Start mowing."""

        command = (
            "ContinueWork"
            if self.device.status.get(STATUS_DPCODE) == "PAUSED"
            else "StartMowing"
        )

        await self._send_command(command)

    async def async_pause(self) -> None:
        """Pause mower."""
        await self._send_command("PauseWork")

    async def async_dock(self) -> None:
        """Return mower to dock."""
        await self._send_command("StartReturnStation")

    async def _send_command(self, command: str) -> None:
        """Send command to device."""

        commands = [
            {
                "code": ACTION_DPCODE,
                "value": command,
            }
        ]

        await self.hass.async_add_executor_job(
            self.manager.send_commands,
            self.device.id,
            commands,
        )