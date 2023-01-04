/*
  sensor

  Sends fake sensor data onto the CAN bus to simulate a sensor on the pod.

  Alexandre Singer
*/

#include "variant.h"
#include <due_can.h>

unsigned light;

void setup() {
  Can0.begin(CAN_BPS_250K);

  // Debug: setup the led on the board to blink
  pinMode(LED_BUILTIN, OUTPUT);
  light = HIGH;
}

void sendData()
{
	CAN_FRAME outgoing;
	outgoing.id = 0x400;
	outgoing.extended = false;
	outgoing.priority = 4; // 0-15 lower is higher priority
	
  outgoing.length = 8;
	outgoing.data.s0 = 0xFEED;
  outgoing.data.byte[2] = 0xDD;
	outgoing.data.byte[3] = 0x55;
	outgoing.data.high = 0xDEADBEEF;
	Can0.sendFrame(outgoing);
}

void loop() {
  static unsigned long lastTime = 0;
  if ((millis() - lastTime) > 1000) {
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
