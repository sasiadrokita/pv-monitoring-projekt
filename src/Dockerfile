# Schritt 1: Basis-Image auswählen
# Wir verwenden ein schlankes Python-Image, um die Größe gering zu halten.
FROM python:3.9-slim

# Schritt 2: Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Schritt 3: Abhängigkeiten kopieren und installieren
# Wir kopieren zuerst nur die requirements.txt, um den Docker-Cache optimal zu nutzen.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Schritt 4: Den Quellcode der Anwendung kopieren
COPY src/ .

# Schritt 5: Den Befehl zum Starten der Anwendung definieren
# Dieser Befehl wird ausgeführt, wenn der Container startet.
CMD ["python", "pv_simulator.py"]
