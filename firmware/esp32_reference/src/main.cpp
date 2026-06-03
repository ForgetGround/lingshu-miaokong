#include <Arduino.h>

#include "config.h"

static uint16_t window_buffer[WINDOW_SIZE];

void setup() {
  Serial.begin(SERIAL_BAUD);
  analogReadResolution(12);
  delay(300);
}

void loop() {
  uint32_t next_sample_at = micros();

  for (uint16_t index = 0; index < WINDOW_SIZE; ++index) {
    while (static_cast<int32_t>(micros() - next_sample_at) < 0) {
      delayMicroseconds(10);
    }

    window_buffer[index] = analogRead(EMG_ADC_PIN);
    next_sample_at += SAMPLE_INTERVAL_US;
  }

  for (uint16_t index = 0; index < WINDOW_SIZE; ++index) {
    if (index > 0) {
      Serial.print(',');
    }
    Serial.print(window_buffer[index]);
  }
  Serial.println();
}
