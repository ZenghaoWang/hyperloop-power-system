/*
  sensor

  Sends fake sensor data onto the CAN bus periodically to simulate a sensor on the pod.

  The LED on the board will toggle everytime a message is sent onto the bus.

  Alexandre Singer
*/

#include "variant.h"
#include <due_can.h>

// The prescalar for the Real Time Timer (RTT)
//      f (Hz) = 0x8000 / RTT_PRESCALER
#define RTT_PRESCALER 0x8000

// Global variables
unsigned light = HIGH;      // Light used to indicate when data was sent over the bus
volatile bool tick = false; // Tick variable used to indicate when an interrupt occured

// Setup function of the programm, called once at the start
void setup() {
  // Setup the CAN bus
  Can0.begin(CAN_BPS_1000K);

  // Setup the led on the board to blink
  pinMode(LED_BUILTIN, OUTPUT);

  // Setup the Real Time Timer (RTT) on the Due
  RTT_SetPrescaler(RTT, RTT_PRESCALER); // Set the prescaler
  RTT_EnableIT(RTT, RTT_MR_RTTINCIEN);  // Enable the increment interrupt to interrupt everytime the counter increments
  NVIC_EnableIRQ(RTT_IRQn);             // Enable the IRQ on the DUE
}

// IRQ handler for the RTT
// Note: This should be as short as possible and should contain no `wait` calls
void RTT_Handler(void) {
  // Read status to clear IRQ and alarm bits
  RTT_GetStatus( RTT );
  // Set tick to true to be read by the main loop
  tick = true;
}

// Helper function to send data over the CAN bus
void sendData() {
  // Initialize the CAN Frame
  CAN_FRAME outgoing;
  outgoing.id = 0x400;        // The ID of the frame
  outgoing.extended = false;  // Whether the ID is extended or not
  outgoing.priority = 2;      // 0-15 lower is higher priority
  outgoing.length = 8;        // The length of the data in the frame

  // The data field is a maximum of 8 bytes in length
  // Can be accessed in 3 different ways:
  //    1) using .s0 / .s1 / .s2 / .s3 to access each of the 4 (2 byte) words at a time
  outgoing.data.s0 = 0xFEED;        // The first (2 byte) word of data
  //    2) using 'byte' or 'bytes' arrays to access each of the 8 bytes at a time
  outgoing.data.byte[2] = 0xDD;     // The third byte of data
  outgoing.data.byte[3] = 0x55;     // The fourth byte of data
  //    3) using 'low' or 'high' to access the lower or upper 4 bytes respectively
  outgoing.data.high = 0xDEADBEEF;  // The upper 4 bytes of data

  // Send the frame over the bus
  Can0.sendFrame(outgoing);
}

// Main program loop, executing continuously
void loop() {
  // Waits for the tick variable to be set by the RTT IRQ
  if (tick) {
    // Unsets the tick variable
    tick = false;
    // Send data onto the CAN bus
    sendData();
    // Toggle the light
    digitalWrite(LED_BUILTIN, light);   
    if (light == HIGH)
      light = LOW;
    else
      light = HIGH;
  }
}
