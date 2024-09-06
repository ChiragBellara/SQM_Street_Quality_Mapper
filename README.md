<a id="readme-top"></a>

<div align="center">
  <h1 align="center">SQM - Street Quality Mapper</h1>
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
Street Quality Mapper (SQM) is an IoT-based system designed to detect potholes and assess overall street quality in real time. It uses signal processing techniques to analyze acceleration fluctuations and determine road quality, providing a comprehensive map of a city's street surface conditions.

The system employs vehicle-mounted sensors to collect data, which is then processed to identify road abnormalities and quantify road quality. SQM offers a cost-effective alternative to manual road inspections, enabling efficient prioritization of road repairs. By providing a holistic view of road infrastructure health, SQM supports urban planners, transportation departments, and emergency services in improving road safety and maintenance strategies.

## Features
- Real-time pothole detection
- Street quality assessment
- GPS-based location tracking
- Color-coded street quality mapping
- Cumulative analysis of pothole data
- Web interface for data visualization

## Components
### Hardware Components
- 6-axis accelerometer (MPU6050)
- GPS module (Neo6Mv2)
- NodeMCU controller
- Raspberry Pi 3B+
- WiFi module
### Software Components
- Data collection and processing scripts
- Pothole detection algorithm
- Web interface for data visualization

## How It Works
<div>
  <ol>
    <b><li>Data Collection</li></b>
    Accelerometer data is collected using MPU6050 sensors placed near the axles of the vehicle. GPS data is collected using the Neo6Mv2 module connected to a Raspberry Pi 3B+. Data is sent to a cloud platform (Firebase) in real time.
    <b><li>Data Processing</li></b>
    Collected data is cleaned and synchronized. A robust peak detection algorithm is applied to identify potholes. Ride Quality Score is calculated based on acceleration values.
    <b><li>Visualization</li></b>
    Streets are color-coded on maps based on their quality. Potholes are plotted on street maps with specific locations. Graphical representations show the number and intensity of potholes.
  </ol>
</div>
