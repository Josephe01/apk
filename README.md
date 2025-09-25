# Arduino Sine Wave Wobble Generator

A comprehensive Arduino program that generates dynamic sine wave wobble patterns suitable for display on Arduino-powered screens. Perfect for creating mesmerizing visual effects with adjustable parameters.

## 🌊 Features

- **Dynamic Wobble Animation**: Smooth sine wave patterns with wobble effects
- **Multi-Display Support**: Compatible with OLED, TFT, and custom displays  
- **Real-time Control**: Adjustable amplitude, frequency, and speed
- **Easy Configuration**: Header-based configuration system
- **Visual Simulator**: Python script to preview patterns
- **Comprehensive Documentation**: Complete setup and usage guides

## 🚀 Quick Start

### Option 1: Test with Serial Monitor (Recommended)
```bash
# Upload simple_wobble_demo.ino to your Arduino
# Open Serial Monitor at 9600 baud
# Watch ASCII wobble animation in real-time
```

### Option 2: Preview with Python Simulator
```bash
python3 wobble_simulator.py
# or for parameter demonstration:
python3 wobble_simulator.py --demo
```

### Option 3: Full Arduino Implementation
1. Configure `wobble_config.h` for your display type
2. Upload `sine_wave_wobble.ino` to your Arduino
3. Enjoy dynamic wobble patterns on your screen!

## 📁 Project Files

- **`sine_wave_wobble.ino`** - Main comprehensive Arduino sketch
- **`simple_wobble_demo.ino`** - Simple demo for Serial Monitor
- **`wobble_config.h`** - Configuration header file
- **`display_examples`** - Example code for different displays
- **`wobble_simulator.py`** - Python visualization tool
- **`WOBBLE_README.md`** - Comprehensive documentation
- **`validate_project.py`** - Project validation script

## 🎛️ Supported Displays

- **OLED**: SSD1306 (128x64, 128x32)
- **TFT**: ST7735, ST7789 (various sizes)
- **Custom**: Implement your own display interface
- **Serial**: ASCII art output for testing

## ⚙️ Configuration Example

```cpp
// Wobble parameters
#define DEFAULT_AMPLITUDE     0.7f    // Wave height
#define DEFAULT_FREQUENCY     2.0f    // Wave density  
#define DEFAULT_PHASE_INC     0.1f    // Animation speed

// Display settings
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
```

## 🔧 Hardware Requirements

- Arduino Uno/Nano or compatible
- Supported display (OLED/TFT recommended)
- Optional: Potentiometers for real-time control
- Connecting wires

## 📚 Documentation

See **`WOBBLE_README.md`** for:
- Detailed setup instructions
- Display wiring diagrams
- Configuration options
- Troubleshooting guide
- Advanced customization

## ✅ Validation

Run the validation script to ensure everything is set up correctly:
```bash
python3 validate_project.py
```

## 🎯 Perfect For

- LED matrix displays
- OLED dashboard projects  
- TFT screen demos
- Visual art installations
- Arduino learning projects
- Mesmerizing desktop displays

---

**Ready to create stunning wobble patterns? Start with the simple demo and work your way up to full display integration!** 🌊✨