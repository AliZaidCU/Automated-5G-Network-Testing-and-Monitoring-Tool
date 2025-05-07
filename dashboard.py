import threading
import time
import logging
import json
from datetime import datetime
import os

try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

logger = logging.getLogger("OAM-Platform")

class Dashboard:
    """Web Dashboard for the 5G OA&M Platform"""
    def __init__(self, platform):
        self.platform = platform
        self.running = False
        self.port = 8501
        self.refresh_interval = 10  # seconds
        self.cache = {
            "last_update": None,
            "platform_status": None,
            "alarms": [],
            "kpi_summary": {},
            "events": [],
            "ip_stats": {}
        }
    def start(self):
        if self.running:
            return
        self.running = True
        logger.info("Starting Web Dashboard")
        if not STREAMLIT_AVAILABLE:
            logger.warning("Streamlit not available. Running in limited mode.")
            return
        threading.Thread(target=self._run_dashboard, name="dashboard-thread", daemon=True).start()
        threading.Thread(target=self._update_data_loop, name="dashboard-data-thread", daemon=True).start()
    def stop(self):
        self.running = False
        logger.info("Stopped Web Dashboard")
    def get_status(self):
        return {
            "status": "running" if self.running else "stopped",
            "streamlit_available": STREAMLIT_AVAILABLE,
            "port": self.port,
            "last_update": self.cache["last_update"].isoformat() if self.cache["last_update"] else None
        }
    def _update_data_loop(self):
        logger.info("Starting dashboard data update loop")
        while self.running:
            try:
                self._update_dashboard_data()
                self._save_cache_to_files()
                time.sleep(self.refresh_interval)
            except Exception as e:
                logger.error(f"Error updating dashboard data: {str(e)}")
                time.sleep(5)
    def _update_dashboard_data(self):
        logger.info("Updating dashboard data")
        self.cache["last_update"] = datetime.now()
        self.cache["platform_status"] = self.platform.get_status()
        if "oam" in self.platform.components:
            self.cache["alarms"] = self.platform.components["oam"].get_alarms()
        if "kpi" in self.platform.components:
            self.cache["kpi_summary"] = self.platform.components["kpi"].get_kpi_summary()
        if "event" in self.platform.components:
            self.cache["events"] = self.platform.components["event"].get_events()
        if "ip" in self.platform.components:
            self.cache["ip_stats"] = self.platform.components["ip"].get_status()
    def _save_cache_to_files(self):
        try:
            with open("dashboard_cache_platform_status.json", "w") as f:
                json.dump(self.cache["platform_status"], f)
            with open("dashboard_cache_alarms.json", "w") as f:
                json.dump(self.cache["alarms"], f)
            with open("dashboard_cache_kpi_summary.json", "w") as f:
                json.dump(self.cache["kpi_summary"], f)
            with open("dashboard_cache_events.json", "w") as f:
                json.dump(self.cache["events"], f)
            with open("dashboard_cache_ip_stats.json", "w") as f:
                json.dump(self.cache["ip_stats"], f)
            logger.info("Saved cache data to files")
        except Exception as e:
            logger.error(f"Error saving cache to files: {str(e)}")
    def _run_dashboard(self):
        if not STREAMLIT_AVAILABLE:
            logger.warning("Cannot run dashboard: Streamlit not available")
            return
        script_path = "dashboard_app.py"
        with open(script_path, "w") as f:
            f.write("""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime, timedelta
import os
# ... (dashboard Streamlit code omitted for brevity; see original for full code) ...
""")
        os.system(f"streamlit run {script_path} --server.port={self.port}")
