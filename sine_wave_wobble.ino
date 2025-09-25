/*
 * Sine Wave Wobble Generator for Arduino Display
 * 
 * This program generates a dynamic sine wave wobble pattern suitable for
 * display on Arduino-powered screens. The wobble effect creates visually
 * appealing wave patterns with adjustable amplitude and frequency.
 * 
 * Compatible with various Arduino display libraries including:
 * - Adafruit SSD1306 (OLED displays)
 * - Adafruit ST7735/ST7789 (TFT displays)
 * - Arduino TFT library
 * 
 * Features:
 * - Adjustable amplitude (wave height)
 * - Adjustable frequency (wave speed/density)
 * - Real-time animation
 * - Optimized for Arduino memory constraints
 * 
 * Author: Arduino Sine Wobble Generator
 * Date: 2024
 */

// Include necessary Arduino libraries
#include <Arduino.h>
#include <math.h>

// Display library includes (uncomment based on your display type)
// #include <Adafruit_SSD1306.h>  // For OLED displays
// #include <Adafruit_ST7735.h>   // For TFT displays
// #include <Adafruit_GFX.h>      // Graphics library

// ========================================
// CONFIGURATION PARAMETERS
// ========================================

// Display dimensions (adjust based on your screen)
const int SCREEN_WIDTH = 128;
const int SCREEN_HEIGHT = 64;

// Sine wave wobble parameters
struct WobbleParams {
  float amplitude;        // Wave amplitude (0.1 to 1.0)
  float frequency;        // Wave frequency (0.1 to 5.0)
  float phase;           // Phase offset for animation
  float phaseIncrement;  // How fast the animation moves
};

// Initialize wobble parameters with default values
WobbleParams wobble = {
  .amplitude = 0.7,      // 70% of screen height
  .frequency = 2.0,      // 2 waves per screen width
  .phase = 0.0,          // Starting phase
  .phaseIncrement = 0.1  // Animation speed
};

// Display object (uncomment and configure based on your display)
// Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ========================================
// SINE WAVE CALCULATION FUNCTIONS
// ========================================

/**
 * Calculate sine wave Y position for given X coordinate
 * @param x - X coordinate (0 to SCREEN_WIDTH)
 * @param params - Wobble parameters structure
 * @return Y coordinate for the sine wave
 */
int calculateSineY(int x, const WobbleParams& params) {
  // Convert x to normalized coordinate (0 to 2π * frequency)
  float normalizedX = (float)x / SCREEN_WIDTH * 2.0 * PI * params.frequency;
  
  // Calculate sine value with phase offset
  float sineValue = sin(normalizedX + params.phase);
  
  // Scale to screen coordinates
  int centerY = SCREEN_HEIGHT / 2;
  int amplitude_pixels = (int)(params.amplitude * SCREEN_HEIGHT / 2);
  
  return centerY + (int)(sineValue * amplitude_pixels);
}

/**
 * Generate wobble effect by modulating the main sine wave
 * @param x - X coordinate
 * @param baseY - Base Y coordinate from main sine wave
 * @param params - Wobble parameters
 * @return Modified Y coordinate with wobble effect
 */
int applyWobbleEffect(int x, int baseY, const WobbleParams& params) {
  // Create secondary sine wave for wobble effect
  float wobbleFreq = params.frequency * 3.0; // Higher frequency for wobble
  float normalizedX = (float)x / SCREEN_WIDTH * 2.0 * PI * wobbleFreq;
  float wobbleValue = sin(normalizedX + params.phase * 2.5);
  
  // Apply wobble amplitude (smaller than main wave)
  int wobbleAmplitude = (int)(params.amplitude * SCREEN_HEIGHT * 0.1);
  int wobbleOffset = (int)(wobbleValue * wobbleAmplitude);
  
  return constrain(baseY + wobbleOffset, 0, SCREEN_HEIGHT - 1);
}

// ========================================
// DISPLAY FUNCTIONS
// ========================================

/**
 * Draw sine wave wobble pattern on the display
 */
void drawSineWobble() {
  // Clear display buffer (implementation depends on display library)
  // display.clearDisplay();
  
  // Generate sine wave points
  for (int x = 0; x < SCREEN_WIDTH - 1; x++) {
    // Calculate main sine wave Y coordinates
    int y1 = calculateSineY(x, wobble);
    int y2 = calculateSineY(x + 1, wobble);
    
    // Apply wobble effect
    y1 = applyWobbleEffect(x, y1, wobble);
    y2 = applyWobbleEffect(x + 1, y2, wobble);
    
    // Draw line segment (uncomment based on your display library)
    // display.drawLine(x, y1, x + 1, y2, WHITE);
    
    // Alternative: Draw individual pixels for more control
    // display.drawPixel(x, y1, WHITE);
    
    // For debugging: print coordinates to serial monitor
    if (x % 10 == 0) { // Print every 10th point to avoid flooding serial
      Serial.print("X:");
      Serial.print(x);
      Serial.print(" Y:");
      Serial.println(y1);
    }
  }
  
  // Update display (implementation depends on display library)
  // display.display();
}

/**
 * Draw additional visual elements (optional enhancements)
 */
void drawEnhancements() {
  // Draw center line
  // display.drawLine(0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2, WHITE);
  
  // Draw amplitude indicators
  int maxY = SCREEN_HEIGHT/2 - (int)(wobble.amplitude * SCREEN_HEIGHT/2);
  int minY = SCREEN_HEIGHT/2 + (int)(wobble.amplitude * SCREEN_HEIGHT/2);
  
  // display.drawLine(0, maxY, 5, maxY, WHITE);
  // display.drawLine(0, minY, 5, minY, WHITE);
}

// ========================================
// PARAMETER ADJUSTMENT FUNCTIONS
// ========================================

/**
 * Adjust wobble amplitude based on analog input or time
 */
void updateAmplitude() {
  // Example: Use analog pin for real-time adjustment
  // int analogValue = analogRead(A0);
  // wobble.amplitude = map(analogValue, 0, 1023, 10, 100) / 100.0;
  
  // Alternative: Automatic amplitude variation
  static unsigned long lastUpdate = 0;
  if (millis() - lastUpdate > 5000) { // Change every 5 seconds
    wobble.amplitude = 0.3 + 0.4 * sin(millis() * 0.0005);
    lastUpdate = millis();
  }
}

/**
 * Adjust wobble frequency based on input or time
 */
void updateFrequency() {
  // Example: Use analog pin for real-time adjustment
  // int analogValue = analogRead(A1);
  // wobble.frequency = map(analogValue, 0, 1023, 10, 500) / 100.0;
  
  // Alternative: Automatic frequency variation
  static unsigned long lastUpdate = 0;
  if (millis() - lastUpdate > 3000) { // Change every 3 seconds
    wobble.frequency = 1.0 + 2.0 * sin(millis() * 0.0003);
    lastUpdate = millis();
  }
}

/**
 * Update animation phase for continuous movement
 */
void updatePhase() {
  wobble.phase += wobble.phaseIncrement;
  
  // Keep phase in reasonable range to prevent float overflow
  if (wobble.phase > 2.0 * PI * 100) {
    wobble.phase = 0.0;
  }
}

// ========================================
// ARDUINO SETUP AND MAIN LOOP
// ========================================

/**
 * Arduino setup function - runs once at startup
 */
void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);
  Serial.println("Sine Wave Wobble Generator Starting...");
  
  // Initialize display (uncomment and configure based on your display)
  /*
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("Sine Wobble Ready");
  display.display();
  delay(2000);
  */
  
  // Initialize analog pins for parameter control (optional)
  // pinMode(A0, INPUT); // Amplitude control
  // pinMode(A1, INPUT); // Frequency control
  
  Serial.println("Setup complete. Starting wobble animation...");
  Serial.println("Parameters:");
  Serial.print("- Amplitude: ");
  Serial.println(wobble.amplitude);
  Serial.print("- Frequency: ");
  Serial.println(wobble.frequency);
  Serial.print("- Phase Increment: ");
  Serial.println(wobble.phaseIncrement);
}

/**
 * Arduino main loop - runs continuously
 */
void loop() {
  // Update wobble parameters
  updateAmplitude();
  updateFrequency();
  updatePhase();
  
  // Draw the sine wave wobble
  drawSineWobble();
  
  // Draw optional enhancements
  drawEnhancements();
  
  // Print current parameters to serial (for debugging)
  static unsigned long lastDebugPrint = 0;
  if (millis() - lastDebugPrint > 2000) { // Print every 2 seconds
    Serial.print("Amplitude: ");
    Serial.print(wobble.amplitude, 2);
    Serial.print(", Frequency: ");
    Serial.print(wobble.frequency, 2);
    Serial.print(", Phase: ");
    Serial.println(wobble.phase, 2);
    lastDebugPrint = millis();
  }
  
  // Control animation speed
  delay(50); // 20 FPS (adjust for desired animation speed)
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * Helper function to constrain values within bounds
 */
int constrain(int value, int min_val, int max_val) {
  if (value < min_val) return min_val;
  if (value > max_val) return max_val;
  return value;
}

/**
 * Fast sine approximation for performance-critical applications
 * (Optional - use if standard sin() is too slow)
 */
float fastSin(float x) {
  // Normalize x to -π to π range
  while (x > PI) x -= 2 * PI;
  while (x < -PI) x += 2 * PI;
  
  // Taylor series approximation (good balance of speed vs accuracy)
  float x2 = x * x;
  return x * (1.0 - x2 / 6.0 * (1.0 - x2 / 20.0));
}

/**
 * Map function implementation (if not available in Arduino core)
 */
long map(long x, long in_min, long in_max, long out_min, long out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

/*
 * ========================================
 * USAGE NOTES AND CUSTOMIZATION GUIDE
 * ========================================
 * 
 * To use this code with your specific display:
 * 
 * 1. OLED Display (SSD1306):
 *    - Uncomment the Adafruit_SSD1306 includes
 *    - Uncomment display initialization in setup()
 *    - Uncomment display.drawLine() calls in drawSineWobble()
 * 
 * 2. TFT Display (ST7735/ST7789):
 *    - Replace SSD1306 includes with ST7735/ST7789
 *    - Adjust pin definitions for your setup
 *    - Use appropriate color constants
 * 
 * 3. Custom Display:
 *    - Replace display function calls with your library's functions
 *    - Adjust SCREEN_WIDTH and SCREEN_HEIGHT constants
 * 
 * 4. Parameter Adjustment:
 *    - Connect potentiometers to A0 and A1 for real-time control
 *    - Uncomment analog read sections in update functions
 *    - Adjust value ranges in map() functions
 * 
 * 5. Performance Optimization:
 *    - Use fastSin() instead of sin() for better performance
 *    - Reduce SCREEN_WIDTH for faster calculation
 *    - Increase delay() in loop() for slower animation
 * 
 * 6. Visual Customization:
 *    - Modify wobbleFreq multiplier for different wobble effects
 *    - Adjust wobbleAmplitude for more or less wobble
 *    - Add multiple sine waves with different parameters
 */