# Arduino Sine Wave Wobble Generator

A comprehensive Arduino program that generates dynamic sine wave wobble patterns suitable for display on Arduino-powered screens. The wobble effect creates visually appealing wave patterns with adjustable amplitude and frequency parameters.

## Features

- **Dynamic Sine Wave Generation**: Creates smooth sine wave patterns with wobble effects
- **Adjustable Parameters**: Real-time control of amplitude, frequency, and animation speed
- **Multi-Display Support**: Compatible with OLED, TFT, and custom display libraries
- **Optimized Performance**: Efficient calculations suitable for Arduino's limited resources
- **Visual Enhancements**: Optional center lines, amplitude markers, and grid overlays
- **Real-time Animation**: Smooth animation with customizable frame rates
- **Serial Debug Output**: Comprehensive debugging and coordinate output

## Files Description

### Core Files

1. **`sine_wave_wobble.ino`** - Main comprehensive Arduino sketch with full functionality
2. **`wobble_config.h`** - Configuration header for easy customization
3. **`simple_wobble_demo.ino`** - Simplified demo that works out-of-the-box with Serial Monitor
4. **`display_examples`** - Example implementations for different display types

## Quick Start

### Option 1: Simple Demo (Recommended for Testing)

1. Upload `simple_wobble_demo.ino` to your Arduino
2. Open Serial Monitor at 9600 baud
3. Watch the ASCII wobble pattern animate in real-time

### Option 2: Full Implementation

1. Copy `sine_wave_wobble.ino` and `wobble_config.h` to your Arduino project
2. Modify `wobble_config.h` for your specific display type
3. Uncomment appropriate display library includes
4. Upload and enjoy the wobble on your screen!

## Supported Display Types

### OLED Displays (SSD1306)
```cpp
#define USE_SSD1306_OLED
#include <Adafruit_SSD1306.h>
```

### TFT Displays (ST7735/ST7789)
```cpp
#define USE_ST7735_TFT
#include <Adafruit_ST7735.h>
```

### Custom Displays
Implement the display interface functions:
- `initializeDisplay()`
- `clearDisplay()`
- `drawPixel(x, y)`
- `drawLine(x0, y0, x1, y1)`
- `updateDisplay()`

## Configuration Parameters

### Wobble Parameters
- **Amplitude**: Wave height (0.1 to 1.0) - Controls how tall the waves are
- **Frequency**: Wave density (0.1 to 5.0) - Controls how many waves fit on screen
- **Phase Speed**: Animation speed (0.01 to 0.5) - Controls how fast the waves move

### Display Settings
- **Screen Dimensions**: Adjust `SCREEN_WIDTH` and `SCREEN_HEIGHT`
- **Pin Configuration**: Set up CS, DC, RST pins for your display
- **Color Settings**: Configure colors for your display type

### Performance Options
- **Fast Sine**: Use approximation for better performance
- **Calculation Step**: Skip pixels for faster rendering
- **Frame Rate**: Adjust delay for desired animation speed

## Real-time Control

Connect potentiometers to analog pins for real-time parameter adjustment:

```cpp
#define ENABLE_AMPLITUDE_CONTROL  true
#define AMPLITUDE_CONTROL_PIN     A0

#define ENABLE_FREQUENCY_CONTROL  true  
#define FREQUENCY_CONTROL_PIN     A1

#define ENABLE_SPEED_CONTROL      true
#define SPEED_CONTROL_PIN         A2
```

## Hardware Requirements

### Minimum Requirements
- Arduino Uno, Nano, or compatible board
- Any supported display (OLED/TFT recommended)
- Connecting wires

### Optional Components
- Potentiometers (3x 10kΩ) for real-time control
- Breadboard for prototyping
- External power supply for larger displays

## Wiring Examples

### SSD1306 OLED (I2C)
```
Arduino -> OLED
VCC     -> 3.3V or 5V
GND     -> GND
SDA     -> A4 (Uno) / SDA pin
SCL     -> A5 (Uno) / SCL pin
```

### ST7735 TFT (SPI)
```
Arduino -> TFT
VCC     -> 3.3V
GND     -> GND
CS      -> Pin 10
RST     -> Pin 9
DC      -> Pin 8
SDA     -> Pin 11 (MOSI)
SCK     -> Pin 13 (SCK)
```

## Customization Examples

### Basic Wobble Pattern
```cpp
wobble.amplitude = 0.7;     // 70% screen height
wobble.frequency = 2.0;     // 2 waves across screen
wobble.phaseIncrement = 0.1; // Moderate animation speed
```

### High-Frequency Wobble
```cpp
wobble.amplitude = 0.4;     // Smaller waves
wobble.frequency = 4.0;     // 4 waves across screen
wobble.phaseIncrement = 0.2; // Faster animation
```

### Slow, Large Wobble
```cpp
wobble.amplitude = 0.9;     // Large waves
wobble.frequency = 0.8;     // Less than 1 wave across screen
wobble.phaseIncrement = 0.05; // Slow animation
```

## Advanced Features

### Multiple Wave Layers
Add multiple sine waves with different parameters for complex patterns:

```cpp
// Primary wave
int y1 = calculateSineY(x, primaryWobble);

// Secondary wave  
int y2 = calculateSineY(x, secondaryWobble);

// Combine waves
int finalY = (y1 + y2) / 2;
```

### Color Animation (for color displays)
```cpp
// Cycle through colors based on wave position
uint16_t waveColor = HSVtoRGB(y * 360 / SCREEN_HEIGHT, 255, 255);
display.drawPixel(x, y, waveColor);
```

### Interactive Control
```cpp
// Button input for parameter switching
if (digitalRead(BUTTON_PIN) == LOW) {
  currentMode = (currentMode + 1) % NUM_MODES;
  loadPreset(currentMode);
}
```

## Troubleshooting

### Common Issues

1. **Display not working**
   - Check wiring connections
   - Verify display library is installed
   - Confirm correct display address/pins

2. **Choppy animation**
   - Increase delay in main loop
   - Reduce screen resolution
   - Enable fast sine approximation

3. **Memory issues**
   - Reduce buffer sizes
   - Use smaller data types
   - Disable debug output

4. **Compilation errors**
   - Install required display libraries
   - Check include paths
   - Verify board selection

### Performance Tips

- Use `fastSin()` instead of `sin()` for better performance
- Reduce `SCREEN_WIDTH` for faster calculations
- Increase `CALCULATION_STEP` to skip pixels
- Lower frame rate with larger delay values

## Library Dependencies

### Required Libraries (install via Arduino Library Manager)

For OLED displays:
- Adafruit SSD1306
- Adafruit GFX Library

For TFT displays:
- Adafruit ST7735 and ST7789 Library
- Adafruit GFX Library

### Optional Libraries
- FastLED (for LED strip displays)
- TFT_eSPI (alternative TFT library)
- U8g2 (alternative OLED library)

## Examples and Demos

### Serial Monitor Demo
Run `simple_wobble_demo.ino` to see ASCII art wobble in Serial Monitor.

### OLED Demo
Uncomment OLED sections in main sketch for 128x64 OLED display.

### TFT Color Demo
Use TFT configuration for colorful wobble patterns.

## Contributing

Feel free to submit improvements, additional display support, or optimization suggestions!

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0** - Initial release with basic wobble generation
- **v1.1** - Added multi-display support and configuration system
- **v1.2** - Performance optimizations and real-time control
- **v1.3** - Enhanced documentation and examples

---

**Enjoy creating mesmerizing wobble patterns on your Arduino displays!** 🌊