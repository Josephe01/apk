#!/usr/bin/env python3
"""
Sine Wave Wobble Simulator

This Python script simulates the Arduino sine wave wobble generator
to help visualize the wobble patterns and test parameters before
uploading to the Arduino.

Run this script to see an animated ASCII representation of the wobble
pattern that matches what the Arduino code will generate.
"""

import math
import time
import os
import sys

# Configuration (matching Arduino defaults)
SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32
AMPLITUDE = 0.8
FREQUENCY = 1.5
PHASE_SPEED = 0.15

def calculate_wobble_y(x, phase, amplitude=AMPLITUDE, frequency=FREQUENCY):
    """Calculate sine wave Y coordinate with wobble effect"""
    # Main sine wave
    main_wave = math.sin(x / SCREEN_WIDTH * 2.0 * math.pi * frequency + phase)
    
    # Wobble effect (secondary wave)
    wobble_wave = math.sin(x / SCREEN_WIDTH * 2.0 * math.pi * frequency * 3.0 + phase * 2.0)
    
    # Combine waves
    combined_wave = main_wave + wobble_wave * 0.3  # Wobble is 30% of main wave
    
    # Convert to screen coordinates
    center_y = SCREEN_HEIGHT // 2
    wave_amplitude = int(amplitude * SCREEN_HEIGHT / 2)
    
    y = center_y + int(combined_wave * wave_amplitude)
    
    # Clamp to screen bounds
    return max(0, min(SCREEN_HEIGHT - 1, y))

def draw_ascii_wobble(phase):
    """Draw ASCII representation of the wobble"""
    # Create buffer
    buffer = [[' ' for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    
    # Draw center line
    for x in range(SCREEN_WIDTH):
        buffer[SCREEN_HEIGHT//2][x] = '-'
    
    # Draw wobble line
    coordinates = []
    for x in range(SCREEN_WIDTH):
        y = calculate_wobble_y(x, phase)
        buffer[y][x] = '*'
        if x % 8 == 0:  # Collect every 8th coordinate for display
            coordinates.append((x, y))
    
    # Clear screen (works on most terminals)
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("=" * 70)
    print("Arduino Sine Wave Wobble Simulator")
    print("=" * 70)
    print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT} | Phase: {phase:.2f}")
    print(f"Amplitude: {AMPLITUDE:.2f} | Frequency: {FREQUENCY:.2f}")
    print("-" * 70)
    
    # Print buffer
    for row in buffer:
        print("|" + "".join(row) + "|")
    
    print("-" * 70)
    print("Coordinates (every 8th point):")
    coord_str = " | ".join([f"X:{x:2d} Y:{y:2d}" for x, y in coordinates])
    print(coord_str)
    print("-" * 70)
    print("Press Ctrl+C to stop")

def demonstrate_parameter_changes():
    """Demonstrate how different parameters affect the wobble"""
    parameters = [
        (0.4, 1.0, "Small amplitude, low frequency"),
        (0.9, 1.0, "Large amplitude, low frequency"), 
        (0.6, 3.0, "Medium amplitude, high frequency"),
        (0.8, 1.5, "Default parameters"),
    ]
    
    print("Demonstrating different parameter combinations...")
    print("Each pattern will display for 3 seconds")
    
    for amp, freq, description in parameters:
        print(f"\nShowing: {description}")
        print(f"Amplitude: {amp}, Frequency: {freq}")
        time.sleep(2)
        
        # Show 10 frames of this configuration
        for frame in range(10):
            phase = frame * 0.2
            
            # Temporarily change globals
            global AMPLITUDE, FREQUENCY
            old_amp, old_freq = AMPLITUDE, FREQUENCY
            AMPLITUDE, FREQUENCY = amp, freq
            
            draw_ascii_wobble(phase)
            
            # Restore globals
            AMPLITUDE, FREQUENCY = old_amp, old_freq
            
            time.sleep(0.3)

def main():
    """Main simulation loop"""
    print("Starting Arduino Sine Wave Wobble Simulation...")
    print("This simulates the wobble pattern your Arduino will generate.")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demonstrate_parameter_changes()
        return
    
    phase = 0.0
    frame_count = 0
    
    try:
        while True:
            draw_ascii_wobble(phase)
            
            # Update phase
            phase += PHASE_SPEED
            frame_count += 1
            
            # Keep phase in reasonable range
            if phase > 2.0 * math.pi * 10:
                phase = 0.0
            
            # Optional: vary parameters over time (like Arduino version)
            if frame_count % 50 == 0:  # Every 50 frames
                global AMPLITUDE, FREQUENCY
                AMPLITUDE = 0.4 + 0.4 * math.sin(frame_count * 0.02)
                FREQUENCY = 1.0 + 1.0 * math.sin(frame_count * 0.015)
            
            time.sleep(0.5)  # Control animation speed
            
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user.")
        print("The Arduino wobble generator is ready to upload!")

if __name__ == "__main__":
    main()