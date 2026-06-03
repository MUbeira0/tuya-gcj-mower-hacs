from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import DeviceQuirk
from tuya_device_handlers.const import DPMode

(
    DeviceQuirk()
    .applies_to(product_id="icw5sal7xfcevsve")

    .add_dpid_enum(
        dpid=101,
        dpcode="MachineStatus",
        dpmode=DPMode.READ,
        enum_range=[
            "STANDBY",
            "CHARGING",
            "MOWING",
            "PAUSED",
            "PARK",
            "UPDATA",
            "FIXED_MOWING",
            "ERROR",
            "SELF_TEST",
            "CHARGING_WITH_TASK_SUSPEND",
            "EMERGENCY",
            "LOCKED",
        ],
    )

    .add_dpid_bitmap(
        dpid=102,
        dpcode="MachineError",
        dpmode=DPMode.READ,
        label_range=[],
    )

    .add_dpid_boolean(
        dpid=104,
        dpcode="MachineRainMode",
        dpmode=DPMode.READ,
    )

    .add_dpid_integer(
        dpid=105,
        dpcode="MachineWorktime",
        dpmode=DPMode.READ,
        unit="h",
        min=1,
        max=99,
        scale=0,
        step=1,
    )

    .add_dpid_enum(
        dpid=115,
        dpcode="MachineControlCmd",
        dpmode=DPMode.WRITE,
        enum_range=[
            "PauseWork",
            "CancelWork",
            "ContinueWork",
            "StartMowing",
            "StartFixedMowing",
            "StartReturnStation",
        ],
    )

    .register(TUYA_QUIRKS_REGISTRY)
)
import logging

logging.getLogger(__name__).warning(
    "GCJ QUIRK REGISTERED FOR icw5sal7xfcevsve"
)