"""Lawn mower platform for Tuya gcj devices."""

from __future__ import annotations

import logging
from typing import Any



from homeassistant.components.lawn_mower import (
    LawnMowerActivity,
    LawnMowerEntity,
    LawnMowerEntityEntityDescription,
    LawnMowerEntityFeature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from typing import Any

from .const import (
    ACTION_DPCODE,
    DOMAIN,
    STATUS_DPCODE,
    STATUS_TO_ACTIVITY,
    TUYA_DISCOVERY_NEW,
    TUYA_DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict[str, Any],
    async_add_entities: AddEntitiesCallback,
    discovery_info: dict[str, Any] | None = None,
) -> None:
    """Set up Tuya gcj mowers from loaded Tuya config entries."""
    del config, discovery_info

    tuya_entries = hass.config_entries.async_entries(TUYA_DOMAIN)
    if not tuya_entries:
        _LOGGER.warning(
            "No Tuya config entries found. Configure Tuya first, then restart Home Assistant."
        )
        return

    known_device_ids: set[str] = set()

    for entry in tuya_entries:
        listener = getattr(entry, "runtime_data", None)
        manager = getattr(listener, "manager", None)

        if manager is None:
            _LOGGER.debug("Skipping Tuya entry %s because runtime manager is missing", entry.entry_id)
            continue

        _register_manager_discovery(
            hass,
            manager,
            known_device_ids,
            async_add_entities,
        )


@callback
def _register_manager_discovery(
    hass: HomeAssistant,
    manager: Any,
    known_device_ids: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Register initial and dynamic discovery for one Tuya manager."""

    @callback

    """Lawn mower platform for Tuya gcj devices."""

    import logging
    from homeassistant.components.lawn_mower import (
        LawnMowerActivity,
        LawnMowerEntity,
        LawnMowerEntityEntityDescription,
        LawnMowerEntityFeature,
    )
    from homeassistant.helpers.dispatcher import async_dispatcher_connect
    from .const import (
        ACTION_DPCODE,
        DOMAIN,
        STATUS_DPCODE,
        STATUS_TO_ACTIVITY,
        TUYA_DISCOVERY_NEW,
        TUYA_DOMAIN,
    )

    _LOGGER = logging.getLogger(__name__)

    async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
        """Set up Tuya gcj mowers from loaded Tuya config entries."""
        tuya_entries = getattr(hass.config_entries, "async_entries", lambda domain: [])(TUYA_DOMAIN)
        if not tuya_entries:
            _LOGGER.warning("No Tuya config entries found. Configure Tuya first, luego reinicia Home Assistant.")
            return

        known_device_ids = set()
        for entry in tuya_entries:
            listener = getattr(entry, "runtime_data", None)
            manager = getattr(listener, "manager", None)
            if manager is None:
                continue
            def async_discover_device(device_ids):
                entities = []
                for device_id in device_ids:
                    if device_id in known_device_ids:
                        continue
                    device = manager.device_map.get(device_id)
                    if device is None or getattr(device, "category", None) != "gcj":
                        continue
                    known_device_ids.add(device_id)
                    entities.append(TuyaGcjLawnMowerEntity(device, manager, LawnMowerEntityEntityDescription(key="")))
                if entities:
                    async_add_entities(entities)
            async_discover_device(list(manager.device_map))
            async_dispatcher_connect(hass, TUYA_DISCOVERY_NEW, async_discover_device)

    class TuyaGcjLawnMowerEntity(LawnMowerEntity):
        _attr_name = None
        _attr_supported_features = (
            LawnMowerEntityFeature.START_MOWING
            | LawnMowerEntityFeature.PAUSE
            | LawnMowerEntityFeature.DOCK
        )

        def __init__(self, device, device_manager, description):
            self._attr_unique_id = f"{DOMAIN}.{device.id}{description.key}"
            self._attr_device_info = {
                "identifiers": {(TUYA_DOMAIN, device.id)},
                "manufacturer": "Tuya",
                "name": getattr(device, "name", None),
                "model": getattr(device, "product_name", None),
                "model_id": getattr(device, "product_id", None),
            }
            self.entity_description = description
            self.device = device
            self.device_manager = device_manager

        @property
        def available(self):
            return getattr(self.device, "online", True)

        @property
        def activity(self):
            value = self.device.status.get(STATUS_DPCODE)
            if value is None:
                return None
            return STATUS_TO_ACTIVITY.get(value)

        async def async_added_to_hass(self):
            self.async_on_remove(
                async_dispatcher_connect(
                    self.hass,
                    f"tuya_entry_update_{self.device.id}",
                    self._handle_state_update,
                )
            )

        async def _handle_state_update(self, updated_status_properties, dp_timestamps):
            if (
                updated_status_properties is None
                or await self._process_device_update(updated_status_properties, dp_timestamps)
            ):
                self.async_write_ha_state()

        async def _process_device_update(self, updated_status_properties, dp_timestamps):
            return STATUS_DPCODE in updated_status_properties if updated_status_properties else True

        async def async_start_mowing(self):
            command = "ContinueWork" if self.device.status.get(STATUS_DPCODE) == "PAUSED" else "StartMowing"
            await self._async_send_commands([{"code": ACTION_DPCODE, "value": command}])

        async def async_pause(self):
            await self._async_send_commands([
                {"code": ACTION_DPCODE, "value": "PauseWork"}
            ])

        async def async_dock(self):
            await self._async_send_commands([
                {"code": ACTION_DPCODE, "value": "StartReturnStation"}
            ])

        async def _async_send_commands(self, commands):
            if not commands:
                return
            await self.hass.async_add_executor_job(
                self.device_manager.send_commands,
                self.device.id,
                commands,
            )
                    dp_timestamps: dict[str, int] | None,
