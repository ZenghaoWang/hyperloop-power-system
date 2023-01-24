/*
  battery_module_mcu

  Monitors the temperature and voltage of the battery module within the UTHT
  Hyperloop pod.

  Designed to run on an Arduino Micro, communicates directly with an Arduino
  Due over I2C (the Micro is the slave and the Due is the master).

  Author: Alexandre Singer
  January 2023
*/

#include <Wire.h>

// The address of this device on the I2C interface.
//   Will be different for EACH Arduino Micro.
//   Can be any value from 0 - 127 (7-bit address).
#define I2C_ADDR 0
// The analog input port used to measure the voltage.
#define VOLTAGE_ANALOG_INPUT_PORT A7
// The analog input ports used to measure temperature.
#define TEMP_ANALOG_INPUT_PORTS {A0, A1, A2, A3, A4, A5, A6}
// The number of analog input ports used to measure temperature.
#define NUM_TEMP_ANALOG_INPUT_PORTS 7

void setup() {
  // Setup the I2C interface as a slave with the address I2C_ADDR.
  Wire.begin(I2C_ADDR);
  // Register the I2C request handler to be called when the Due requests data.
  Wire.onRequest(I2C_Request_Handler);
  // Configure the analog reference voltage to be 2.56V instead of 5V.
  analogReference(INTERNAL);
}

// Convert an analog sensor value from the analogRead function into a voltage
// value from 0V - 2.56V.
static inline float convert_sensor_value_to_voltage(int analog_sensor_value) {
  // Arduino Micros measure at a 10 bit resolution, meaning there are 1024
  // possible values; with 0 being 0V and 1023 being 2.56V.
  // Note: this is by default 5V refernece, however used analogReference to
  //       change it to 2.56V.
  return analog_sensor_value * (2.56 / 1023.0);
}

// Convert an analog sensor value into a temperature value using 2nd order
// polynomial approximation. Approximation calculated based on Li4P25RT
// datasheet, page 3, only within our expected temperature range of 15C to 60C.
// Accurate within 1C within the expected range. Will not be accurate outside
// of this range.
static inline float convert_sensor_value_to_temp(int analog_sensor_value) {
  float voltage = convert_sensor_value_to_voltage(analog_sensor_value);
  float voltage_squared = voltage * voltage;
  return 62.9036 * voltage_squared - 312.17635 * voltage + 387.51705;
}

// Convert an analog sensor value into a State of Charge value using a linear
// interpolation to get the state of charge from the voltage of the battery
// with the max state of charge (1) when the batteries are at 29.4V and min (0)
// when the batteries are at 17.5V.
// TODO: Update this based on experimental results to use a more accurate
//       model. The real SoC characteristics will depend on the discharge
//       characteristics of the batteries based on their C values.
static inline float convert_sensor_value_to_SoC(int analog_sensor_value) {
  float port_voltage = convert_sensor_value_to_voltage(analog_sensor_value);
  // Assuming that the voltage analog input port is reading the voltage accross
  // a voltage divider with 29.4V corresponding to the maximum value of 2.56V,
  // the battery voltage must be scaled up accordingly.
  float battery_voltage = port_voltage * (29.4 / 2.56);  
  float state_of_charge = 0.084 * battery_voltage - 1.4706;
}

// Callback function for when data is requested from this device by the master.
//  Calculates the temperature and voltage of the battery module and sends it
//  to the master.
void I2C_Request_Handler() {
  // Get the maximum temperature from the temperature sensors.
  //  Temperature goes up as the analog sensor value goes down; thus, need to
  //  find the minimum analog sensor value of the temperature sensors.
  int min_temp_sensor_val = 1023;
  const uint8_t temp_analog_input_ports[] = TEMP_ANALOG_INPUT_PORTS;
  for (int i = 0; i < NUM_TEMP_ANALOG_INPUT_PORTS; i++) {
    int temp_sensor_val = analogRead(temp_analog_input_ports[i]);
    if (temp_sensor_val < min_temp_sensor_val) {
      min_temp_sensor_val = temp_sensor_val;
    }
  }
  float max_battery_temp = convert_sensor_value_to_temp(min_temp_sensor_val);

  // Get the state of charge of the battery module using the battery voltage.
  int voltage_sensor_value = analogRead(VOLTAGE_ANALOG_INPUT_PORT);
  float state_of_charge = convert_sensor_value_to_SoC(voltage_sensor_value);

  // Send the data over the I2C interface.
  //  The data is sent as an array of 8 chars, but is actually an array of 2
  //  floats. Need to be careful on the receiver side.
  float data[] = {max_battery_temp, state_of_charge};
  Wire.write((char *)data, sizeof(data));
}

void loop() {
  // For now the main loop is empty, as the Arduino Micro will only do work if
  // the Arduino Due requests data; however, if the latency is too large, the
  // Arduino Micro could precalculate the data every so often and just send the
  // precalculated data when requested. This will burn more power but will
  // reduce latency. Need to be carefull with interrupts in that case.
}
