/*
  battery_module_mcu

  Monitors the temperature and voltage of the battery module within the UTHT
  Hyperloop pod.

  Designed to run on an Arduino Micro, communicates directly with an Arduino Due
  over I2C (the Micro is the slave and the Due is the master).
*/

#include <Wire.h>

// The address of this device on the I2C interface.
//   Will be different for EACH Arduino Micro.
//   Can be any value from 0 - 127 (7-bit address).
#define I2C_ADDR 0
// The analog input port used to measure the voltage.
#define VOLTAGE_ANALOG_INPUT_PORT A7
// The number of analog input ports used to measure temperature.
#define NUM_TEMP_ANALOG_INPUT_PORTS 7
// The analog input ports used to measure temperature.
//  Used to simply iterate over the sensors when needed.
const uint8_t temp_analog_input_ports[] = {A0, A1, A2, A3, A4, A5, A6};

void setup() {
  // Setup the I2C interface as a slave with the address I2C_ADDR.
  Wire.begin(I2C_ADDR);
  // Register the I2C request handler to be called when the Due requests data.
  Wire.onRequest(I2C_Request_Handler);
  // Setup the analog input ports for temperate.
  for (int i = 0; i < NUM_TEMP_ANALOG_INPUT_PORTS; i++) {
    pinMode(temp_analog_input_ports[i], INPUT);    
  }
  // Setup the analog input port for voltage.
  pinMode(VOLTAGE_ANALOG_INPUT_PORT, INPUT);
}

// Convert an analog sensor value from the analogRead function into a voltage value from 0V - 5V.
static float convert_analog_sensor_value_to_voltage(int analog_sensor_value) {
  // Arduino Micros measure at a 10 bit resolution, meaning there are 1024 possible values;
  // with 0 being 0V and 1023 being 5V.
  return analog_sensor_value * (5.0 / 1023.0);
}

// Convert an analog sensor value into a temperature value using 3rd order polynomial
// approximation with 99.72% accuracy, based on data provided by UTHT.
//  temp = -225.7 * v^3 + 1310.6 * v^2 - 2594.8 * v + 1767.8
// TODO: Double check the data provided is accurate.
static float convert_analog_sensor_value_to_temp(int analog_sensor_value) {
  float voltage = convert_analog_sensor_value_to_voltage(analog_sensor_value);
  float voltage_squared = voltage * voltage;
  float voltage_cubed = voltage_squared * voltage;
  return -225.7 * voltage_cubed + 1310.6 * voltage_squared - 2594.8 * voltage + 1767.8;
}

// Callback function for when data is requested from this device by the master.
// Calculates the temperature and voltage of the battery module and sends it to the master.
void I2C_Request_Handler() {
  // Get the maximum temperature from the 7 temperature sensors.
  int max_temp_analog_sensor_val = 0;
  for (int i = 0; i < NUM_TEMP_ANALOG_INPUT_PORTS; i++) {
    int temp_analog_sensor_val = analogRead(temp_analog_input_ports[i]);
    if (temp_analog_sensor_val > max_temp_analog_sensor_val) {
      max_temp_analog_sensor_val = temp_analog_sensor_val;
    }
  }
  float max_battery_temp = convert_analog_sensor_value_to_temp(max_temp_analog_sensor_val);

  // Get the voltage of the battery module.
  //  According to UTHT, the voltage of the battery can be found by multiplying the
  //  voltage of the sensor by 5.
  // TODO: Double check that this is accurate.
  // TODO: We really want the state of charge. Need a formula to convert the battery
  //       voltage to state of charge.
  int battery_analog_sensor_value = analogRead(VOLTAGE_ANALOG_INPUT_PORT);
  float battery_voltage = convert_analog_sensor_value_to_voltage(battery_analog_sensor_value) * 5.0;

  // Send the data over the I2C interface.
  // The data is sent as an array of 8 chars, but is actually an array of 2 floats.
  // Needs to be careful on the receiver side.
  float data[] = {max_battery_temp, battery_voltage};
  Wire.write((char *)data, sizeof(data));
}

void loop() {
  // For now the main loop is empty, as the Arduino Micro will only do work if the
  // Arduino Due requests data; however, if the latency is too large, the Arduino
  // Micro could precalculate the data every so often and just send the precalculated
  // data when requested. This will burn more power but will reduce latency. Need to
  // be carefull with interrupts in that case.
}
