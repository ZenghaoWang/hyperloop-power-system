/*
  HV_power_system_mcu

  Monitors the voltage and current of the HV power system and the temperature
  and of the HV batteries; sending this data over the CAN bus.

  Designed to run on an Arduino Due. Should be connected to Arduino Micros
  over I2C, where the Due is the master and the Micros are the slave. Should have
  analog signals coming from different sensors. Should be connected to the CAN
  bus through a CAN transceiver.

  Author: Alexandre Singer
  March 2023
*/

#include "variant.h"
#include <due_can.h>
#include <Wire.h>

// Sends all spoofed data. Used to test the CANBUS when nothing is connected.
#define SEND_FAKE_DATA false
// Puts the MCU into DEMO mode, where only the sensors we are able have live
// during a demo are sent and the rest are spoofed.
#define DEMO_MODE false

// The prescalar for the Real Time Timer (RTT). Currently set to run at 64 Hz.
//      f (Hz) = 0x8000 / RTT_PRESCALER
#define RTT_PRESCALER (0x8000 >> 6)
// The analog input port used to read the current of the HV System.
#define CURRENT_ANALOG_INPUT_PORT A0
// The analog input port used to read the voltage of the HV System.
#define VOLTAGE_ANALOG_INPUT_PORT A1
// The I2C addresses of the slave Arduino monitoring the battery modules.
#define BATTERY_MODULE_MCU_I2C_ADDRS {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
// The number of I2C slaves monitoring the battery modules.
#define NUM_BATTERY_MODULE_MCUS 10
// Multiplier used when converting a voltage divded signal to the original Vin.
//  R1 is the pull up resistor to Vin
//  R2 is the pull down resistor to ground
#define VOLTAGE_DIV_MULT(R1, R2) ((R1 + R2) / R2)
// Multiplier used when a resistor is put in line with a current source
// we wish to read.
//    RES is the resistor's resistance in Ohms
#define CURRENT_RES_MULT(RES) ((6250.0 / RES) - 25.0)

// Flag for when data should be sent over the CAN bus.
volatile int should_send_data = false;

void setup() {
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

void loop() {
  if (should_send_data) {
    // Unset the flag, to allow for another interrupt.
    should_send_data = false;
    
    // Get the battery modules' data.
    int bm_i2c_addrs[] = BATTERY_MODULE_MCU_I2C_ADDRS;
    for (int i = 0; i < NUM_BATTERY_MODULE_MCUS; i++) {
      float battery_module_temp;
      // Note: this function returns the number of bytes returned by the slave, 0 in the event of a timeout.
      uint8_t res = Wire.requestFrom(bm_i2c_addrs[i], sizeof(battery_module_temp));
      while (Wire.available()) {
        Wire.readBytes((char *)(&battery_module_temp), sizeof(battery_module_temp));
      }
      if (SEND_FAKE_DATA || DEMO_MODE) battery_module_temp = 20 + .20 * (float) random(100) / 100.0;
      send_data_over_can_bus(&battery_module_temp, sizeof(float), 0x000 + i, 0);
    }

    // Get the HV System Voltage.
    //  Note: the HV voltage sensor produces a 5V output. Same resistor divider as the 5V buck was used.
    float HV_voltage = VOLTAGE_DIV_MULT(20, 10) * convert_sensor_value_to_voltage(analogRead(VOLTAGE_ANALOG_INPUT_PORT));
    if (SEND_FAKE_DATA || DEMO_MODE) HV_voltage = 288 + 2.88 * (float) random(100) / 100.0;
    send_data_over_can_bus(&HV_voltage, sizeof(float), 0x014, 3);

    // Get the HV System Current.
    float HV_current = CURRENT_RES_MULT(91.6) * convert_sensor_value_to_voltage(analogRead(CURRENT_ANALOG_INPUT_PORT));
    if (SEND_FAKE_DATA || DEMO_MODE) HV_current = 5 + 0.05 * (float) random(100) / 100.0;
    send_data_over_can_bus(&HV_current, sizeof(float), 0x015, 3);
  }
}
