# Raspberry Pi – ESP8266 UDP Control

This project demonstrates UDP-based communication between a Raspberry Pi and an ESP8266 for button-based control and sensor data signaling.

## Overview
- A Raspberry Pi sends START/STOP commands to an ESP8266 via UDP using a physical button.
- The ESP8266 reads a light sensor (photoresistor) and computes a rolling average.
- Averaged sensor values are sent back to the Raspberry Pi over UDP.
- The Raspberry Pi lights up RGB LEDs based on LOW / MEDIUM / HIGH light levels.

This project was completed as part of an embedded systems lab assignment.

## Hardware
- Raspberry Pi  
- ESP8266 (NodeMCU)  
- Photoresistor (LDR)  
- RGB LEDs (Red, Green, Blue)  
- White LED  
- Push button  

## Software
- Python (Raspberry Pi)
- Arduino C++ (ESP8266)
- UDP networking (socket-based communication)

## Project Structure
```
pi-esp8266-udp-control/
├── pi_client.py # Main Raspberry Pi controller
├── pi_button_to_esp.py # Button-triggered UDP sender
├── udp_sender.py # UDP test sender
├── udp_receiver.py # UDP test receiver
├── button_test.py # GPIO button test
├── esp_code/ # ESP8266 Arduino sketches
│ ├── ESP_Server.ino
│ ├── ESP_UDP_Ping.ino
│ ├── ESP_UDP_Receiver.ino
│ ├── ESP_UDP_Sender.ino
│ └── ESP_Wifi_Test.ino
```
