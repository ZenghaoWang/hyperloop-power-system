/*
  listener

  Listens on the CAN bus and prints what it hears to the Serial output.

  This will act as the Test Computer in our prototype.

  Alexandre Singer
*/

#include <due_can.h>

#define Serial SerialUSB

void setup() {
  // Set up the serial interface
  Serial.begin(115200);

  // Set up the can bus interface to run at 1000 Kbps
  Can0.begin(CAN_BPS_1000K);

  // There are 7 mailboxes for each device that are RX boxes.
  // Set each mailbox to have an open filter that will accept standard
  // (non-extended) frames only.
  // Standard frames allow for an 11-bit identifier allowing for a total of 
  // 2048 different.
  // Extended frames allow for a 29-bit identifier allowing for a total of
  // 536+ million messages.
  for (int filter = 0; filter < 7; filter++) {
    Can0.setRXFilter(filter, 0, 0, false);    
  }
}

void printFrame(CAN_FRAME &frame) {
  Serial.print("ID: 0x");
  Serial.print(frame.id, HEX);
  Serial.print(" Len: ");
  Serial.print(frame.length);
  Serial.print(" Data: 0x");
  for (int count = 0; count < frame.length; count++) {
    Serial.print(frame.data.bytes[count], HEX);
    Serial.print(" ");
  }
  Serial.print("\r\n");
}

void loop(){
  CAN_FRAME incoming;

  if (Can0.available() > 0) {
    Can0.read(incoming); 
    printFrame(incoming);
  }
}
