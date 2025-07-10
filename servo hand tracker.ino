#include <Servo.h>

Servo servo;
bool  attached = false;     // not attached until first command

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (!Serial.available()) return;

  int c = Serial.peek();             // first byte
  if (c < '0' || c > '9') {          // discard non-digits
    Serial.read();
    return;
  }

  int angle = Serial.parseInt();     // read full number
  if (angle < 0 || angle > 180) return;

  if (!attached) {                   // first ever command
    servo.attach(9);                 // start PWM only now
    attached = true;
  }
  servo.write(angle);                // update position
}