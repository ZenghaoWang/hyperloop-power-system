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
  January 2023
*/

#include "variant.h"
#include <Wire.h>
#include <due_can.h>

// The prescalar for the Real Time Timer (RTT). Currently set to run at 64 Hz.
//      f (Hz) = 0x8000 / RTT_PRESCALER
#define RTT_PRESCALER (0x8000 >> 0)
// The analog input port used to read the current of the LV Battery.
#define CURRENT_ANALOG_INPUT_PORT A0
// The analog input port used to read the voltage of the LV System.
#define VOLTAGE_ANALOG_INPUT_PORT A1
// The analog input port used to read the temperature of the PCB.
#define TEMP_ANALOG_INPUT_PORT A2

double randMToN(double M, double N)
{
  return M + (rand() / (RAND_MAX / (N - M)));
}

void setup()
{
  Serial.begin(9600);
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
void RTT_Handler(void)
{
  // Read status to clear IRQ and alarm bits
  RTT_GetStatus(RTT);
  // Set flag to true to be read by the main loop
}

static void send_data_over_can_bus(void *data, size_t length, uint32_t id,
                                   uint8_t priority)
{
  CAN_FRAME frame;
  frame.extended = false;
  frame.id = id;
  frame.priority = priority;
  frame.length = length;
  memcpy(frame.data.bytes, data, length);
  Can0.sendFrame(frame);
}

void loop()
{

  if (Serial.available() > 0)
  {
    char incoming_byte = Serial.read();
    if (incoming_byte != '\n' && incoming_byte != '\0')
    {
      Serial.print(incoming_byte);
    }
  }
  // Get the battery module data.
  float battery_module_temp = randMToN(40, 60);
  send_data_over_can_bus(&battery_module_temp, sizeof(float), 0x100, 0);
  Serial.println(battery_module_temp);

  // Get the LV Battery Current.
  float LV_current = randMToN(100, 150);
  send_data_over_can_bus(&LV_current, sizeof(float), 0x102, 4);
  Serial.println(LV_current);

  // Get the LV System Voltage.
  float LV_voltage = randMToN(200, 250);
  send_data_over_can_bus(&LV_voltage, sizeof(float), 0x103, 4);
  Serial.println(LV_voltage);

  // Get the LV PCB Temperature.
  float PCB_temp = randMToN(20, 40);
  send_data_over_can_bus(&PCB_temp, sizeof(float), 0x104, 7);
  Serial.println(PCB_temp);
}
