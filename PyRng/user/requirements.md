# PyRng - Random Number Generator Requirements

## Project Overview
A highly configurable command-line random number generator written in Python, designed to run on Ubuntu Linux with support for multiple distribution types, execution modes, and flexible configuration management.

## Project Name
**PyRng**

## Core Features

### 1. Number Types
- Support for **integer** random numbers
- Support for **floating-point** random numbers
- Type selection should be configurable

### 2. Output Modes
- **Single value**: Generate one random number
- **Range/Multiple values**: Generate multiple random numbers
- Count/range should be configurable

### 3. Distribution Types
Support for multiple probability distributions:
- **Uniform** distribution (default)
- **Normal/Gaussian** distribution
- **Exponential** distribution
- Additional distributions as appropriate
- Distribution parameters should be configurable

### 4. Execution Modes
- **Run once**: Generate number(s) and exit
- **Continuous mode**: Keep generating numbers until stopped
- Mode selection should be configurable

### 5. Interface Modes
- **Bash/CLI mode**: Non-interactive mode suitable for scripting and piping
- **Interactive mode**: Allow users to change and update configurations in real-time
- Mode selection should be configurable

### 6. Seeding Options
- **Fixed seed**: Use a specific seed value for reproducibility
- **Random seed**: Use system entropy for true randomness
- Seed configuration should be optional and configurable

### 7. Output Saving
- **Optional feature** to save generated values to a file
- Format: **Comma-separated text** (CSV-compatible)
- File path and save option should be configurable

## Technical Stack

### Language
- **Python** (version 3.8+ recommended for Ubuntu compatibility)

### Platform
- **Ubuntu Linux**

### Interface
- **Command-line interface (CLI)**

## Configuration Management

### Configuration File
- Support for a configuration file (e.g., JSON, YAML, or INI format)
- **Default behavior**: If config file not found, create one with sensible default values on first run
- Config file should store all configurable options

### Command-Line Arguments
- All configuration options should be overridable via command-line arguments
- Command-line arguments take precedence over config file settings

### Interactive Mode Configuration
- In interactive mode, users should be able to:
  - View current configuration
  - Modify configuration parameters dynamically
  - Update and save configuration changes
  - Generate numbers with updated settings without restarting

## Configuration Options Summary

The following options should be configurable via config file and/or command-line arguments:

1. **Number type**: `int` or `float`
2. **Output mode**: `single` or `multiple` (with count parameter)
3. **Distribution type**: `uniform`, `normal`, `exponential`, etc.
4. **Distribution parameters**: mean, std dev, lambda, min, max, etc. (depending on distribution)
5. **Execution mode**: `once` or `continuous`
6. **Interface mode**: `cli` or `interactive`
7. **Seed**: `fixed` (with seed value) or `random`
8. **Output saving**: `enabled` or `disabled`
9. **Output file path**: path to save generated values (if saving enabled)

## User Experience Requirements

### First Run
- If no config file exists, create one with sensible defaults
- Inform user that config file was created and where it's located

### CLI Mode
- Output should be clean and parseable (suitable for piping and scripting)
- Minimal or no extraneous messages in non-verbose mode

### Interactive Mode
- Provide clear menu or command interface
- Show current configuration
- Allow easy modification of settings
- Provide help/documentation within the interface

## Success Criteria
- Program runs successfully on Ubuntu Linux
- All configuration options work as specified
- Config file is created automatically if missing
- Command-line arguments properly override config file
- Interactive mode allows real-time configuration updates
- Generated numbers follow specified distributions
- Output saving works correctly when enabled
- Code is clean, well-documented, and maintainable

## Date
November 24, 2025
