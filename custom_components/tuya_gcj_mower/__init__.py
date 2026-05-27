"""Tuya GCJ lawn mower custom integration."""

from homeassistant.core import HomeAssistant

PLATFORMS = ["lawn_mower"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up integration."""
    return True


async def async_setup_entry(hass, entry):
    """Set up config entry."""

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload config entry."""

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )