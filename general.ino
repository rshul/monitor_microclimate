#include "DHT.h" //for DHT

#include <Wire.h> // for bmp
#include <Adafruit_BMP085.h> // for bmp

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;
int measurePin = A0;
int ledPower = 12;
unsigned int samplingTime = 280;
unsigned int deltaTime = 40;
unsigned int sleepTime = 9680;
float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

void setup() {
	Serial.begin(9600);
	pinMode(ledPower,OUTPUT);
	
	dht.begin();
	if(!bmp.begin()){
	Serial.println("Could not find a valid BMP085 sensor");
	while(1);
	}
}
void loop(){
	digitalWrite(ledPower, LOW);
	delayMicroseconds(samplingTime);
	voMeasured = analogRead(measurePin);
	delayMicroseconds(deltaTime);
	digitalWrite(ledPower, HIGH);
	delayMicroseconds(sleepTime);
	
	calcVoltage = voMeasured * (5.0/1024);
	dustDensity = 0.17 * calcVoltage - 0.1;
	if(dustDensity < 0){
		dustDensity = 0.0;
	}
	
	float h = dht.readHumidity();
	float t = dht.readTemperature();
	if(isnan(t) || isnan(h)){
	Serial.println("Failed to read from DHT");

	}else{
	Serial.print("Humidity: ");
	Serial.println(h);
	Serial.print("Temperature: ");
	Serial.println(t);
	}
	Serial.print("Temperature = ");
	Serial.println(bmp.readTemperature());
	Serial.print("Pressure = ");
	Serial.println(bmp.readPressure());
	Serial.println("Dust Density: ");
	Serial.println(dustDensity);
	Serial.println();
	delay(1000);
}

