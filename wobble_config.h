/*
 * Wobble Configuration Header
 * 
 * This file contains all configuration parameters for the sine wave wobble
 * generator. Modify these values to customize the wobble behavior for your
 * specific Arduino display setup.
 */

#ifndef WOBBLE_CONFIG_H
#define WOBBLE_CONFIG_H

// ========================================
// DISPLAY CONFIGURATION
// ========================================

// Display type selection (uncomment ONE of the following)
// #define USE_SSD1306_OLED    // For OLED displays using SSD1306
// #define USE_ST7735_TFT      // For TFT displays using ST7735
// #define USE_ST7789_TFT      // For TFT displays using ST7789
// #define USE_SERIAL_OUTPUT   // For serial monitor output (debugging)
#define USE_CUSTOM_DISPLAY     // For custom display implementation

// Display dimensions (adjust based on your screen)
#ifdef USE_SSD1306_OLED
  #define SCREEN_WIDTH 128
  #define SCREEN_HEIGHT 64
#elif defined(USE_ST7735_TFT)
  #define SCREEN_WIDTH 128
  #define SCREEN_HEIGHT 160
#elif defined(USE_ST7789_TFT)
  #define SCREEN_WIDTH 240
  #define SCREEN_HEIGHT 240
#else
  #define SCREEN_WIDTH 128
  #define SCREEN_HEIGHT 64
#endif

// Display pins (adjust based on your wiring)
#ifdef USE_SSD1306_OLED
  #define OLED_RESET -1
  #define OLED_ADDRESS 0x3C
#elif defined(USE_ST7735_TFT) || defined(USE_ST7789_TFT)
  #define TFT_CS     10
  #define TFT_RST    9
  #define TFT_DC     8
#endif

// ========================================
// WOBBLE PARAMETERS
// ========================================

// Default wobble settings
#define DEFAULT_AMPLITUDE     0.7f    // Wave amplitude (0.1 to 1.0)
#define DEFAULT_FREQUENCY     2.0f    // Wave frequency (0.1 to 5.0)
#define DEFAULT_PHASE_INC     0.1f    // Animation speed (0.01 to 0.5)

// Wobble effect settings
#define WOBBLE_FREQ_MULTIPLIER  3.0f  // Secondary wave frequency multiplier
#define WOBBLE_AMPLITUDE_RATIO  0.1f  // Wobble amplitude as ratio of main amplitude

// Animation settings
#define ANIMATION_DELAY       50      // Delay between frames (ms) - controls FPS
#define DEBUG_PRINT_INTERVAL  2000    // Debug print interval (ms)

// Parameter update intervals (for automatic variation)
#define AMPLITUDE_UPDATE_INTERVAL  5000  // ms
#define FREQUENCY_UPDATE_INTERVAL  3000  // ms

// ========================================
// CONTROL INPUT CONFIGURATION
// ========================================

// Analog input pins for real-time control (optional)
#define AMPLITUDE_CONTROL_PIN  A0  // Potentiometer for amplitude control
#define FREQUENCY_CONTROL_PIN  A1  // Potentiometer for frequency control
#define SPEED_CONTROL_PIN      A2  // Potentiometer for animation speed

// Enable/disable real-time control
#define ENABLE_AMPLITUDE_CONTROL  false
#define ENABLE_FREQUENCY_CONTROL  false
#define ENABLE_SPEED_CONTROL      false

// Control value ranges
#define MIN_AMPLITUDE  0.1f
#define MAX_AMPLITUDE  1.0f
#define MIN_FREQUENCY  0.1f
#define MAX_FREQUENCY  5.0f
#define MIN_PHASE_INC  0.01f
#define MAX_PHASE_INC  0.5f

// ========================================
// PERFORMANCE SETTINGS
// ========================================

// Use fast sine approximation for better performance
#define USE_FAST_SINE  false

// Reduce calculation precision for speed (if needed)
#define CALCULATION_STEP  1  // Calculate every N pixels (1 = every pixel)

// Enable/disable visual enhancements
#define DRAW_CENTER_LINE      true
#define DRAW_AMPLITUDE_MARKS  true
#define DRAW_GRID            false

// ========================================
// SERIAL DEBUG CONFIGURATION
// ========================================

#define SERIAL_BAUD_RATE      9600
#define ENABLE_DEBUG_OUTPUT   true
#define ENABLE_COORDINATE_OUTPUT false  // Print wave coordinates

#endif // WOBBLE_CONFIG_H