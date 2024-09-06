<a id="readme-top"></a>

<div align="center">
  <h1 align="center">Street Quality Mapper (SQM)</h1>
  <p align="center">
    eYantra Ideas Competition, IIT Bombay, April 2019
    <br />
    <a href="https://ieeexplore.ieee.org/abstract/document/9487763"><strong>Read the research paper.</strong></a>
    <br />
    <br />
  </p>
</div>

## Technologies
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
![NodeMCU](https://img.shields.io/badge/NodeMCU-1957B6?style=for-the-badge)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Firebase](https://img.shields.io/badge/firebase-a08021?style=for-the-badge&logo=firebase&logoColor=ffcd34)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

## Overview
Street Quality Mapper (SQM) is a system designed to identify potholes and map street quality in real-time. The system employs vehicle-mounted sensors to collect data, which is then processed to identify road abnormalities and quantify road quality. SQM offers a cost-effective alternative to manual road inspections providing a comprehensive map of a city's street surface quality and enabling authorities to monitor road conditions, make informed decisions, and improve street quality.

## Features
- **Real-time pothole detection:** Utilizes a 6-axis accelerometer and GPS module to detect potholes based on acceleration fluctuations.
- **Street quality assessment:** Streets are color-coded based on road quality, with potholes plotted on the map for easy visualization.
- **Ride Quality Score:** Calculates a 'Ride Quality Score' based on acceleration data, helping to classify road conditions.
- **Web Interface:** Provides a user-friendly interface with color-coded maps and graphical representations of street quality data.

## Implementation
### Hardware Components
- **NodeMCU with Accelerometer (MPU6050):** Collects acceleration data and sends it to the cloud via a WiFi module.
- **Raspberry Pi 3B+ with GPS Module (Neo6Mv2):** Collects location data and transmits it to the cloud for further processing.

### Software Components
- **Data Processing:** Data collected from the sensors is cleaned, synchronized, and processed to detect potholes using a robust peak detection algorithm based on z-scores.
- **Ride Quality Calculation:** The system calculates the Ride Quality Score using the formula:</br>```RideQualityScore = sqrt(x^2 + y^2 + z^2)```</br>
where x, y, and z are the acceleration values along the three axes.
- **Web Interface:** Displays color-coded maps and provides detailed information on potholes, including timestamps and GPS coordinates.

## How It Works
<div>
  <ol>
    <b><li>Data Collection</li></b>
    Accelerometer data is collected using MPU6050 sensors placed near the axles of the vehicle. GPS data is collected using the Neo6Mv2 module connected to a Raspberry Pi 3B+. Data is sent to a cloud platform (Firebase) in real time.
    <div align="center">
      </br>
      <img width = "720" alt="image" src="https://github.com/user-attachments/assets/0da9034d-5e65-48f1-9ae8-c3c0d1ae1b10">
      <div>Data Collection framework of Street Quality Mapper system.</div>
    </div>
    </br>
    <b><li>Data Processing</li></b>
    Collected data is cleaned and synchronized. A robust peak detection algorithm is applied to identify potholes. Ride Quality Score is calculated based on acceleration values.
    <b><li>Visualization</li></b>
    Streets are color-coded on maps based on their quality. Potholes are plotted on street maps with specific locations. Graphical representations show the number and intensity of potholes.
  </ol>
</div>

## Installation and Setup
- **Hardware Setup:** Attach the accelerometer near the axle of the vehicle's tires and the GPS module in a secure location connected to the Raspberry Pi 3B+.
- **Software Setup:**
  - Install the necessary Python libraries (```pip install -r requirements.txt```).
  - Set up Firebase for real-time data storage.
  - Deploy the web interface on a server.
- **Connectivity:** Ensure a stable internet connection for real-time data transmission to the cloud.
- **API Keys:** Add your Google Maps API keys in place of ```{GOOGLE_MAPS_API_KEY}``` in relevant HTML files.

## Usage
- **Data Collection:** The system automatically collects and sends data to the cloud as the vehicle moves.
- **Pothole Detection:** The system processes the data in real time, detects potholes, and updates the maps accordingly.
- **Web Interface:** Access the web interface to view the mapped potholes, color-coded street quality, and detailed reports.

## Results
The Street Quality Mapper provides:

#### Pothole List
A list of all the potholes recorded 
<div align="center">
</br>
  <img width = "720" alt="image" src="https://github.com/user-attachments/assets/193014dd-ccda-4cd4-afc4-f1384f44a0a9">
  <div>A list of all the potholes recorded along with their time of detection, location, ride quality score, and intensity.</div>
</div>
</br>

#### Color-Coded Maps
Indicating the intensity of potholes with the following color codes:
- Red: High Priority
- Orange: Medium Priority
- Yellow: Lower-Medium Priority
- Green: Lower Priority
<div align="center">
</br>
  <img width = "720" alt="image" src="https://github.com/user-attachments/assets/af41ff4b-f747-44de-a3d0-3514c119010e">
  <div>Map showing multiple color-coded patches of roads.</div>
</div>
</br>

#### Pothole Locations
Marked on the map with details like GPS coordinates and timestamps.
<div align="center">
</br>
  <img width = "720" alt="image" src="https://github.com/user-attachments/assets/2b00ee9d-362b-4f9d-b6be-b1fb4cf8f7c2">
  <div>Map pinpointing locations of potholes in satellite view.</div>
</div>
</br>

#### Cumulative Analysis
Graphical representation of the number and intensity of potholes over time.
<div align="center">
</br>
  <img width = "720" alt="image" src="https://github.com/user-attachments/assets/991ee1bf-5d0a-4fba-be7e-cce06fc0c0ca">
  <div>Accelerometer readings with timestamps. These are used to identify occurrences of potholes.</div>
  </br>
  <img width = "720" alt="image" src="https://github.com/user-attachments/assets/0e3ad41e-a636-461b-9afb-df60dd0b08a6">
  <div>Ride Quality Score (RQS) computed according to the accelerometer readings. The higher the RQS, more is the intensity of the pothole.</div>
  </br>
  <img width = "720" alt="image" src="https://github.com/user-attachments/assets/a72a6b0c-2604-4037-ab1e-2e8bfe5b2a35">
  <div>Number of potholes identified grouped according to their intensity.</div>
</div>
</br>

## Future Work
- **Integration with Transport Services:** Expand data collection by collaborating with services like Ola and Uber.
- **Mobile Sensors:** Replace hardware components with mobile sensors for easier implementation.
- **Machine Learning Integration:** Use machine learning algorithms to improve pothole detection accuracy.
- **Community Access:** Make the data publicly accessible to allow community monitoring.
