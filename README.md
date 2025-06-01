# Arvee Integration - Updated for Home Assistant 2025.5.3

## Major Changes

### Key Improvements:
1. **Replaced timezonefinder with tzfpy** - No more compilation requirements
2. **Added fallback to timezonefinderL** - Lightweight alternative if tzfpy isn't available
3. **Modern Home Assistant integration structure** - Fully compliant with HA 2025.5.3
4. **Improved error handling** - Better logging and user feedback
5. **Config flow support** - Modern setup through UI

### Why tzfpy?
- **No compilation required** - Pure Python implementation
- **Faster performance** - Optimized for speed
- **Uses built-in zoneinfo** - Leverages Python 3.9+ standard library
- **Drop-in replacement** - Compatible API with timezonefinder
- **Better maintenance** - Actively maintained and HA-friendly

## Installation Instructions

### Method 1: HACS (Recommended)
1. Add this repository as a custom repository in HACS
2. Install the "Arvee" integration
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration
5. Search for "Arvee" and add it

### Method 2: Manual Installation
1. Copy the entire `custom_components/arvee` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Arvee" and add it

## File Structure
```
custom_components/arvee/
├── __init__.py          # Main integration code
├── config_flow.py       # Configuration flow
├── const.py            # Constants
├── manifest.json       # Integration metadata
├── services.yaml       # Service definitions
└── strings.json        # Localization strings
```

## Dependencies

The integration will automatically install `tzfpy` which has no compilation requirements. If for some reason tzfpy is not available, it will fall back to `timezonefinderL` (lightweight version).

**No more Docker build issues!** The new dependencies are pure Python and install without compilation.

## Services

### `arvee.set_timezone`
Directly set the Home Assistant timezone.

**Parameters:**
- `timezone` (required): IANA timezone name (e.g., "America/New_York")

**Example:**
```yaml
service: arvee.set_timezone
data:
  timezone: "America/Denver"
```

### `arvee.set_geo_timezone`
Set timezone based on GPS coordinates.

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate

**Example:**
```yaml
service: arvee.set_geo_timezone
data:
  latitude: 39.7392
  longitude: -104.9903
```

## Migration from Old Version

### Automatic Migration
The new version is backward compatible with existing automations. Your existing service calls will continue to work without changes.

### What's Changed
1. **Dependencies**: Now uses `tzfpy` instead of `timezonefinder`
2. **Installation**: No more Docker container modifications needed
3. **Performance**: Faster timezone lookups
4. **Setup**: Modern config flow instead of YAML configuration

### Recommended Steps
1. Remove the old integration files
2. Install the new version using HACS or manual method
3. Restart Home Assistant
4. Add the integration through the UI
5. Test your existing automations

## Troubleshooting

### "Cannot Connect" Error
This usually means the timezone finding library isn't available. The integration should automatically install `tzfpy`, but if issues persist:

1. Check Home Assistant logs for specific errors
2. Manually install tzfpy: `pip install tzfpy`
3. Restart Home Assistant

### Service Not Available
If services don't appear:
1. Ensure the integration is properly installed
2. Check that it's enabled in Settings → Devices & Services
3. Restart Home Assistant
4. Check logs for any error messages

### Performance Issues
The new tzfpy library is significantly faster than the original timezonefinder. First-time lookups might take a moment to initialize the timezone database, but subsequent lookups should be very fast.

## Example Automation

```yaml
alias: "Update timezone when location changes"
trigger:
  - platform: state
    entity_id: device_tracker.my_phone
action:
  - service: arvee.set_geo_timezone
    data:
      latitude: "{{ state_attr('device_tracker.my_phone', 'latitude') }}"
      longitude: "{{ state_attr('device_tracker.my_phone', 'longitude') }}"
```

## Support

For issues or questions:
1. Check the Home Assistant logs for error messages
2. Create an issue on the GitHub repository
3. Include your Home Assistant version and full error logs