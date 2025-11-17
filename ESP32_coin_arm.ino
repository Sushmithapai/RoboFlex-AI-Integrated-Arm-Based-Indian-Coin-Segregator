#include <ESP32Servo.h>

// Servo objects
Servo base, shoulder, elbow;

// Servo control pins
const int basePin = 25;
const int shoulderPin = 27;
const int elbowPin = 14;
const int relay = 32;

void setup() {
  Serial.begin(115200);

  base.setPeriodHertz(50);
  shoulder.setPeriodHertz(50);
  elbow.setPeriodHertz(50);

  base.attach(basePin, 500, 2400);
  shoulder.attach(shoulderPin, 500, 2400);
  elbow.attach(elbowPin, 500, 2400);

  pinMode(relay, OUTPUT);

  Serial.println("Ready.....");
}

void loop() {
  if (Serial.available()) {
    int command = Serial.parseInt();

    if (command == 1) {
      pickObject();
      delay(2000);
      digitalWrite(relay, HIGH);
      delay(500);
      liftObject();
      delay(1000);
      base.write(45);
      delay(1000);
      pickObject();
      delay(2000);
      digitalWrite(relay, LOW);
      delay(500);
      liftObject();
      delay(1000);
      base.write(0);
    } else if (command == 2) {
      pickObject();
      delay(2000);
      digitalWrite(relay, HIGH);
      delay(500);
      liftObject();
      delay(1000);
      base.write(90);
      delay(1000);
      pickObject();
      delay(2000);
      digitalWrite(relay, LOW);
      delay(500);
      liftObject();
      delay(1000);
      base.write(0);
    }else if (command == 3) {
      pickObject();
      delay(1000);
      digitalWrite(relay, HIGH);
      delay(500);
      liftObject();
      delay(1000);
      base.write(125);
      delay(1000);
      pickObject();
      delay(1000);
      digitalWrite(relay, LOW);
      delay(500);
      liftObject();
      delay(1000);
      base.write(0);
    }else if (command == 4) {
      pickObject();
      delay(1000);
      digitalWrite(relay, HIGH);
      delay(500);
      liftObject();
      delay(1000);
      base.write(180);
      delay(1000);
      pickObject();
      delay(1000);
      digitalWrite(relay, LOW);
      delay(500);
      liftObject();
      delay(1000);
      base.write(0);
    }else {
      Serial.println("Invalid input. Enter 1 to pick and lift.");
    }

    while (Serial.available()) Serial.read(); // Clear serial buffer
  }
}

void pickObject() {
  Serial.println("Picking object...");

  shoulder.write(180);
  Serial.println("Shoulder at 180°");

  delay(500);

  elbow.write(20);
  Serial.println("Elbow at 20°");

  delay(100);
}

void liftObject() {
  Serial.println("Lifting object...");
  shoulder.write(90);
  Serial.println("Shoulder at 90°");

   delay(500);

  elbow.write(60);
  Serial.println("Elbow at 60°");
}
