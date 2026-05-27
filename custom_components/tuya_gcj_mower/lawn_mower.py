async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:

    tuya = hass.data.get("tuya")

    if not tuya:
        _LOGGER.error("Tuya integration not found")
        return

    entities = []

    for entry_data in tuya.values():

        manager = entry_data.manager

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