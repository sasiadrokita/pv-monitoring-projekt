# Why MQTT? The Role of MQTT in the PV-Monitoring Project

In the PV-Monitoring project, the **MQTT** (Message Queuing Telemetry Transport) protocol serves as a key intermediary (message broker). 

Here is a detailed description of the benefits it brings and how this process physically works in the system.

## 🌟 Advantages of Using MQTT in Your Project

1. **Decoupling of Components**
   The `pv-collector.py` script (responsible for reading data from the physical inverter/meter via Modbus) does not need to know which database the readings go to, what port it runs on, or how to log into it. Its only job is to publish data. This allows individual containers to work completely independently.
   
2. **Exceptional Flexibility and Scalability**
   Thanks to MQTT, if you want to add another system in the future—for example, Smart Home notifications (e.g., Home Assistant) or a simple script that sends an alert to Telegram if the voltage drops—the new element simply subscribes to the `pv/anlage/data` topic. **You do not have to write a single additional line of code in your `pv-collector.py`.**

3. **Lightweight and IoT-Optimized**
   MQTT was created specifically for these kinds of tasks—sending small data packets (e.g., a dozen parameters in JSON format) from end devices. It has very low network overhead.

4. **Stability in Microservices Architecture**
   If for some reason the InfluxDB database experiences a temporary failure or is restarting, the `pv-collector` will still send requests to the Mosquitto broker. This protects the data collection script (which must be called regularly at the `/dev/ttyUSB0` serial ports) from being blocked by write lags to the database itself.

---

## ⚙️ How Does It EXACTLY Work in Your Architecture?

Based on the `docker-compose.yml` file, the communication can be described in the following 5 steps:

1. **Data Collection and Publishing (Publisher)**
   The `pv-collector` container acts as the **Publisher**. It runs a Python script that connects via cable (Modbus: `/dev/ttyUSB0` at 9600 baud) to the inverter/meter, reads raw parameters (e.g., voltage, power, current), and creates a simple JSON object from them. It then connects to the `mosquitto` broker within the Docker network (`pv-net`) and publishes this JSON packet to a specific "topic": `pv/anlage/data`.

2. **Mediation and Sorting (Broker)**
   The `mosquitto` container acts as a **Broker** (a central dispatch) listening on the standard MQTT port `1883`. It does not permanently store these data on disk like a typical database; it simply "knows" that a new message has just been posted to the `pv/anlage/data` topic, and that another container previously asked to listen to this specific topic.

3. **Receiving (Subscriber)**
   The `telegraf` container acts as the **Subscriber**. Telegraf has been instructed in its configuration file to "subscribe" to the `pv/anlage/data` topic at the broker (Mosquitto). As soon as the `pv-collector` publishes something to Mosquitto, Mosquitto immediately pushes this data to Telegraf.

4. **Writing to the Database (InfluxDB)**
   Telegraf is a great tool for forwarding metrics. It takes the raw JSON payload passed by the station (MQTT), formats these metrics appropriately for the optimized time-series database mechanism, and loads them into the `influxdb` container service (on port `8086`, to the designated account `eco-energy-solutions` / `pv_data`).

5. **Visualization (Grafana)**
   At the top of the chain runs `grafana`. Grafana has no concept of the existence of MQTT or Modbus; it only serves "read-only" purposes. Every few seconds, it directly queries the InfluxDB database and draws detailed, interactive dashboards for the user accessing port `3000`.

**Summary of the System Architecture Flow:**
`Physical Meter` ➜ (Modbus RTU) ➜ `pv-collector` ➜ **(MQTT)** ➜ `mosquitto` ➜ **(MQTT)** ➜ `telegraf` ➜ (Influx Protocol) ➜ `influxdb` ➜ (Visualization Query) ➜ `grafana`
