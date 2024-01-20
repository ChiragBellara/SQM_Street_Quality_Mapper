#include <ArduinoJson.h>
#include <FirebaseArduino.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <time.h>


#define FIREBASE_AUTH "SpB4u8GxpVzCH4KNxd7BrQPoQjuUNL1yFHQlVTq7" //initializations to connect to firebase
#define FIREBASE_HOST "squid-3349a.firebaseio.com"

const char *ssid =  "Chirag";     // replace with your wifi ssid and wpa2 key
const char *pass =  "chris/7077";

//initialization for getting the time from nodemcu
double timezone = 0*3600;
int dst = 0;
String timestamp;

int count=0;


//Hardware initializations
// MPU6050 Slave Device Address
const uint8_t MPU6050SlaveAddress = 0x68;

// Select SDA and SCL pins for I2C communication 
const uint8_t scl = D6;
const uint8_t sda = D7;

// sensitivity scale factor respective to full scale setting provided in datasheet 
const uint16_t AccelScaleFactor = 16384;
const uint16_t GyroScaleFactor = 131;

// MPU6050 few configuration register addresses
const uint8_t MPU6050_REGISTER_SMPLRT_DIV   =  0x19;
const uint8_t MPU6050_REGISTER_USER_CTRL    =  0x6A;
const uint8_t MPU6050_REGISTER_PWR_MGMT_1   =  0x6B;
const uint8_t MPU6050_REGISTER_PWR_MGMT_2   =  0x6C;
const uint8_t MPU6050_REGISTER_CONFIG       =  0x1A;
const uint8_t MPU6050_REGISTER_GYRO_CONFIG  =  0x1B;
const uint8_t MPU6050_REGISTER_ACCEL_CONFIG =  0x1C;
const uint8_t MPU6050_REGISTER_FIFO_EN      =  0x23;
const uint8_t MPU6050_REGISTER_INT_ENABLE   =  0x38;
const uint8_t MPU6050_REGISTER_ACCEL_XOUT_H =  0x3B;
const uint8_t MPU6050_REGISTER_SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY, AccelZ, Temperature, GyroX, GyroY, GyroZ;


void setup() {

   Serial.begin(9600);
   Serial.println("Connecting to "); 
   Serial.println(ssid); 
  
   WiFi.begin(ssid, pass); //connecting to the WiFi
   while (WiFi.status() != WL_CONNECTED) 
      {
        delay(500);
        Serial.print(".");
      }
  Serial.println("");
  Serial.println("WiFi connected");  //printing status


  //Connecting to firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  if (Firebase.failed()) {
    Serial.print("Error connecting to Firebase: ");
    Serial.println(Firebase.error());
  }

  Wire.begin(sda, scl);
  MPU6050_Init();

  //configurations for timestamp
  configTime(timezone , dst, "pool.nt.org", "time.nist.gov");
  Serial.println("\nWaiting for Internet Time");

  while(!time(nullptr)){
    Serial.print("*");
    delay(100);
  }
  Serial.println("Time Response..... OK");
  delay(20000);

  
}

void loop() {
  
  double Ax, Ay, Az, T, Gx, Gy, Gz;
  
  Read_RawValue(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_XOUT_H); //reading accelerometer values
  
  //divide each with their sensitivity scale factor
  Ax = 9.80665*(double)AccelX/AccelScaleFactor;
  Ay = 9.80665*(double)AccelY/AccelScaleFactor;
  Az = 9.80665*(double)AccelZ/AccelScaleFactor;
//  T = (double)Temperature/340+36.53; //temperature formula
//  Gx = (double)GyroX/GyroScaleFactor;
//  Gy = (double)GyroY/GyroScaleFactor;
//  Gz = (double)GyroZ/GyroScaleFactor;
  
//  Serial.print("Ax: "); Serial.print(Ax);
//  Serial.print(" Ay: "); Serial.print(Ay);
//  Serial.print(" Az: "); Serial.print(Az);
//  Serial.print(" T: "); Serial.print(T);
//  Serial.print(" Gx: "); Serial.print(Gx);
//  Serial.print(" Gy: "); Serial.print(Gy);
//  Serial.print(" Gz: "); Serial.println(Gz);

  //getting the time and converting it into a desirable format
  time_t now = time(nullptr);
  struct tm* p_tm = localtime(&now);
  //Serial.print(p_tm);
  timestamp = (String)p_tm->tm_mday + "/" + (String)(p_tm->tm_mon + 1) + "/" + (String)(p_tm->tm_year + 1900) + " " + (String)p_tm->tm_hour + ":" + (String)(p_tm->tm_min) + ":" + (String)p_tm->tm_sec;
  Serial.println(timestamp);

  firebaseSend(Ax, Ay, Az, timestamp);

  delay(1000);
}


//function to send data to FireBase
void firebaseSend(double Ax, double Ay, double Az, String timestamp){
 
  Firebase.pushFloat("A2/Ax/",Ax);
  if (Firebase.failed()){
    Serial.println("Firebase Failed - x");
  }
  
  Firebase.pushFloat("A2/Ay/",Ay);
  if (Firebase.failed()){
    Serial.println("Firebase Failed - y");
  }
  
  Firebase.pushFloat("A2/Az/",Az);
  if (Firebase.failed()){
    Serial.println("Firebase Failed - z");
  }

  Firebase.pushString("A2/Timestamp/",timestamp);
  if (Firebase.failed()){
    Serial.println("Firebase Failed - timestamp");
  }
  
}

//I2C_Write
void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}

// read all 14 register
void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)14);
  AccelX = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelY = (((int16_t)Wire.read()<<8) | Wire.read());
  AccelZ = (((int16_t)Wire.read()<<8) | Wire.read());
  Temperature = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroX = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroY = (((int16_t)Wire.read()<<8) | Wire.read());
  GyroZ = (((int16_t)Wire.read()<<8) | Wire.read());
}

//configure accelerometer MPU6050
void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SMPLRT_DIV, 0x07);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_1, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_PWR_MGMT_2, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_CONFIG, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_FIFO_EN, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_INT_ENABLE, 0x01);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050SlaveAddress, MPU6050_REGISTER_USER_CTRL, 0x00);
}
