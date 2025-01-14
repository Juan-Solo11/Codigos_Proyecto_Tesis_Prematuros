#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Configuración del LCD I2C (dirección 0x20)
LiquidCrystal_I2C lcd(0x20, 16, 2);

// Pines y variables
#define TMP36_PIN A2
#define BUZZER_PIN 9
float temperature = 0.0;

void setup() {
  // Inicializar el LCD
  lcd.init();
  lcd.backlight();

  // Configurar el buzzer
  pinMode(BUZZER_PIN, OUTPUT);

  // Mensaje de inicio
  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
  delay(2000);
  lcd.clear();
}

void loop() {
  // Leer la temperatura del sensor TMP36
  int sensorValue = analogRead(TMP36_PIN);
  temperature = (sensorValue * 5.0 / 1023.0 - 0.5) * 100.0;

  // Mostrar la temperatura en el LCD
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C   ");

  // Activar alarma si la temperatura está fuera de rango
  if (temperature < 36.5 || temperature > 37.2) {
    activateBuzzer();
    lcd.setCursor(0, 1);
    lcd.print("Alarma Temp!");
  } else {
    noTone(BUZZER_PIN);
    lcd.setCursor(0, 1);
    lcd.print("Temp OK      ");
  }

  delay(500);
}

// Función para activar el buzzer con 3 tonos
void activateBuzzer() {
  tone(BUZZER_PIN, 1000, 300);
  delay(300);
  tone(BUZZER_PIN, 1500, 300);
  delay(300);
  tone(BUZZER_PIN, 2000, 300);
  delay(300);
}