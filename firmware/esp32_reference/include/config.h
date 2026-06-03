#pragma once

#include <Arduino.h>

constexpr uint32_t SERIAL_BAUD = 115200;
constexpr uint16_t WINDOW_SIZE = 200;
constexpr uint8_t EMG_CHANNEL_COUNT = 8;
constexpr uint32_t SAMPLE_INTERVAL_US = 1000;

// Placeholder GPIO mapping for ESP32-S3-WROOM-1-N16R8.
// Replace these values with the final EasyEDA netlist before hardware bring-up.
constexpr uint8_t EMG_ADC_PINS[EMG_CHANNEL_COUNT] = {
  1, 2, 3, 4, 5, 6, 7, 8
};

constexpr uint8_t FINGER_COUNT = 5;
constexpr uint8_t JOINTS_PER_FINGER = 3;

// Logical IO1_1..IO5_3 driver pins. Replace with final schematic GPIOs.
constexpr uint8_t JOINT_DRIVER_PINS[FINGER_COUNT][JOINTS_PER_FINGER] = {
  {9, 10, 11},
  {12, 13, 14},
  {15, 16, 17},
  {18, 21, 33},
  {34, 35, 36},
};
