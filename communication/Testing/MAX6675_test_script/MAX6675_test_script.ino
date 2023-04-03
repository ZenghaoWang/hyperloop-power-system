/*
  MAX6675_test_script

  Testing script used to work with the MAX6675.

  Found an issue with the library commented below; the temperature it was producing was
  ver wrong. Remade the library code and fixed the issue in the library.
*/

// #include <MAX6675.h> // https://github.com/zhenek-kreker/MAX6675 (install from library manager)

#include <SPI.h>

// Themocouple chip select digital pin
#define THERMOCOUPLE_CS 7
// MAX6675 *thermocouple;

struct {
  float temp = 0.00;
  uint32_t lastcalltime = 0;
} thermocouple;

float get_temp_in_c() {
  if (millis()  - thermocouple.lastcalltime >= 250) {
    SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));  // <---- this was the issue, it should be SPI_MODE0
    digitalWrite(THERMOCOUPLE_CS, LOW);
    uint16_t received_data = SPI.transfer16(NULL);
    digitalWrite(THERMOCOUPLE_CS, HIGH);
    thermocouple.lastcalltime = millis();
    if (received_data & 0x04) {
      thermocouple.temp = NAN;
    } else {
      thermocouple.temp = (received_data >> 3) * 0.25;
    }
    SPI.endTransaction();
  }
  return thermocouple.temp;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // thermocouple = new MAX6675(THERMOCOUPLE_CS);
  pinMode(THERMOCOUPLE_CS, OUTPUT);
  digitalWrite(THERMOCOUPLE_CS, HIGH);
  SPI.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(get_temp_in_c());
  delay(500);
}
