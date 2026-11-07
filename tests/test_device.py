"""Tests for the shared device registry entry."""
from __future__ import annotations

import copy

import pytest

from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar, device_registry as dr

from custom_components.heatit_wifi.const import DOMAIN

from .conftest import DEVICE_ID, WIFI7_STATUS


def _device(hass: HomeAssistant, config_entry) -> dr.DeviceEntry:
    (device,) = dr.async_entries_for_config_entry(
        dr.async_get(hass), config_entry.entry_id
    )
    assert (DOMAIN, DEVICE_ID) in device.identifiers
    return device


async def test_no_room_leaves_the_area_unset(
    hass: HomeAssistant, config_entry
) -> None:
    """WiFi6 firmware reports no room, so Home Assistant asks the user."""
    assert _device(hass, config_entry).area_id is None


@pytest.mark.parametrize("status", [{**copy.deepcopy(WIFI7_STATUS), "room": "Lab"}])
async def test_room_becomes_the_home_assistant_area(
    hass: HomeAssistant, config_entry
) -> None:
    """The MyHeatit room lands in the area field, not in the device name."""
    device = _device(hass, config_entry)
    assert device.name == "Lab thermostat"  # the name from the config entry
    assert ar.async_get(hass).async_get_area(device.area_id).name == "Lab"
