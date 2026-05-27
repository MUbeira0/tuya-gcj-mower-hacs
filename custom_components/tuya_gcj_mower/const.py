"""Constants for Tuya GCJ lawn mower custom integration."""

from homeassistant.components.lawn_mower import LawnMowerActivity

DOMAIN = "tuya_gcj_mower"

STATUS_DPCODE = "MachineStatus"
ACTION_DPCODE = "MachineControlCmd"

STATUS_TO_ACTIVITY: dict[str, LawnMowerActivity] = {
    "CHARGING": LawnMowerActivity.DOCKED,
    "EMERGENCY": LawnMowerActivity.ERROR,
    "ERROR": LawnMowerActivity.ERROR,
    "LOCKED": LawnMowerActivity.ERROR,
    "MOWING": LawnMowerActivity.MOWING,
    "PARK": LawnMowerActivity.RETURNING,
    "PAUSED": LawnMowerActivity.PAUSED,
    "SELF_TEST": LawnMowerActivity.PAUSED,
    "STANDBY": LawnMowerActivity.PAUSED,
}