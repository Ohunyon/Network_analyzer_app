# Network Traffic Analyzer

A real-time network traffic analyzer that monitors packets, detects malicious traffic, and generates detailed reports with visualizations.

## Features

- Real-time packet capture and analysis
- Machine learning-based threat detection
- Live web interface with real-time updates
- Detailed PDF reports with charts and visualizations
- JSON reports for data analysis
- Traffic statistics and monitoring
- Top malicious source tracking

## Requirements

- Python 3.10 or lower
- Virtual environment
- Root privileges (for packet capture)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application (requires root privileges for packet capture):
```bash
sudo venv/bin/python src/main.py
```

2. Access the web interface:
- Open your browser and navigate to `http://localhost:8000`
- Click "Start Capture" to begin monitoring network traffic
- Use the "Generate Report" button to create PDF/JSON reports

## Features Description

### Real-time Monitoring
- Live packet capture and analysis
- Instant threat detection
- Real-time statistics updates

### Web Interface
- Clean, intuitive dashboard
- Live traffic display
- Traffic statistics
- Report generation controls

### Reports
- Comprehensive PDF reports with:
  - Traffic distribution charts
  - Top malicious sources visualization
  - Summary statistics
  - Security recommendations
- JSON reports for data analysis

### Security Features
- Machine learning-based threat detection
- Malicious traffic identification
- Source IP tracking
- Protocol analysis

## Project Structure

```
project/
├── src/
│   ├── main.py           # Main application file
│   ├── packet_capture.py # Packet capture functionality
│   ├── predictor.py      # ML prediction module
│   ├── pdf_report.py     # PDF report generation
│   └── static/           # Web interface files
├── model/                # ML model files
├── reports/             # Generated reports
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Notes

- The application requires root privileges to capture network packets
- Reports are saved in the `reports/` directory
- Both PDF and JSON formats are available for reports
- The web interface automatically updates in real-time

## Troubleshooting

1. If you get permission errors:
   - Ensure you're running with sudo
   - Verify network interface permissions

2. If the web interface doesn't load:
   - Check if the server is running
   - Verify the port (8000) is available

3. If packet capture doesn't start:
   - Ensure you have root privileges
   - Check network interface availability
