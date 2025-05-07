# 5G OA&M Automation and IP Protocol Simulation Platform

## Overview
This platform provides OA&M automation, KPI monitoring, event simulation, and IP protocol simulation for 5G/LTE networks, with a web dashboard for visualization.

## Project Structure
- `main.py` — Entry point to start the platform
- `platform.py` — Main controller, wires all modules together
- `oam.py` — OA&M automation module
- `kpi.py` — KPI monitoring module
- `event.py` — Event simulation module
- `ip_sim.py` — IP traffic simulation module
- `dashboard.py` — Web dashboard module
- `requirements.txt` — Python dependencies

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the platform:
   ```bash
   python main.py
   ```

## Notes
- The dashboard runs on Streamlit (default port 8501).
- Some features require `scapy` and `streamlit` to be installed.
- Logs are written to `oam_platform.log`.

