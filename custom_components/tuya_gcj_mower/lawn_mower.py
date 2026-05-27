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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Tuya lawn mowers."""

    _LOGGER.warning("ASYNC_SETUP_ENTRY STARTED")

    tuya_entries = hass.config_entries.async_entries("tuya")

    entities = []

    for tuya_entry in tuya_entries:

        runtime_data = getattr(tuya_entry, "runtime_data", None)

        if runtime_data is None:
            continue

        manager = getattr(runtime_data, "manager", None)

        if manager is None:
            continue

        for device in manager.device_map.values():

            _LOGGER.warning(
                "DEVICE FOUND: %s | category=%s | status=%s",
                device.name,
                device.category,
                device.status,
            )

            #
            # IMPORTANTE:
            # cambia gcj si el log muestra otra categoría
            #
            if device.category != "gcj":
                continue

            entities.append(
                TuyaLawnMowerEntity(
                    device,
                    manager,
                )
            )

    _LOGGER.warning("TOTAL ENTITIES: %s", len(entities))

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
        """Initialize mower."""

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
    def extra_state_attributes(self):
        """Return all Tuya raw attributes."""

        attrs = {}

        try:

            #
            # Status principal
            #
            attrs["raw_status"] = self.device.status

            #
            # Todos los atributos del device
            #
            for key, value in vars(self.device).items():

                try:
                    attrs[f"device_{key}"] = str(value)
                except Exception:
                    attrs[f"device_{key}"] = "ERROR"

            #
            # Todos los status
            #
            if hasattr(self.device, "status"):

                for key, value in self.device.status.items():

                    attrs[f"status_{key}"] = value

            #
            # Status range
            #
            if hasattr(self.device, "status_range"):

                attrs["status_range"] = str(self.device.status_range)

            #
            # Functions
            #
            if hasattr(self.device, "function"):

                attrs["function"] = str(self.device.function)

        except Exception as err:

            attrs["debug_error"] = str(err)

        return attrs

    @property
    def activity(self) -> LawnMowerActivity:
        """Return mower activity."""

        status = self.device.status.get(STATUS_DPCODE)

        _LOGGER.warning(
            "ACTIVITY STATUS: %s -> %s",
            self.device.name,
            status,
        )

        #
        # Si no existe status
        #
        if status is None:

            #
            # Intentar fallback
            #
            for key, value in self.device.status.items():

                _LOGGER.warning(
                    "STATUS KEY: %s = %s",
                    key,
                    value,
                )

                #
                # Buscar enums parecidos
                #
                if isinstance(value, str):

                    mapped = STATUS_TO_ACTIVITY.get(value)

                    if mapped:
                        return mapped

            return LawnMowerActivity.ERROR

        #
        # Estado conocido
        #
        mapped = STATUS_TO_ACTIVITY.get(status)

        if mapped:
            return mapped

        _LOGGER.warning(
            "UNKNOWN STATUS RECEIVED: %s",
            status,
        )

        return LawnMowerActivity.ERROR

    async def async_start_mowing(self) -> None:
        """Start mowing."""

        current_status = self.device.status.get(STATUS_DPCODE)

        _LOGGER.warning(
            "START COMMAND | CURRENT STATUS: %s",
            current_status,
        )

        command = (
            "ContinueWork"
            if current_status == "PAUSED"
            else "StartMowing"
        )

        await self._async_send_command(command)

    async def async_pause(self) -> None:
        """Pause mowing."""

        _LOGGER.warning("PAUSE COMMAND")

        await self._async_send_command("PauseWork")

    async def async_dock(self) -> None:
        """Return to dock."""

        _LOGGER.warning("DOCK COMMAND")

        await self._async_send_command("StartReturnStation")

    async def _async_send_command(self, command: str) -> None:
        """Send command to device."""

        commands = [
            {
                "code": ACTION_DPCODE,
                "value": command,
            }
        ]

        _LOGGER.warning(
            "SENDING COMMAND: %s",
            commands,
        )

        try:

            result = await self.hass.async_add_executor_job(
                self.device_manager.send_commands,
                self.device.id,
                commands,
            )

            _LOGGER.warning(
                "COMMAND RESULT: %s",
                result,
            )

        except Exception as err:

            _LOGGER.exception(
                "COMMAND FAILED: %s",
                err,
            )

            raise