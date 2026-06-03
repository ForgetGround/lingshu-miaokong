#include <Arduino.h>

#include "config.h"

static uint16_t window_buffer[WINDOW_SIZE][EMG_CHANNEL_COUNT];

static void configureJointDriverPins() {
  for (uint8_t finger = 0; finger < FINGER_COUNT; ++finger) {
    for (uint8_t joint = 0; joint < JOINTS_PER_FINGER; ++joint) {
      pinMode(JOINT_DRIVER_PINS[finger][joint], OUTPUT);
      digitalWrite(JOINT_DRIVER_PINS[finger][joint], LOW);
    }
  }
}

static void printWindowCsv() {
  for (uint16_t sample = 0; sample < WINDOW_SIZE; ++sample) {
    for (uint8_t channel = 0; channel < EMG_CHANNEL_COUNT; ++channel) {
      if (sample > 0 || channel > 0) {
        Serial.print(',');
      }
      Serial.print(window_buffer[sample][channel]);
    }
  }
  Serial.println();
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  analogReadResolution(12);
  configureJointDriverPins();
  delay(300);
}

void loop() {
  uint32_t next_sample_at = micros();

  for (uint16_t sample = 0; sample < WINDOW_SIZE; ++sample) {
    while (static_cast<int32_t>(micros() - next_sample_at) < 0) {
      delayMicroseconds(10);
    }

    for (uint8_t channel = 0; channel < EMG_CHANNEL_COUNT; ++channel) {
      window_buffer[sample][channel] = analogRead(EMG_ADC_PINS[channel]);
    }

    next_sample_at += SAMPLE_INTERVAL_US;
  }

  printWindowCsv();
}
