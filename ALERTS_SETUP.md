# Guide: Setting Up System Health Alerts via Telegram

This guide explains how to configure Grafana to send critical alerts to a Telegram bot if the monitoring system stops sending data. This serves as a "heartbeat" monitor, notifying you of potential system failures (e.g., Raspberry Pi crash, Docker container failure, or network issues).

## Part 1: Create a Telegram Bot

1.  **Talk to `@BotFather`**: In the Telegram app, search for `@BotFather` and start a chat.
2.  **Create a new bot**: Send the command `/newbot`. Follow the prompts to choose a name and a username for your bot.
3.  **Save your API Token**: `@BotFather` will give you a unique API Token. Save it securely.
4.  **Get your Chat ID**: Search for `@userinfobot`, start a chat, and it will immediately send you your numeric `Chat ID`. Save it.
5.  **Start your bot**: Find your newly created bot in Telegram and send it a message (e.g., `/start`) to initiate the chat.

## Part 2: Configure Grafana Contact Point

1.  In your Grafana instance, navigate to **Alerting** (bell icon) -> **Contact points**.
2.  Click **`+ Add contact point`**.
3.  **Name** it (e.g., `Telegram Alerts`).
4.  Add a new **Integration**, select `Telegram`.
5.  Paste your **Bot API Token** and **Chat ID** into the respective fields.
6.  Use the **`Test`** button to send a test notification. You should receive a message on Telegram.
7.  **Save** the contact point.
8.  (Recommended) Go to the **Notification policies** tab and set your new `Telegram Alerts` contact point as the **Default contact point**.

## Part 3: Create the "No Data" Alert Rule

This rule will trigger if no new data arrives from the PV system for a specified duration.

1.  In Grafana, navigate to **Alerting** (bell icon) -> **Alert rules**.
2.  Click **`+ New alert rule`**.
3.  **Configure the query:**
    -   **Query A (InfluxDB):** Use the code editor to paste the following Flux query. It checks for data in the last 2 minutes.
        ```flux
        from(bucket: "pv_data")
          |> range(start: -2m)
          |> filter(fn: (r) => r["_measurement"] == "mqtt_consumer")
          |> filter(fn: (r) => r["_field"] == "leistung_W")
          |> last()
        ```
    -   **Expression B (Reduce):** Click `+ Expression`.
        -   **Function:** `Count`
        -   **Input:** `A`
    -   **Condition:** Select `Classic condition`.
        -   Set the condition to: `WHEN` `last()` `OF` `B` `IS BELOW` `1`.

4.  **Define alert evaluation behavior:**
    -   Set **`Evaluate every`** to `1m`.
    -   Set **`For`** to `1m` (to avoid false positives).
    -   Under **"Configure no data and error handling"**, set both `If no data` and `If execution error` to **`Alerting`**. This is crucial.

5.  **Add details:**
    -   Give the rule a **Name**, e.g., `Critical: No Data from PV System`.
    -   Add a **Summary** and **Description** for the notification message. Example:
        -   **Summary**: `System Health Alert: No data received from PV system!`
        -   **Description**: `The system has not sent any new data for over 2 minutes. Please check the status of the Raspberry Pi and Docker containers.`

6.  **Save and exit** the rule.

Your system is now actively monitored. To test it, you can stop the simulator container (`docker stop pv-simulator`). You should receive an alert on Telegram within a few minutes.
