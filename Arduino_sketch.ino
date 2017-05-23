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
int voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;
boolean isbmp = true;
void setup() {
	Serial.begin(9600);
	pinMode(ledPower,OUTPUT);
	
	dht.begin();
	if(!bmp.begin()){
	isbmp = false;
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
      	  Serial.print(0.00);
      	  Serial.print(";");
      	  Serial.print(0.00);
          Serial.print(";");

	}else{
	  Serial.print(h);
	  Serial.print(";");
	  Serial.print(t);
          Serial.print(";");
	}
	if(isbmp){
          Serial.print(bmp.readTemperature());
          Serial.print(";");
          Serial.print(bmp.readPressure());
          Serial.print(";");
        }else{
          Serial.print(0.00);
          Serial.print(";");
          Serial.print(0.00);
          Serial.print(";");
        }
          Serial.print(dustDensity);
          Serial.println();
        
	delay(1000);
}

