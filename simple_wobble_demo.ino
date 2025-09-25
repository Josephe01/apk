/*
 * Simple Sine Wave Wobble Demo
 * 
 * A simplified version of the sine wave wobble generator that works
 * out-of-the-box for testing and demonstration purposes.
 * 
 * This demo outputs the wobble coordinates to the Serial Monitor,
 * making it easy to test without requiring specific display hardware.
 * 
 * Upload this sketch to your Arduino and open the Serial Monitor
 * to see the wobble pattern coordinates in real-time.
 */

#include <Arduino.h>
#include <math.h>

// Simple configuration
const int SCREEN_WIDTH = 64;   // Reduced for clearer serial output
const int SCREEN_HEIGHT = 32;  // Reduced for clearer serial output

// Wobble parameters
float amplitude = 0.8;      // Wave height (80% of screen)
float frequency = 1.5;      // 1.5 waves across screen
float phase = 0.0;          // Current animation phase
float phaseSpeed = 0.15;    // Animation speed

/**
 * Calculate sine wave Y coordinate with wobble effect
 */
int calculateWobbleY(int x) {
  // Main sine wave
  float mainWave = sin((float)x / SCREEN_WIDTH * 2.0 * PI * frequency + phase);
  
  // Wobble effect (secondary wave)
  float wobbleWave = sin((float)x / SCREEN_WIDTH * 2.0 * PI * frequency * 3.0 + phase * 2.0);
  
  // Combine waves
  float combinedWave = mainWave + wobbleWave * 0.3; // Wobble is 30% of main wave
  
  // Convert to screen coordinates
  int centerY = SCREEN_HEIGHT / 2;
  int waveAmplitude = (int)(amplitude * SCREEN_HEIGHT / 2);
  
  return centerY + (int)(combinedWave * waveAmplitude);
}

/**
 * Draw ASCII representation of the wobble
 */
void drawASCIIWobble() {
  Serial.println("\n--- Sine Wave Wobble Frame ---");
  
  // Create a simple ASCII buffer
  char buffer[SCREEN_HEIGHT][SCREEN_WIDTH + 1];
  
  // Initialize buffer with spaces
  for (int y = 0; y < SCREEN_HEIGHT; y++) {
    for (int x = 0; x < SCREEN_WIDTH; x++) {
      buffer[y][x] = ' ';
    }
    buffer[y][SCREEN_WIDTH] = '\0'; // Null terminate
  }
  
  // Draw center line
  for (int x = 0; x < SCREEN_WIDTH; x++) {
    buffer[SCREEN_HEIGHT/2][x] = '-';
  }
  
  // Draw wobble line
  for (int x = 0; x < SCREEN_WIDTH; x++) {
    int y = calculateWobbleY(x);
    
    // Ensure y is within bounds
    if (y >= 0 && y < SCREEN_HEIGHT) {
      buffer[y][x] = '*';
    }
    
    // Print coordinates for debugging
    if (x % 8 == 0) { // Print every 8th coordinate
      Serial.print("X:");
      Serial.print(x);
      Serial.print(" Y:");
      Serial.print(y);
      Serial.print(" | ");
    }
  }
  
  Serial.println(); // New line after coordinates
  
  // Print the ASCII buffer
  for (int y = 0; y < SCREEN_HEIGHT; y++) {
    Serial.print("|");
    Serial.print(buffer[y]);
    Serial.println("|");
  }
  
  // Print current parameters
  Serial.print("Amplitude: ");
  Serial.print(amplitude, 2);
  Serial.print(" | Frequency: ");
  Serial.print(frequency, 2);
  Serial.print(" | Phase: ");
  Serial.println(phase, 2);
}

/**
 * Update wobble parameters for animation
 */
void updateWobble() {
  // Advance animation phase
  phase += phaseSpeed;
  
  // Keep phase in reasonable range
  if (phase > 2.0 * PI * 10) {
    phase = 0.0;
  }
  
  // Optional: Vary amplitude over time
  static unsigned long lastAmplitudeChange = 0;
  if (millis() - lastAmplitudeChange > 8000) { // Change every 8 seconds
    amplitude = 0.4 + 0.4 * sin(millis() * 0.0003);
    lastAmplitudeChange = millis();
  }
  
  // Optional: Vary frequency over time
  static unsigned long lastFrequencyChange = 0;
  if (millis() - lastFrequencyChange > 6000) { // Change every 6 seconds
    frequency = 1.0 + 1.0 * sin(millis() * 0.0002);
    lastFrequencyChange = millis();
  }
}

void setup() {
  Serial.begin(9600);
  
  // Wait for Serial connection (needed for some boards)
  while (!Serial) {
    delay(100);
  }
  
  Serial.println("=================================");
  Serial.println("Sine Wave Wobble Demo Starting");
  Serial.println("=================================");
  Serial.print("Screen Size: ");
  Serial.print(SCREEN_WIDTH);
  Serial.print(" x ");
  Serial.println(SCREEN_HEIGHT);
  Serial.println("Watch the wobble pattern below!");
  Serial.println("Open Serial Monitor at 9600 baud");
  Serial.println("=================================\n");
  
  delay(2000); // Give user time to read
}

void loop() {
  // Update wobble parameters
  updateWobble();
  
  // Draw the wobble pattern
  drawASCIIWobble();
  
  // Control animation speed
  delay(800); // Slower for better visibility in serial monitor
}

/*
 * Expected Output:
 * 
 * You should see an ASCII representation of a sine wave with wobble effect
 * that animates over time. The '*' characters show the wobble line, and
 * the '-' characters show the center reference line.
 * 
 * The amplitude and frequency will automatically vary over time to
 * demonstrate the dynamic nature of the wobble effect.
 * 
 * To use with a real display:
 * 1. Replace the ASCII drawing code with your display library calls
 * 2. Use the calculateWobbleY() function to get Y coordinates
 * 3. Adjust SCREEN_WIDTH and SCREEN_HEIGHT for your display
 * 4. Modify the delay() for desired animation speed
 */