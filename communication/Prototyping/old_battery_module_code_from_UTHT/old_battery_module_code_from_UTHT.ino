//SLAVE

// Note: this is the old battery module code provided by UTHT.
// Last updated: May 26, 2021
// Posted by: Natasha Yang

#include <Wire.h>

const int slaveAddress = 1; //Change this depending on Arduino number

float battery = 4.78;

int sensorValue1;
float voltage1;
float temp1;

int sensorValue2;
float voltage2;
float temp2;

int sensorValue3;
float voltage3;
float temp3;

int sensorValue4;
float voltage4;
float temp4;

int sensorValue5;
float voltage5;
float temp5;

int sensorValue6;
float voltage6;
float temp6;

int sensorValue7;
float voltage7;
float temp7;

float dataVoltage[] = {2.44, 2.42, 2.40, 2.38, 2.35, 2.32, 2.27, 2.23, 2.17, 2.11, 2.05, 1.99, 1.92, 1.86, 1.80, 1.74, 1.68, 1.63, 1.59, 1.55, 1.51, 1.48, 1.45, 1.43, 1.40, 1.38, 1.37, 1.35, 1.34, 1.33, 1.32, 1.31, 1.30};
float dataTemperature[] = {-40, -35, -30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120};

char sendTemp[10]={};

float printVoltage(int , int );
float printTemp(float , int );

int sensePin = A0;  //This is the Arduino Pin that will read the sensor output
int sensorInput;    //The variable we will use to store the sensor input
double v;
double actualV;
double vPerCell;
double dischargeC;

char sendSOC[10]={};

char sendAll[10]={};

void setup()
{
  Wire.begin(slaveAddress);
  Wire.onRequest(requestEvent);
  
  Serial.begin(9600);
}

void loop()
{
  sensorValue1 = analogRead(A1);
  voltage1 = printVoltage(sensorValue1, 1);
  temp1 = printTemp(voltage1, 1);
  
  sensorValue2 = analogRead(A2);
  voltage2 = printVoltage(sensorValue2, 2);
  temp2 = printTemp(voltage2, 2);
  
  sensorValue3 = analogRead(A3);
  voltage3 = printVoltage(sensorValue3, 3);
  temp3 = printTemp(voltage3, 3);

  sensorValue4 = analogRead(A4);
  voltage4 = printVoltage(sensorValue4, 4);
  temp4 = printTemp(voltage4, 4);
  
  sensorValue5 = analogRead(A5);
  voltage5 = printVoltage(sensorValue5, 5);
  temp5 = printTemp(voltage5, 5);

  sensorValue6 = analogRead(A6);
  voltage6 = printVoltage(sensorValue6, 6);
  temp6 = printTemp(voltage6, 6);

  sensorValue7 = analogRead(A7);
  voltage7 = printVoltage(sensorValue7, 7);
  temp7 = printTemp(voltage7, 7);
  
  if (temp7 >= temp6 && temp7 >= temp5 && temp7 >= temp4 && temp7 >= temp3 && temp7 >= temp2 && temp7 >= temp1){
  	dtostrf(temp7, 7, 4, sendTemp);
  }
  else if (temp6 >= temp5 && temp6 >= temp4 && temp6 >= temp3 && temp6 >= temp2 && temp6 >= temp1){
  	dtostrf(temp6, 7, 4, sendTemp);
  }
  else if (temp5 >= temp4 && temp5 >= temp3 && temp5 >= temp2 && temp5 >= temp1){
  	dtostrf(temp5, 7, 4, sendTemp);
  }
  else if (temp4 >= temp3 && temp4 >= temp2 && temp4 >= temp1){
    dtostrf(temp4, 7, 4, sendTemp);
  }
  else if (temp3 >= temp2 && temp3 >= temp1){
  	dtostrf(temp3, 7, 4, sendTemp);
  }
  else if (temp3 >= temp1){
  	dtostrf(temp2, 7, 4, sendTemp);
  }
  else {
  	dtostrf(temp1, 7, 4, sendTemp);
  }
  

sensorInput = analogRead(A0);
  v = (double)sensorInput / 1024;   //find percentage of input reading
  v = v * 5;                     //multiply by 5V to get voltage

  actualV = v*10;
  vPerCell = actualV/10;
  
  if(vPerCell >= 3.9){
    dischargeC = 0;
  }
  else if(vPerCell < 3.9 && vPerCell >= 3.85 ){
    dischargeC = 0.1;
  }
  else if(vPerCell < 3.85 && vPerCell >= 3.8 ){
    dischargeC = 0.2;
  }
  else if(vPerCell < 3.8 && vPerCell >= 3.75 ){
    dischargeC = 0.3;
  }
  else if(vPerCell < 3.75 && vPerCell >= 3.72 ){
    dischargeC = 0.4;
  }
  else if(vPerCell < 3.72 && vPerCell >= 3.69 ){
    dischargeC = 0.5;
  }
  else if(vPerCell < 3.69 && vPerCell >= 3.67 ){
    dischargeC = 0.6;
  }
  else if(vPerCell < 3.67 && vPerCell >= 3.62 ){
    dischargeC = 0.7;
  }
  else if(vPerCell < 3.62 && vPerCell >= 3.58 ){
    dischargeC = 0.8;
  }
  else if(vPerCell < 3.58 && vPerCell >= 3.54 ){
    dischargeC = 0.9;
  }
  else if(vPerCell < 3.54 && vPerCell >= 3.51 ){
    dischargeC = 1.0;
  }
  else if(vPerCell < 3.51 && vPerCell >= 3.49 ){
    dischargeC = 1.1;
  }
  else if(vPerCell < 3.49 && vPerCell >= 3.45 ){
    dischargeC = 1.2;
  }
  else if(vPerCell < 3.45 && vPerCell >= 3.41 ){
    dischargeC = 1.3;
  }
  else if(vPerCell < 3.41 && vPerCell >= 3.38 ){
    dischargeC = 1.4;
  }
  else if(vPerCell < 3.38 && vPerCell >= 3.36 ){
    dischargeC = 1.5;
  }
  else if(vPerCell < 3.36 && vPerCell >= 3.33 ){
    dischargeC = 1.6;
  }
  else if(vPerCell < 3.33 && vPerCell >= 3.31 ){
    dischargeC = 1.7;
  }
  else if(vPerCell < 3.31 && vPerCell >= 3.29 ){
    dischargeC = 1.8;
  }
  else if(vPerCell < 3.29 && vPerCell >= 3.27 ){
    dischargeC = 1.9;
  }
  else if(vPerCell < 3.27 && vPerCell >= 3.24 ){
    dischargeC = 2.0;
  }
  else if(vPerCell < 3.24 && vPerCell >= 3.2 ){
    dischargeC = 2.1;
  }
  else if(vPerCell < 3.2 && vPerCell >= 3.15 ){
    dischargeC = 2.2;
  }
  else if(vPerCell < 3.15 && vPerCell >= 3.08 ){
    dischargeC = 2.3;
  }
  else if(vPerCell < 3.08 && vPerCell >= 2.95 ){
    dischargeC = 2.4;
  }
  else if(vPerCell < 2.95){
    dischargeC = 2.5;

  delay(1000);
  }


  Serial.print("Current discharge in Ah is: ");
  Serial.println(dischargeC);

  dtostrf(dischargeC, 7, 4, sendSOC);



  for (int i = 0; i <= 10; i++){
  	sendAll[i] = sendTemp[i];
  }
  
  int j = 0;
  for (int i = 0; i <= 10; i++){
    while (sendAll[j] != NULL){
      j++;
    }
  }
  
  for (int i = 0; i <= 10; i++){
    sendAll[i+j] = sendSOC[i];
  }
  
  sendAll[j] = 's';


}

void requestEvent()
{
  Wire.write(sendTemp);
  Wire.write(sendSOC);
}

float printVoltage(int sensor, int sensorNumb){
	float voltage = sensor * (battery / 1024.0);
  	Serial.print("VoltsA");
  	Serial.print(sensorNumb);
    Serial.print(": ");
  	Serial.println(voltage);
  	return voltage;
}

float printTemp(float voltage, int sensorNumb){
  float temp;
  if (1.30 < voltage && voltage < 2.44)
  {
  	for (int x = 0; x <= 32; x++)
  	{
      if (dataVoltage[x] >= voltage && voltage >= dataVoltage[x+1])
      {
        temp = dataTemperature[x+1] + (voltage - dataVoltage[x+1]) * (dataTemperature[x] - dataTemperature[x+1]) / (dataVoltage[x] - dataVoltage[x+1]);
        Serial.print("TempA");
  		Serial.print(sensorNumb);
   		Serial.print(": ");
       	Serial.println(temp);
      }
  	}
  }
  else
  {
    Serial.print("TempA");
  	Serial.print(sensorNumb);
    Serial.println(": ERROR!");
  }
  return temp;
}


