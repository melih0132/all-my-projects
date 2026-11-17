# IoT Spy Game

MQTT sensor and server lab (spy/capture style game loop).

## Overview

Python clients publish/subscribe over MQTT.

## Stack

- Python 3, MQTT

## Layout

```
iot-spy-game/
├── capteur.py
├── server.py
├── cleanup_mqtt.py
└── requirements.txt
```

## Run

```bash
pip install -r requirements.txt
python server.py
python capteur.py
```
