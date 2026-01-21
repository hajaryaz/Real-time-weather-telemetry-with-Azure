# Real-time Weather Telemetry with Azure
Azure | IoT | Cloud Computing

## Table of Contents
- [Project Description](#project-description)
- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## Project Description
A real-time weather monitoring system leveraging Microsoft Azure IoT services to collect, process, and visualize meteorological data. The solution demonstrates:

- Real-time telemetry ingestion from simulated IoT devices
- Edge computing capabilities with containerized processing
- Cloud-native data pipeline architecture
- Live dashboard visualization with synchronized time display

## Key Features
- **Real-time Weather Data Pipeline**: Continuous ingestion and processing of meteorological telemetry
- **Azure IoT Edge Integration**: Local data preprocessing at the network edge
- **Cloud-Based Analytics**: SQL-like stream processing with Azure Stream Analytics
- **Dynamic Visualization**: Real-time Power BI dashboard with synchronized clock display
- **Secure Communication**: Encrypted device-to-cloud messaging with authentication
- **Containerized Deployment**: Docker-based module deployment via Azure Container Registry

## Architecture Overview
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────┐
│  Python-based   │────▶│   Azure IoT Hub │────▶│  Azure IoT Edge     │
│  Weather Sensor │     │  (Cloud Gateway)│     │  (Edge Processing)  │
└─────────────────┘     └─────────────────┘     └─────────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────┐
│  Power BI       │◀────│ Azure Stream    │◀────│  Processed          │
│  Dashboard      │     │ Analytics       │     │  Telemetry          │
└─────────────────┘     └─────────────────┘     └─────────────────────┘
```

## Technologies Used
### Cloud Services:
- **Azure IoT Hub** (Device connectivity and messaging)
- **Azure IoT Edge** (Edge computing platform)
- **Azure Container Registry** (Docker image management)
- **Azure Stream Analytics** (Real-time data processing)
- **Azure Virtual Machines** (Edge runtime hosting)
- **Power BI** (Real-time visualization)

### Programming & Tools:
- **Python 3** (Sensor simulation and module development)
- **Docker** (Containerization)
- **OpenWeather API** (Weather data source)
- **MQTT/HTTP Protocols** (Device communication)
- **Azure CLI** (Resource management)
- **SSH** (Remote VM access)

## Requirements
- Active Azure subscription with IoT Hub permissions
- Python 3.8 or higher
- Docker Desktop (for local container testing)
- OpenWeather API key (free tier available)
- Power BI account
- Azure CLI installed locally

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/marouaa145/azuredev-8a05.git
cd azure-iot-weather-telemetry
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Fill in your credentials:
# OPENWEATHER_API_KEY=your_api_key_here
# IOTHUB_CONNECTION_STRING=your_iothub_connection_string
# ACR_LOGIN_SERVER=your_acr_login_server
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
# Key packages: azure-iot-device, azure-iot-hub, requests, python-dotenv
```

4. **Set up Azure resources**:
```bash
# Create resource group
az group create --name WeatherTelemetryRG --location eastus

# Create IoT Hub
az iot hub create --name WeatherIoTHub --resource-group WeatherTelemetryRG --sku S1

# Create Container Registry
az acr create --name WeatherACR --resource-group WeatherTelemetryRG --sku Basic

# Create IoT Edge device
az iot hub device-identity create --hub-name WeatherIoTHub --device-id weather-edge-device --edge-enabled
```

5. **Deploy IoT Edge runtime to VM**:
```bash
# Create Ubuntu VM with IoT Edge
az vm create --resource-group WeatherTelemetryRG \
  --name IoTEdgeVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B1s
```

6. **Build and push Docker module**:
```bash
# Build the weather module image
docker build -t weathermodule:1.0 .

# Tag for ACR
docker tag weathermodule:1.0 weatheracr.azurecr.io/weathermodule:1.0

# Push to ACR
docker push weatheracr.azurecr.io/weathermodule:1.0
```

7. **Configure Stream Analytics job**:
- Create Stream Analytics job in Azure portal
- Set IoT Hub as input
- Configure Power BI workspace as output
- Deploy the following query:
```sql
SELECT
    deviceId,
    temperature,
    humidity,
    windSpeed,
    weatherCondition,
    EventProcessedUtcTime
INTO
    [powerbi-output]
FROM
    [iothub-input]
```

## Usage

### 1. Start the IoT Edge runtime on VM:
```bash
ssh azureuser@<vm-public-ip>
sudo systemctl start iotedge
sudo iotedge list  # Verify modules are running
```

### 2. Deploy weather module to Edge device:
- Navigate to IoT Hub → IoT Edge → your device
- Add module with image: `weatheracr.azurecr.io/weathermodule:1.0`
- Set environment variables for OpenWeather API
- Apply deployment

### 3. Monitor data flow:
```bash
# View module logs
sudo iotedge logs weathermodule -f

# Monitor IoT Hub messages
az iot hub monitor-events --hub-name WeatherIoTHub --device-id weather-edge-device
```

### 4. Start Stream Analytics job:
- In Azure portal, navigate to Stream Analytics job
- Click "Start" to begin processing
- Verify data is flowing to Power BI

### 5. Access the dashboard:
- Open Power BI service
- Navigate to your workspace
- Open "Weather Dashboard" report
- Data should refresh automatically every few seconds

### Real-time Dashboard Features:
- Live temperature gauge with color-coded alerts
- Humidity percentage display
- Wind speed and direction indicators
- Synchronized digital clock with NTP accuracy
- Historical weather trends chart
- Location-based weather condition icons

## Example Dashboard View
The Power BI dashboard displays:
<img width="1473" height="769" alt="image" src="https://github.com/user-attachments/assets/db2cb8d0-ae62-486b-9c2d-a0ced4acf864" />


## Contact
For project inquiries or technical support:

**Project Team:**

- @marouaa145
- @ELyazri Hajar



---

*This project demonstrates a complete IoT-to-cloud pipeline using Microsoft Azure services, showcasing edge computing, real-time analytics, and cloud-native architecture patterns for weather monitoring applications.*
