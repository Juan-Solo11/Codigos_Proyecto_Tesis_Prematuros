#include <OneWire.h>
#include <DallasTemperature.h>

#define TEMP_PIN 2   // Pin de la sonda de temperatura
#define BUZZER_PIN 9 // Pin del buzzer

OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

// Secuencia de tonos para alarmas (en Hz)
const int alarmTones[] = {262, 294, 330, 349};
const int numTones = 3;
const int toneDuration = 500;  // 500 ms por tono
const int pauseBetweenTones = 100;  // 100 ms de pausa entre tonos

void playAlarmSequence() {
  for (int i = 0; i < numTones; i++) {
    tone(BUZZER_PIN, alarmTones[i], toneDuration);
    delay(toneDuration + pauseBetweenTones);
  }
  noTone(BUZZER_PIN);
}

void setup() {
  Serial.begin(9600);
  sensors.begin();
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);
  
  Serial.print(temperature);
  Serial.println("C");

  if (temperature >= 38.0 || temperature <= 25.0) {
    playAlarmSequence();
  }

  // Agregar un pequeño delay para estabilidad
  delay(1000);
}