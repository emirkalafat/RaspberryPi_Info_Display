# Configuration Documentation

The application configuration is managed via a `config.json` file located in the same directory as the script. This file allows you to customize various aspects of the application without modifying the code.

## File Structure: `config.json`

The file should contain a JSON object with the following sections:

### 1. Crafty Controller (`crafty`)
Settings for connecting to the Crafty Controller API.

> [!NOTE]
> **Authentication Credentials**: The `username` and `password` are NOT stored in this file. They must be set in a `.env` file as `CRAFTY_USERNAME` and `CRAFTY_PASSWORD`.
>
> **2FA Limitation**: If your Crafty account has 2FA enabled, the login will fail. The system will automatically switch to **Public Fallback Mode**. In this mode, it fetches data from the public status endpoint. Basic stats (online count, status) will work, but **player names will not be visible**.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `url` | string | "https://localhost:8443" | The full URL to your Crafty Controller instance. |

### 2. Display (`display`)
Settings for the OLED display behavior.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | integer | 128 | Width of the display in pixels. |
| `height` | integer | 64 | Height of the display in pixels. |
| `i2c_address` | string | "0x3C" | I2C address of the display (hex string). |
| `default_duration` | integer | 5 | Time in seconds to show each screen. |
| `auto_scroll` | boolean | true | Whether to automatically cycle through screens. |
| `stats_only` | boolean | false | If true, only the System Stats screen is shown (Crafty screens skipped). |
| `refresh_interval` | float | 1.0 | Frequency (in seconds) to update the display content. Increase to reduce load. |

### 3. Fonts (`fonts`)
Settings for text rendering.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `path` | string | "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" | Absolute path to the TrueType font file. |
| `size_main` | integer | 10 | Font size for main text. |
| `size_header` | integer | 11 | Font size for headers. |

### 4. GPIO (`gpio`)
Settings for hardware buttons.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `button_pin` | integer/null | null | GPIO pin number (BCM) for the navigation button. Set to `null` if not used. |

### 5. System (`system`)
Internal system settings.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `update_interval` | integer | 10 | How often (in seconds) config data (like Crafty stats) is refreshed. |

### 6. Pages (`pages`)
Control which screens are displayed and their order.

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `enabled` | array | `["system", "crafty", "datetime", "weather", "finance"]` | List of screens to display. Order matters. Available: `system`, `crafty`, `datetime`, `weather`, `finance`. |

### 7. Weather (`weather`)
Settings for the Weather screen (using Open-Meteo).

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `lat` | float | 41.0082 | Latitude of the location. |
| `lon` | float | 28.9784 | Longitude of the location. |
| `city` | string | "Istanbul" | City name to display on screen. |

### 8. Finance (`finance`)
Settings for the Finance screen (using truncgil.com and other sources).

| Key | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `base_currency` | string | "TRY" | The target currency (currently mostly ignored as API defaults to TRY). |
| `currencies` | array | `["USD", "EUR"]` | List of foreign currencies to track against TRY. |
| `show_gold` | boolean | true | Whether to show Gram Gold price. |

## Example `config.json`

```json
{
    "crafty": {
        "url": "https://192.168.1.100:8443"
    },
    "display": {
        "width": 128,
        "height": 64,
        "i2c_address": "0x3C",
        "default_duration": 10,
        "auto_scroll": true,
        "stats_only": false,
        "refresh_interval": 1.0
    },
    "fonts": {
        "path": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "size_main": 10,
        "size_header": 12
    },
    "gpio": {
        "button_pin": 4
    },
    "system": {
        "update_interval": 15
    },
    "pages": {
        "enabled": ["system", "datetime", "weather", "finance"]
    },
    "weather": {
        "lat": 39.9334,
        "lon": 32.8597,
        "city": "Ankara"
    },
    "finance": {
        "base_currency": "TRY",
        "currencies": ["USD", "EUR", "GBP"],
        "show_gold": true
    }
}
```
