/*
  SoftwareSwitchTest

  A simple script used to test the software switch.
*/

void setup() {
  // Setup the Serial lines
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char incoming_byte = Serial.read();
    if (incoming_byte == 'y') {
      digitalWrite(2, HIGH);
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("Pin Set to High");
    } else if (incoming_byte == 'n') {
      digitalWrite(2, LOW);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("Pin Set to Low");
    }
  }
}
