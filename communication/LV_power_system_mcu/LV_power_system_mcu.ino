/*
  LV_power_system_mcu

  Monitors the voltage and current of the LV power system and the temperature
  and state of charge of the LV battery; sending this data over the CAN bus.
  Based on commands coming from the serial USB connection, controls the source
  of the LV power through the software switch and controls the enable signals
  of the buck converters.

  Designed to run on an Arduino Due. Should be connected to an Arduino Micro
  over I2C, where the Due is the master and the Micro is the slave. Should have
  analog signals coming from different sensors. Should be connected to the CAN
  bus through a CAN transceiver. Should be connected to a serial USB cable over
  its serial USB interface.

  Author: Alexandre Singer
  March 2023
*/

#include "variant.h"
#include <due_can.h>
#include <Wire.h>

// The baud rate of the serial connection
#define SERIAL_BAUD_RATE 9600
// The prescalar for the Real Time Timer (RTT). Currently set to run at 64 Hz.
//      f (Hz) = 0x8000 / RTT_PRESCALER
#define RTT_PRESCALER (0x8000 >> 6)
// The digital output port used to close the software switch.
#define SWITCH_DIGITAL_OUTPUT_PORT 2
// The digital output port used to enable the different Bucks
#define BUCK_A_EN_DIGITAL_OUTPUT_PORT 3
#define BUCK_B_EN_DIGITAL_OUTPUT_PORT 4
#define BUCK_C_EN_DIGITAL_OUTPUT_PORT 5
#define BUCK_D_EN_DIGITAL_OUTPUT_PORT 6
// The analog input port used to read the current of the LV Battery.
#define CURRENT_ANALOG_INPUT_PORT A0
// The analog input port used to read the voltage of the LV System.
#define VOLTAGE_ANALOG_INPUT_PORT A1
// The analog input port used to read the temperature of the PCB.
#define TEMP_ANALOG_INPUT_PORT A2
// The I2C address of the slave Arduino monitoring the battery module.
#define BATTERY_MODULE_MCU_I2C_ADDR 0

// Flag for when data should be sent over the CAN bus.
volatile int should_send_data = false;

void setup() {
  // Setup Serial communication.
  Serial.begin(SERIAL_BAUD_RATE);
  // Setup the CAN bus.
  Can0.begin(CAN_BPS_1000K);
  // Setup I2C communication with this device as the master.
  Wire.begin();  
  // Setup the Real Time Timer (RTT) on the Due by setting the prescaler,
  // enabling interrupts on increments of the counter, and enabling the IRQ.
  RTT_SetPrescaler(RTT, RTT_PRESCALER);
  RTT_EnableIT(RTT, RTT_MR_RTTINCIEN);
  NVIC_EnableIRQ(RTT_IRQn);
  // Set the analog read resolution to 12 bits. Arduino Dues can read with a
  // resolution of up to 12 bits, but for compatibility reasons defaults to 10.
  analogReadResolution(12);
  // Set the switch and buck enable digital pins to output.
  pinMode(SWITCH_DIGITAL_OUTPUT_PORT, OUTPUT);
  pinMode(BUCK_A_EN_DIGITAL_OUTPUT_PORT, OUTPUT);
  pinMode(BUCK_B_EN_DIGITAL_OUTPUT_PORT, OUTPUT);
  pinMode(BUCK_C_EN_DIGITAL_OUTPUT_PORT, OUTPUT);
  pinMode(BUCK_D_EN_DIGITAL_OUTPUT_PORT, OUTPUT);
  // Set the switch and buck enables to their default values.
  digitalWrite(SWITCH_DIGITAL_OUTPUT_PORT, LOW);      // Switch off by default
  digitalWrite(BUCK_A_EN_DIGITAL_OUTPUT_PORT, HIGH);  // Buck enabled by default
  digitalWrite(BUCK_B_EN_DIGITAL_OUTPUT_PORT, HIGH);
  digitalWrite(BUCK_C_EN_DIGITAL_OUTPUT_PORT, HIGH);
  digitalWrite(BUCK_D_EN_DIGITAL_OUTPUT_PORT, HIGH);
}

// IRQ handler for the RTT
void RTT_Handler(void) {
  // Read status to clear IRQ and alarm bits
  RTT_GetStatus( RTT );
  // Set flag to true to be read by the main loop
  should_send_data = true;
}

// Convert an analog sensor value from the analogRead function into a voltage
// value from 0V - 3.3V.
static inline float convert_sensor_value_to_voltage(int analog_sensor_value) {
  // Arduino Dues use an analog to digitial converter with a 12 bit resolution,
  // meaning there are 4096 possible values; with 0 being 0V and 4095 being
  // 3.3V.
  // Note: the Arduino Due uses 10 bit resolution by default, used the
  //       analogReadResolution function to use more bits to get higher
  //       precision.
  // Note: the analogReference() function is ignored on ArduinoDues, therefore
  //       the voltage on the pins cannot exceed 3.3V.
  return analog_sensor_value * (3.3 / 4095.0);
}

// TODO: Need more information on the current sensor. For now this function
//       just returns the voltage on the analog port.
static inline float convert_sensor_value_to_current(int analog_sensor_value) {
  float port_voltage = convert_sensor_value_to_voltage(analog_sensor_value);
  return port_voltage;
}

// TODO: Need more information on the voltage sensor. For now this function
//       just returns the voltage on the analog port.
static inline float convert_sensor_value_to_ext_voltage(int analog_sensor_value) {
  float port_voltage = convert_sensor_value_to_voltage(analog_sensor_value);
  return port_voltage;
}

// TODO: Need more information on the temperature sensor on the PCB. For now
//       this function just returns the voltage on the analog port.
static inline float convert_sensor_value_to_temp(int analog_sensor_value) {
  float port_voltage = convert_sensor_value_to_voltage(analog_sensor_value);
  return port_voltage;
}

// Helper method for sending data over the CAN bus.
//  data: pointer the data payload to send
//  length: length of the payload (must be 8 or less)
//  id: frame ID for the payload
//  priority: frame priority
static void send_data_over_can_bus(void *data, size_t length, uint32_t id, uint8_t priority) {
  CAN_FRAME frame;
  frame.extended = false;
  frame.id = id;
  frame.priority = priority;
  frame.length = length;
  memcpy(frame.data.bytes, data, length);
  Can0.sendFrame(frame);
}

// Helper function to handle serial commands from the master computer.
//    Capital letters are for enable, lower case letters are for disable
//        S(s): Software Switch Enable (Close)
//        A(a): Buck A enable (disable)
//        B(b): Buck B enable (disable)
//        C(c): Buck C enable (disable)
//        D(d): Buck D enable (disable)
static inline bool handle_serial_request(char incoming_byte) {
  bool error = false;
  switch(incoming_byte) {
    case 'S': // Enable (close) Software Switch
      digitalWrite(SWITCH_DIGITAL_OUTPUT_PORT, HIGH);
      break;
    case 's': // Disable (open) Software Switch
      digitalWrite(SWITCH_DIGITAL_OUTPUT_PORT, LOW);
      break;
    case 'A': // Buck A enable
      digitalWrite(BUCK_A_EN_DIGITAL_OUTPUT_PORT, HIGH);
      break;
    case 'a': // Buck A disable
      digitalWrite(BUCK_A_EN_DIGITAL_OUTPUT_PORT, LOW);
      break;
    case 'B': // Buck B enable
      digitalWrite(BUCK_B_EN_DIGITAL_OUTPUT_PORT, HIGH);
      break;
    case 'b': // Buck B disable
      digitalWrite(BUCK_B_EN_DIGITAL_OUTPUT_PORT, LOW);
      break;
    case 'C': // Buck C enable
      digitalWrite(BUCK_C_EN_DIGITAL_OUTPUT_PORT, HIGH);
      break;
    case 'c': // Buck C disable
      digitalWrite(BUCK_C_EN_DIGITAL_OUTPUT_PORT, LOW);
      break;
    case 'D': // Buck D enable
      digitalWrite(BUCK_D_EN_DIGITAL_OUTPUT_PORT, HIGH);
      break;
    case 'd': // Buck D disable
      digitalWrite(BUCK_D_EN_DIGITAL_OUTPUT_PORT, LOW);
      break;
    default: // Anything else
      error = true;
      break;
  }
  return error;
}

void loop() {
  // Check for a Serial request from the master computer
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incoming_byte = Serial.read();
    // Handle the request
    //    Note: ignore terminators which may signify end of message.
    if (incoming_byte != '\n' && incoming_byte != '\0') {
      bool error = handle_serial_request(incoming_byte);
      // Send response
      //    A: Acknowledge; message received and acted upon
      //    N: No-Acknowledge; message invalid
      if (!error) {
        Serial.print("A");
      } else {
        Serial.print("N");
      }
    }
  }

  // Send data over the CAN Bus.
  if (should_send_data) {
    // Unset the flag, to allow for another interrupt.
    should_send_data = false;
    
    // Get the battery module data.
    float battery_module_temp;
    // Note: this function returns the number of bytes returned by the slave, 0 in the event of a timeout.
    uint8_t res = Wire.requestFrom(BATTERY_MODULE_MCU_I2C_ADDR, sizeof(battery_module_temp));
    while (Wire.available()) {
      Wire.readBytes((char *)(&battery_module_temp), sizeof(battery_module_temp));
    }
    send_data_over_can_bus(&battery_module_temp, sizeof(float), 0x100, 0);

    // Get the LV Battery Current.
    float LV_current = convert_sensor_value_to_current(analogRead(CURRENT_ANALOG_INPUT_PORT));
    send_data_over_can_bus(&LV_current, sizeof(float), 0x102, 4);

    // Get the LV System Voltage.
    float LV_voltage = convert_sensor_value_to_ext_voltage(analogRead(VOLTAGE_ANALOG_INPUT_PORT));
    send_data_over_can_bus(&LV_voltage, sizeof(float), 0x103, 4);

    // Get the LV PCB Temperature.
    float PCB_temp = convert_sensor_value_to_temp(analogRead(TEMP_ANALOG_INPUT_PORT));
    send_data_over_can_bus(&PCB_temp, sizeof(float), 0x104, 7);
  }
}
