import logging
from oam import OAMAutomation
from kpi import KPIMonitoring
from event import EventSimulator
from ip_sim import IPTrafficSimulator
from dashboard import Dashboard
from datetime import datetime

logger = logging.getLogger("OAM-Platform")

class OAMPlatform:
    """Main controller for the 5G OA&M Automation Platform"""
    def __init__(self):
        logger.info("Initializing 5G OA&M Automation Platform")
        self.running = False
        self.components = {}
        self.initialize_components()
    def initialize_components(self):
        logger.info("Loading platform components...")
        self.components["oam"] = OAMAutomation()
        self.components["kpi"] = KPIMonitoring()
        self.components["event"] = EventSimulator()
        self.components["ip"] = IPTrafficSimulator()
        self.components["dashboard"] = Dashboard(self)
        logger.info("All components initialized successfully")
    def start(self):
        if self.running:
            logger.warning("Platform is already running")
            return
        logger.info("Starting 5G OA&M Platform")
        self.running = True
        for name, component in self.components.items():
            component.start()
            logger.info(f"Started {name} component")
        logger.info("Platform started successfully")
    def stop(self):
        if not self.running:
            logger.warning("Platform is not running")
            return
        logger.info("Stopping 5G OA&M Platform")
        self.running = False
        for name, component in self.components.items():
            component.stop()
            logger.info(f"Stopped {name} component")
        logger.info("Platform stopped successfully")
    def get_status(self):
        status = {
            "platform": "running" if self.running else "stopped",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        for name, component in self.components.items():
            status["components"][name] = component.get_status()
        return status 