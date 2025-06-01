"""
Home Assistant Arvee Integration - Updated for HA 2025.5.3
A component designed for mobile installations (e.g. RVs, etc.)
"""
import logging
import voluptuous as vol
from typing import Any, Dict

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

# Use tzfpy instead of timezonefinder for better compatibility
try:
    from tzfpy import get_tz
    TZFPY_AVAILABLE = True
except ImportError:
    TZFPY_AVAILABLE = False

# Fallback to timezonefinderL if tzfpy is not available
if not TZFPY_AVAILABLE:
    try:
        from timezonefinderL import TimezoneFinder
        tf = TimezoneFinder()
        TIMEZONEFINDER_AVAILABLE = True
    except ImportError:
        TIMEZONEFINDER_AVAILABLE = False
else:
    TIMEZONEFINDER_AVAILABLE = False

_LOGGER = logging.getLogger(__name__)

DOMAIN = "arvee"
VERSION = "2.0.0"

# Service names
SERVICE_SET_TIMEZONE = "set_timezone"
SERVICE_SET_GEO_TIMEZONE = "set_geo_timezone"

# Service schemas
SET_TIMEZONE_SCHEMA = vol.Schema({
    vol.Required("timezone"): cv.string,
})

SET_GEO_TIMEZONE_SCHEMA = vol.Schema({
    vol.Required(CONF_LATITUDE): cv.latitude,
    vol.Required(CONF_LONGITUDE): cv.longitude,
})


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Arvee component."""
    
    # Check if we have timezone lookup capability
    if not TZFPY_AVAILABLE and not TIMEZONEFINDER_AVAILABLE:
        _LOGGER.error(
            "Neither tzfpy nor timezonefinderL is available. "
            "Please install one of these packages: pip install tzfpy or pip install timezonefinderL"
        )
        return False
    
    if TZFPY_AVAILABLE:
        _LOGGER.info("Using tzfpy for timezone lookups")
    else:
        _LOGGER.info("Using timezonefinderL for timezone lookups")

    async def async_set_timezone(call: ServiceCall) -> None:
        """Service to set timezone directly."""
        timezone = call.data.get("timezone")
        
        try:
            # Update Home Assistant's timezone
            await hass.config.async_update(time_zone=timezone)
            _LOGGER.info(f"Timezone updated to: {timezone}")
        except Exception as err:
            _LOGGER.error(f"Error setting timezone to {timezone}: {err}")
            raise HomeAssistantError(f"Failed to set timezone: {err}")

    async def async_set_geo_timezone(call: ServiceCall) -> None:
        """Service to set timezone based on coordinates."""
        latitude = call.data.get(CONF_LATITUDE)
        longitude = call.data.get(CONF_LONGITUDE)
        
        try:
            # Get timezone from coordinates
            if TZFPY_AVAILABLE:
                timezone = await hass.async_add_executor_job(
                    get_tz, longitude, latitude
                )
            else:
                timezone = await hass.async_add_executor_job(
                    tf.timezone_at, lat=latitude, lng=longitude
                )
            
            if timezone is None:
                raise HomeAssistantError(
                    f"Could not determine timezone for coordinates: {latitude}, {longitude}"
                )
            
            # Update Home Assistant's timezone
            await hass.config.async_update(time_zone=timezone)
            _LOGGER.info(f"Timezone updated to: {timezone} for coordinates: {latitude}, {longitude}")
            
        except Exception as err:
            _LOGGER.error(
                f"Error setting timezone for coordinates {latitude}, {longitude}: {err}"
            )
            raise HomeAssistantError(f"Failed to set geo timezone: {err}")

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_TIMEZONE,
        async_set_timezone,
        schema=SET_TIMEZONE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_GEO_TIMEZONE,
        async_set_geo_timezone,
        schema=SET_GEO_TIMEZONE_SCHEMA,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Arvee from a config entry."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Arvee config entry."""
    return True