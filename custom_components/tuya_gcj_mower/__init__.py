"""Tuya gcj lawn mower custom integration."""

from homeassistant.core import HomeAssistant


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Tuya gcj lawn mower custom integration."""
    del hass, config
    return True
