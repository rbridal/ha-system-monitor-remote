"""Config flow for System Monitor Remote."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_DEVICE_ID, CONF_STATE_TOPIC, DEFAULT_DEVICE_ID, DEFAULT_NAME, DOMAIN


class RemoteMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            device_id = str(user_input[CONF_DEVICE_ID]).strip()
            topic = str(user_input.get(CONF_STATE_TOPIC) or "").strip()
            if not topic:
                topic = f"system-monitor/{device_id}/state"
            await self.async_set_unique_id(device_id)
            self._abort_if_unique_id_configured()
            if not device_id or "/" in device_id:
                errors["base"] = "invalid_device"
            else:
                return self.async_create_entry(
                    title=str(user_input.get("name") or device_id),
                    data={CONF_DEVICE_ID: device_id, CONF_STATE_TOPIC: topic},
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name", default=DEFAULT_NAME): str,
                    vol.Required(CONF_DEVICE_ID, default=DEFAULT_DEVICE_ID): str,
                    vol.Optional(CONF_STATE_TOPIC, default="system-monitor/shop-dash/state"): str,
                }
            ),
            errors=errors,
        )
