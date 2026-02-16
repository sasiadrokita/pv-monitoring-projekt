# PV Monitoring System

This project monitors a Photovoltaic (PV) system by collecting real-time data from an **Eastron SDM120** energy meter via Modbus RTU and visualizing it in Grafana.

## Architecture

The system runs as a Docker stack on a Raspberry Pi:

1.  **pv-collector**: Python service that reads data from the meter (Voltage, Current, Power, Energy) via USB/RS485 adapter (`/dev/ttyUSB0`) using `minimalmodbus` library.
2.  **Mosquitto**: MQTT Broker handling message distribution.
3.  **Telegraf**: Subscribes to MQTT topics (`pv/anlage/data`) and writes data to InfluxDB.
4.  **InfluxDB**: Time-series database storing historical metrics.
5.  **Grafana**: Visualization platform for dashboards.

## Hardware Requirements

- Raspberry Pi (3/4/Zero 2 W) with Docker installed.
- USB to RS485 Adapter (FTDI or CH340 based).
- Eastron SDM120 Modbus Energy Meter.
- Twisted pair cable for RS485 connection.

## Configuration

### Environment Variables
Key settings in `docker-compose.yml`:
- `MODBUS_PORT`: `/dev/ttyUSB0`
- `MODBUS_BAUDRATE`: `9600` (Default for SDM120)
- `MQTT_TOPIC`: `pv/anlage/data`

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd PV-monitoring
    ```

2.  **Start the stack**:
    ```bash
    docker compose up -d --build
    ```

3.  **Access Grafana**:
    - URL: `http://<raspberry-pi-ip>:3000`
    - Default Credentials: `admin` / `admin` (change on first login).

## Troubleshooting

- **Check Logs**: `docker logs pv-collector`
- **Verify USB**: Ensure adapter is visible as `/dev/ttyUSB0`.
- **Test Modbus**: Use `test_modbus.py` (if available) to diagnose connection issues.
