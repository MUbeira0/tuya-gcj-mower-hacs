"""Constants for Tuya GCJ lawn mower."""

from enum import StrEnum

from homeassistant.components.lawn_mower import LawnMowerActivity

TUYA_DOMAIN = "tuya"

STATUS_DPCODE = "MachineStatus"
ACTION_DPCODE = "MachineControlCmd"


class DeviceCategory(StrEnum):
    GCJ = "gcj"


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