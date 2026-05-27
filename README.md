# Tuya GCJ Lawn Mower (HACS)

Custom integration for Home Assistant that adds `lawn_mower` entities for Tuya devices in category `gcj` (for example Parkside OEM Tuya mowers).

This integration reuses your existing Tuya config entry and only adds mower entities and mower services (`start_mowing`, `pause`, `dock`).

## Requirements

- Home Assistant with official Tuya integration already configured and working.
- Device category `gcj` with DPs like:
  - `MachineStatus`
  - `MachineControlCmd`

## Install with HACS

1. Push this repository to your GitHub account.
2. In Home Assistant: HACS -> Integrations -> 3 dots -> Custom repositories.
3. Add your repository URL and select category `Integration`.
4. Install `Tuya GCJ Lawn Mower`.
5. Restart Home Assistant.

## Configure

Add this to your `configuration.yaml`:

```yaml
lawn_mower:
  - platform: tuya_gcj_mower
```

Restart Home Assistant again.

## Supported status mapping

- `CHARGING` -> `docked`
- `MOWING` -> `mowing`
- `PAUSED` -> `paused`
- `PARK` -> `returning`
- `ERROR`, `EMERGENCY`, `LOCKED` -> `error`
- `STANDBY`, `SELF_TEST` -> `paused`

## Commands sent

- Start/Resume -> `MachineControlCmd=StartMowing` or `ContinueWork` when paused
- Pause -> `MachineControlCmd=PauseWork`
- Dock -> `MachineControlCmd=StartReturnStation`

## Notes

- This is intended as a fast path for real-world Tuya/Parkside gcj mowers while upstream support is prepared.
