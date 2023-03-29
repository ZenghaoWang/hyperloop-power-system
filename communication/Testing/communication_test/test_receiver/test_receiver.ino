/*
  test_receiver

  Listens on the CAN bus and prints what it hears to the Serial output.

  Alexandre Singer
  February 2023
*/

#include <due_can.h>

#define Serial SerialUSB

void setup() {
  // Set up the serial interface
  Serial.begin(9600);

  // Set up the can bus interface to run at 1000 Kbps
  Can0.begin(CAN_BPS_1000K);

  // Setup the CAN mailboxes
  for (int filter = 0; filter < 7; filter++) {
    Can0.setRXFilter(filter, 0, 0, false);    
  }
}

void printFrame(CAN_FRAME &frame) {
  for (int count = 0; count < frame.length; count++) {
    char c = frame.data.bytes[count];
    Serial.print(c);
  }
}

void loop() {
  CAN_FRAME incoming;
  if (Can0.available() > 0) {
    Can0.read(incoming); 
    printFrame(incoming);
  }
}
