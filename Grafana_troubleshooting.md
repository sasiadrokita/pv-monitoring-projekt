
### 1. Grafana is Unreachable or in a Restart Loop

**Symptom:**
You cannot access the Grafana dashboard at `http://<your-pi-ip>:3000`. The browser shows "This site can’t be reached". When you run `docker ps`, you see that the `grafana` container has a status of `Restarting`.

**Diagnosis:**
This almost always indicates a file permission issue. The Grafana process inside the container does not have permission to write to its data directory, which is mapped to a folder on the host system.

To confirm, check the container's logs:
```bash
docker logs grafana


#SOLUTION:

# Ensure you are in the root directory of the project
sudo chown -R 472:472 docker/grafana/data
docker restart grafana
docker ps


