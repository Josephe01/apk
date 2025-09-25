#!/usr/bin/env python3
"""
Project Validation Script

This script validates that all components of the Arduino Sine Wave Wobble
Generator are correctly implemented and ready for use.
"""

import os
import re
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {os.path.basename(filepath)}")
        return True
    else:
        print(f"✗ {description}: {os.path.basename(filepath)} - MISSING")
        return False

def validate_arduino_syntax(filepath):
    """Basic validation of Arduino sketch syntax"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check for required Arduino functions
        has_setup = 'void setup()' in content
        has_loop = 'void loop()' in content
        
        # Check for basic includes
        has_arduino = '#include <Arduino.h>' in content or '#include "Arduino.h"' in content
        
        # Check for sine wave calculation
        has_sin = 'sin(' in content
        
        issues = []
        if not has_setup:
            issues.append("Missing setup() function")
        if not has_loop:
            issues.append("Missing loop() function")
        if not has_sin:
            issues.append("No sine wave calculations found")
        
        if issues:
            print(f"  ⚠ Issues in {os.path.basename(filepath)}:")
            for issue in issues:
                print(f"    - {issue}")
            return False
        else:
            print(f"  ✓ Arduino syntax looks good in {os.path.basename(filepath)}")
            return True
            
    except Exception as e:
        print(f"  ✗ Error reading {os.path.basename(filepath)}: {e}")
        return False

def validate_config_file(filepath):
    """Validate configuration header file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check for key configuration elements
        has_screen_width = 'SCREEN_WIDTH' in content
        has_screen_height = 'SCREEN_HEIGHT' in content
        has_amplitude = 'AMPLITUDE' in content
        has_frequency = 'FREQUENCY' in content
        
        issues = []
        if not has_screen_width:
            issues.append("Missing SCREEN_WIDTH definition")
        if not has_screen_height:
            issues.append("Missing SCREEN_HEIGHT definition")
        if not has_amplitude:
            issues.append("Missing amplitude configuration")
        if not has_frequency:
            issues.append("Missing frequency configuration")
        
        if issues:
            print(f"  ⚠ Issues in {os.path.basename(filepath)}:")
            for issue in issues:
                print(f"    - {issue}")
            return False
        else:
            print(f"  ✓ Configuration file looks complete")
            return True
            
    except Exception as e:
        print(f"  ✗ Error reading {os.path.basename(filepath)}: {e}")
        return False

def main():
    """Main validation function"""
    print("=" * 60)
    print("Arduino Sine Wave Wobble Generator - Project Validation")
    print("=" * 60)
    
    project_dir = "/home/runner/work/apk/apk"
    
    # Check all required files
    files_to_check = [
        (f"{project_dir}/sine_wave_wobble.ino", "Main Arduino sketch"),
        (f"{project_dir}/wobble_config.h", "Configuration header"),
        (f"{project_dir}/simple_wobble_demo.ino", "Demo sketch"),
        (f"{project_dir}/display_examples", "Display examples"),
        (f"{project_dir}/wobble_simulator.py", "Python simulator"),
        (f"{project_dir}/WOBBLE_README.md", "Documentation"),
        (f"{project_dir}/README.md", "Original README"),
    ]
    
    print("\n1. File Existence Check:")
    print("-" * 30)
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    # Validate Arduino sketches
    print("\n2. Arduino Sketch Validation:")
    print("-" * 35)
    
    arduino_files = [
        f"{project_dir}/sine_wave_wobble.ino",
        f"{project_dir}/simple_wobble_demo.ino"
    ]
    
    arduino_syntax_ok = True
    for filepath in arduino_files:
        if os.path.exists(filepath):
            if not validate_arduino_syntax(filepath):
                arduino_syntax_ok = False
        else:
            arduino_syntax_ok = False
    
    # Validate configuration
    print("\n3. Configuration Validation:")
    print("-" * 35)
    config_ok = True
    config_file = f"{project_dir}/wobble_config.h"
    if os.path.exists(config_file):
        config_ok = validate_config_file(config_file)
    else:
        config_ok = False
    
    # Check Python simulator
    print("\n4. Python Simulator Check:")
    print("-" * 35)
    simulator_file = f"{project_dir}/wobble_simulator.py"
    simulator_ok = True
    if os.path.exists(simulator_file):
        if os.access(simulator_file, os.X_OK):
            print("  ✓ Python simulator is executable")
        else:
            print("  ⚠ Python simulator is not executable (run: chmod +x)")
            simulator_ok = False
            
        # Try to run a quick syntax check
        exit_code = os.system(f"python3 -m py_compile {simulator_file} 2>/dev/null")
        if exit_code == 0:
            print("  ✓ Python simulator syntax is valid")
        else:
            print("  ✗ Python simulator has syntax errors")
            simulator_ok = False
    else:
        simulator_ok = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    components = [
        ("File Structure", all_files_exist),
        ("Arduino Sketches", arduino_syntax_ok),
        ("Configuration", config_ok),
        ("Python Simulator", simulator_ok),
    ]
    
    all_ok = True
    for component, status in components:
        status_icon = "✓" if status else "✗"
        status_text = "PASS" if status else "FAIL"
        print(f"{status_icon} {component:<20} {status_text}")
        if not status:
            all_ok = False
    
    print("-" * 60)
    if all_ok:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("The Arduino Sine Wave Wobble Generator is ready to use.")
        print("\nNext steps:")
        print("1. Upload simple_wobble_demo.ino to test with Serial Monitor")
        print("2. Configure wobble_config.h for your display type")
        print("3. Upload sine_wave_wobble.ino for full functionality")
        print("4. Run wobble_simulator.py to preview the wobble pattern")
    else:
        print("❌ SOME VALIDATIONS FAILED!")
        print("Please fix the issues listed above before using the project.")
    
    print("=" * 60)
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())