"""Sensors for System Monitor Remote."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import RemoteMonitorCoordinator


def _device(entry: ConfigEntry) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.title,
        manufacturer="DELROBCO",
        model="System Monitor",
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RemoteMonitorCoordinator = hass.data[DOMAIN][entry.entry_id]
    coordinator.async_add_sensors = async_add_entities
    async_add_entities(
        [
            ValueSensor(coordinator, entry, "disk_usage", "Disk usage /", PERCENTAGE),
            ValueSensor(coordinator, entry, "memory_usage", "Memory usage", PERCENTAGE),
            ValueSensor(coordinator, entry, "processor_use", "Processor use", PERCENTAGE),
            TempSensor(coordinator, entry),
            ValueSensor(coordinator, entry, "load_1_min", "Load (1 min)", None),
            ValueSensor(coordinator, entry, "load_5_min", "Load (5 min)", None),
            ValueSensor(coordinator, entry, "load_15_min", "Load (15 min)", None),
            UptimeSensor(coordinator, entry),
        ]
    )
    if coordinator.data:
        coordinator._ensure_dynamic(coordinator.data)


class _Base(CoordinatorEntity[RemoteMonitorCoordinator], SensorEntity):
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: RemoteMonitorCoordinator, entry: ConfigEntry, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"{entry.unique_id}_{key}"
        self._attr_suggested_object_id = key
        self._attr_device_info = _device(entry)


class ValueSensor(_Base):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, key: str, name: str, unit: str | None) -> None:
        super().__init__(coordinator, entry, key, name)
        self._key = key
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> Any:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._key)


class TempSensor(_Base):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator, entry, "processor_temperature", "Processor temperature")

    @property
    def native_value(self) -> Any:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("processor_temperature_c")


class UptimeSensor(_Base):
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator, entry, "uptime", "Uptime")

    @property
    def native_value(self) -> Any:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("boot_time")


class Ipv4Sensor(_Base):
    def __init__(self, coordinator, entry, iface: str) -> None:
        super().__init__(coordinator, entry, f"ipv4_address_{iface}", f"IPv4 address {iface}")
        self._iface = iface

    @property
    def native_value(self) -> Any:
        if self.coordinator.data is None:
            return None
        return (self.coordinator.data.get("ipv4") or {}).get(self._iface)


class FanSensor(_Base):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "rpm"

    def __init__(self, coordinator, entry, fan: str) -> None:
        super().__init__(coordinator, entry, f"{fan}_fan_speed", f"{fan} fan speed")
        self._fan = fan

    @property
    def native_value(self) -> Any:
        if self.coordinator.data is None:
            return None
        return (self.coordinator.data.get("fans") or {}).get(self._fan)
