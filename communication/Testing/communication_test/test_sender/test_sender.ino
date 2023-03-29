/*
  test_sender

  Used the test the CANBUS to detect how many errors occur over an extended
  period of time.

  Alexandre Singer
  February 2023
*/

#include "variant.h"
#include <due_can.h>

// The prescalar for the Real Time Timer (RTT)
//      f (Hz) = 0x8000 / RTT_PRESCALER
// Currently set to 512 Hz
#define RTT_PRESCALER 0x8000 >> 9

// Global variables
unsigned light = HIGH;      // Light used to indicate when data was sent over the bus
volatile bool tick = false; // Tick variable used to indicate when an interrupt occured
int char_offset = 0;        // Character offset used to send expected data over the bus

void setup() {
  Can0.begin(CAN_BPS_1000K);

  pinMode(LED_BUILTIN, OUTPUT);

  // Setup the Real Time Timer (RTT) on the Due
  RTT_SetPrescaler(RTT, RTT_PRESCALER); // Set the prescaler
  RTT_EnableIT(RTT, RTT_MR_RTTINCIEN);  // Enable the increment interrupt to interrupt everytime the counter increments
  NVIC_EnableIRQ(RTT_IRQn);             // Enable the IRQ on the DUE
}

// IRQ handler for the RTT
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

  // Populate the next 8 bytes as the next 8 letters of the alphabet
  for (int i = 0; i < 8; i++) {
    outgoing.data.byte[i] = char(char_offset + 65);
    char_offset = (char_offset + 1) % 26;
  }

  // Send the frame over the bus
  Can0.sendFrame(outgoing);
}

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
