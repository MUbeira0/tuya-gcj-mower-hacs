from homeassistant import config_entries

DOMAIN = "tuya_gcj_mower"


class TuyaGcjFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        return self.async_create_entry(title="Tuya GCJ Mower", data={})