/*
  sensor

  Sends fake sensor data onto the CAN bus to simulate a sensor on the pod.

  The LED on the board will toggle everytime a message is sent onto the bus.

  Alexandre Singer
*/

#include "variant.h"
#include <due_can.h>

// The delay between sending sensor data to the CAN bus in milliseconds.
#define DELAY_IN_MS 1000

unsigned light;

void setup() {
  Can0.begin(CAN_BPS_1000K);

  // Debug: setup the led on the board to blink
  pinMode(LED_BUILTIN, OUTPUT);
  light = HIGH;
}

void sendData()
{
  CAN_FRAME outgoing;
  outgoing.id = 0x400;        // The ID of the frame
  outgoing.extended = false;  // Whether the ID is extended or not
  outgoing.priority = 2;      // 0-15 lower is higher priority
  outgoing.length = 8;        // The length of the data in the frame

  // The data field is a maximum of 8 bytes in length
  // Can be accessed in 3 different ways:
  //    1) using .s0 / .s1 / .s2 / .s3 to access each of the 4 (2 byte) words at a time
  outgoing.data.s0 = 0xFEED;        // The first word of data
  //    2) using 'byte' or 'bytes' arrays to access each of the 8 bytes at a time
  outgoing.data.byte[2] = 0xDD;
  outgoing.data.byte[3] = 0x55;
  //    3) using 'low' or 'high' to access the lower or upper 4 bytes respectively
  outgoing.data.high = 0xDEADBEEF;

  // Send the frame over the bus
  Can0.sendFrame(outgoing);
}

void loop() {
  static unsigned long lastTime = 0;
  if ((millis() - lastTime) > DELAY_IN_MS) {
    lastTime = millis();
    sendData();
    // Toggle the light
    digitalWrite(LED_BUILTIN, light);   
    if (light == HIGH)
      light = LOW;
    else
      light = HIGH;
  }
}
