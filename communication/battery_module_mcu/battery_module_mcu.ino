/*
  battery_module_mcu

  Monitors the temperature of the battery module within the UTHT Hyperloop pod.

  Designed to run on an Arduino Micro, communicates directly with an Arduino
  Due over I2C (the Micro is the slave and the Due is the master).

  Author: Alexandre Singer
  February 2023
*/

#include <Wire.h>

// The address of this device on the I2C interface.
//   Will be different for EACH Arduino Micro.
//   Can be any value from 0 - 127 (7-bit address).
#define I2C_ADDR 0
// The analog input ports used to measure temperature.
#define TEMP_ANALOG_INPUT_PORTS {A0, A1, A2, A3, A4, A5, A6}
// The number of analog input ports used to measure temperature.
#define NUM_TEMP_ANALOG_INPUT_PORTS 7
// The timer compare match register
//  ((16*10^6) / (desired_freq * 1024)) - 1
//  Note: must be less than 65536. 
//  Currently set to 64 Hz.
#define TIMER_CMP_MATCH_REG 243

// Global variables for interrupts
volatile int check_temps = true;
volatile float max_battery_temp = 0;

void setup() {
  // Setup the I2C interface as a slave with the address I2C_ADDR.
  Wire.begin(I2C_ADDR);
  // Register the I2C request handler to be called when the Due requests data.
  Wire.onRequest(I2C_Request_Handler);

  // Configure the analog reference voltage to be 2.56V instead of 5V.
  analogReference(INTERNAL);
  
  // Set up timer interrupts
  // https://www.instructables.com/id/Arduino-Timer-Interrupts/
  cli();//stop interrupts
  //set timer1 interrupt at 64Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 64hz increments
  OCR1A = TIMER_CMP_MATCH_REG;
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei();//allow interrupts
}

// Timer 1 interrupt handler.
//  Sets the check temps flag to true.
ISR(TIMER1_COMPA_vect){
  check_temps = true;  
}

// Callback function for when data is requested from this device by the master.
//  Sends the precalculated max battery temp to the Master.
void I2C_Request_Handler() {
  Wire.write((char *)(&max_battery_temp), sizeof(float));
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

// Main program loop. Mostly sits idle; however, when the timer interrupt sets
// the check_temps to true, this code will set the max_battery_temp variable
// with the current max battery temperature.
void loop() {  
  if (check_temps) {
    // Reset the check temperature flag
    check_temps = false;
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
    max_battery_temp = convert_sensor_value_to_temp(min_temp_sensor_val);
  }
}
