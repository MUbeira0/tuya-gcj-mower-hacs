"""Support for Tuya lawn mowers."""

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
    STATUS_DPCODE,
    STATUS_TO_ACTIVITY,
)

_LOGGER = logging.getLogger(__name__)

_LOGGER.warning("TUYA GCJ MOWER LOADED")


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up Tuya lawn mowers."""

    entries = hass.config_entries.async_entries("tuya")

    _LOGGER.warning("TUYA ENTRIES FOUND: %s", len(entries))

    entities = []

    for entry in entries:

        _LOGGER.warning("TUYA ENTRY: %s", entry.entry_id)

        runtime_data = getattr(entry, "runtime_data", None)

        if runtime_data is None:
            _LOGGER.warning("NO RUNTIME DATA")
            continue

        manager = getattr(runtime_data, "manager", None)

        if manager is None:
            _LOGGER.warning("NO MANAGER")
            continue

        for device in manager.device_map.values():

            _LOGGER.warning(
                "TUYA DEVICE FOUND: %s | category=%s",
                device.name,
                device.category,
            )

            #
            # IMPORTANTE:
            # cambia "gcj" si el log muestra otra categoría
            #
            if device.category != "gcj":
                continue

            entities.append(
                TuyaLawnMowerEntity(
                    device,
                    manager,
                )
            )

    _LOGGER.warning("TOTAL MOWERS FOUND: %s", len(entities))

    if entities:
        async_add_entities(entities)


class TuyaLawnMowerEntity(LawnMowerEntity):
    """Tuya lawn mower device."""

    _attr_name = None

    _attr_supported_features = (
        LawnMowerEntityFeature.START_MOWING
        | LawnMowerEntityFeature.PAUSE
        | LawnMowerEntityFeature.DOCK
    )

    def __init__(
        self,
        device: Any,
        device_manager: Any,
    ) -> None:
        """Initialize Tuya lawn mower."""

        self.device = device
        self.device_manager = device_manager

        self._attr_unique_id = f"tuya_gcj_{device.id}"

        self._attr_device_info = {
            "identifiers": {("tuya", device.id)},
            "name": device.name,
            "manufacturer": "Tuya",
            "model": device.product_name,
        }

        _LOGGER.warning(
            "ENTITY CREATED: %s",
            device.name,
        )

    @property
    def available(self) -> bool:
        """Return availability."""
        return self.device.online

    @property
    def activity(self) -> LawnMowerActivity | None:
        """Return current activity."""

        status = self.device.status.get(STATUS_DPCODE)

        _LOGGER.warning(
            "DEVICE STATUS: %s -> %s",
            self.device.name,
            status,
        )

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

        await self._async_send_command(command)

    async def async_pause(self) -> None:
        """Pause mowing."""
        await self._async_send_command("PauseWork")

    async def async_dock(self) -> None:
        """Return mower to dock."""
        await self._async_send_command("StartReturnStation")

    async def _async_send_command(self, command: str) -> None:
        """Send command."""

        _LOGGER.warning(
            "SENDING COMMAND: %s -> %s",
            self.device.name,
            command,
        )

        commands = [
            {
                "code": ACTION_DPCODE,
                "value": command,
            }
        ]

        await self.hass.async_add_executor_job(
            self.device_manager.send_commands,
            self.device.id,
            commands,
        )