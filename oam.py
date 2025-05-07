import threading
import time
import random
import logging
from datetime import datetime
from enum import Enum

logger = logging.getLogger("OAM-Platform")

class AlarmSeverity(Enum):
    CRITICAL = 1
    MAJOR = 2
    MINOR = 3
    WARNING = 4
    INDETERMINATE = 5
    CLEARED = 6

class AlarmType(Enum):
    COMMUNICATIONS = 1
    QUALITY_OF_SERVICE = 2
    PROCESSING_ERROR = 3
    EQUIPMENT = 4
    ENVIRONMENTAL = 5
    SECURITY = 6

class OAMAutomation:
    """OA&M Automation module for 5G/LTE networks"""
    def __init__(self):
        self.running = False
        self.health_check_interval = 60  # seconds
        self.fault_gen_interval = 300  # seconds
        self.log_parse_interval = 30  # seconds
        self.alarms = {}
        self.alarm_id_counter = 1
        self.network_nodes = [
            {"id": "gnb-001", "type": "gNB", "ip": "10.0.1.1", "status": "active"},
            {"id": "gnb-002", "type": "gNB", "ip": "10.0.1.2", "status": "active"},
            {"id": "amf-001", "type": "AMF", "ip": "10.0.2.1", "status": "active"},
            {"id": "smf-001", "type": "SMF", "ip": "10.0.2.2", "status": "active"},
            {"id": "upf-001", "type": "UPF", "ip": "10.0.3.1", "status": "active"},
            {"id": "pcf-001", "type": "PCF", "ip": "10.0.3.2", "status": "active"},
        ]
    def start(self):
        if self.running:
            return
        self.running = True
        logger.info("Starting OA&M Automation module")
        threading.Thread(target=self._health_check_loop, name="health-check-thread", daemon=True).start()
        threading.Thread(target=self._fault_generation_loop, name="fault-gen-thread", daemon=True).start()
        threading.Thread(target=self._log_parsing_loop, name="log-parse-thread", daemon=True).start()
    def stop(self):
        self.running = False
        logger.info("Stopped OA&M Automation module")
    def get_status(self):
        return {
            "status": "running" if self.running else "stopped",
            "active_alarms": len(self.alarms),
            "network_nodes": len(self.network_nodes),
            "healthy_nodes": sum(1 for node in self.network_nodes if node["status"] == "active")
        }
    def _health_check_loop(self):
        logger.info("Starting health check loop")
        while self.running:
            logger.info("Performing health check on network nodes")
            for node in self.network_nodes:
                cpu_usage = random.uniform(10, 95)
                memory_usage = random.uniform(20, 90)
                disk_usage = random.uniform(30, 85)
                logger.info(f"Node {node['id']} health: CPU={cpu_usage:.1f}%, Memory={memory_usage:.1f}%, Disk={disk_usage:.1f}%")
                if cpu_usage > 90:
                    self._create_alarm(node_id=node["id"], alarm_type=AlarmType.PROCESSING_ERROR, severity=AlarmSeverity.MAJOR, description=f"High CPU usage: {cpu_usage:.1f}%")
                if memory_usage > 85:
                    self._create_alarm(node_id=node["id"], alarm_type=AlarmType.PROCESSING_ERROR, severity=AlarmSeverity.WARNING, description=f"High memory usage: {memory_usage:.1f}%")
                if disk_usage > 80:
                    self._create_alarm(node_id=node["id"], alarm_type=AlarmType.EQUIPMENT, severity=AlarmSeverity.MINOR, description=f"High disk usage: {disk_usage:.1f}%")
            time.sleep(self.health_check_interval)
    def _fault_generation_loop(self):
        logger.info("Starting fault generation loop")
        fault_types = [
            {"type": "node_down", "probability": 0.05},
            {"type": "service_timeout", "probability": 0.1},
            {"type": "memory_overflow", "probability": 0.07},
            {"type": "connection_failure", "probability": 0.15},
            {"type": "authentication_failure", "probability": 0.03},
        ]
        while self.running:
            logger.info("Checking for random fault generation")
            for node in self.network_nodes:
                for fault in fault_types:
                    if random.random() < fault["probability"]:
                        logger.info(f"Generating {fault['type']} fault for node {node['id']}")
                        if fault["type"] == "node_down":
                            node["status"] = "down"
                            self._create_alarm(node_id=node["id"], alarm_type=AlarmType.EQUIPMENT, severity=AlarmSeverity.CRITICAL, description=f"Node {node['id']} is down")
                        elif fault["type"] == "service_timeout":
                            self._create_alarm(node_id=node["id"], alarm_type=AlarmType.QUALITY_OF_SERVICE, severity=AlarmSeverity.MAJOR, description=f"Service timeout on {node['id']}")
                        elif fault["type"] == "memory_overflow":
                            self._create_alarm(node_id=node["id"], alarm_type=AlarmType.PROCESSING_ERROR, severity=AlarmSeverity.MAJOR, description=f"Memory overflow on {node['id']}")
                        elif fault["type"] == "connection_failure":
                            self._create_alarm(node_id=node["id"], alarm_type=AlarmType.COMMUNICATIONS, severity=AlarmSeverity.MINOR, description=f"Connection failure on {node['id']}")
                        elif fault["type"] == "authentication_failure":
                            self._create_alarm(node_id=node["id"], alarm_type=AlarmType.SECURITY, severity=AlarmSeverity.WARNING, description=f"Authentication failure on {node['id']}")
            for node in self.network_nodes:
                if node["status"] == "down" and random.random() < 0.3:
                    logger.info(f"Node {node['id']} recovered")
                    node["status"] = "active"
                    for alarm_id, alarm in list(self.alarms.items()):
                        if (alarm["node_id"] == node["id"] and alarm["description"] == f"Node {node['id']} is down"):
                            self._clear_alarm(alarm_id)
            time.sleep(self.fault_gen_interval)
    def _log_parsing_loop(self):
        logger.info("Starting log parsing loop")
        log_patterns = [
            {"pattern": "authentication failed", "alarm_type": AlarmType.SECURITY, "severity": AlarmSeverity.WARNING},
            {"pattern": "connection timed out", "alarm_type": AlarmType.COMMUNICATIONS, "severity": AlarmSeverity.MINOR},
            {"pattern": "service unavailable", "alarm_type": AlarmType.QUALITY_OF_SERVICE, "severity": AlarmSeverity.MAJOR},
            {"pattern": "out of memory", "alarm_type": AlarmType.PROCESSING_ERROR, "severity": AlarmSeverity.CRITICAL},
            {"pattern": "temperature exceeds threshold", "alarm_type": AlarmType.ENVIRONMENTAL, "severity": AlarmSeverity.MAJOR},
        ]
        while self.running:
            for _ in range(random.randint(5, 15)):
                node = random.choice(self.network_nodes)
                log_entry = self._generate_mock_log(node)
                for pattern in log_patterns:
                    if pattern["pattern"] in log_entry["message"].lower():
                        logger.info(f"Found pattern '{pattern['pattern']}' in log from {node['id']}")
                        self._create_alarm(node_id=node["id"], alarm_type=pattern["alarm_type"], severity=pattern["severity"], description=f"Log pattern match: {pattern['pattern']}")
            time.sleep(self.log_parse_interval)
    def _generate_mock_log(self, node):
        log_types = [
            "INFO: Normal operation",
            "INFO: Service started",
            "INFO: Connection established",
            "WARNING: High resource usage",
            "WARNING: Authentication failed",
            "ERROR: Connection timed out",
            "ERROR: Service unavailable",
            "CRITICAL: Out of memory",
            "CRITICAL: Temperature exceeds threshold"
        ]
        return {
            "timestamp": datetime.now().isoformat(),
            "node_id": node["id"],
            "node_type": node["type"],
            "message": random.choice(log_types),
            "source": f"{node['type']}-service"
        }
    def _create_alarm(self, node_id, alarm_type, severity, description):
        alarm_id = self.alarm_id_counter
        self.alarm_id_counter += 1
        alarm = {
            "id": alarm_id,
            "node_id": node_id,
            "type": alarm_type.name,
            "severity": severity.name,
            "description": description,
            "raised_time": datetime.now().isoformat(),
            "status": "active"
        }
        self.alarms[alarm_id] = alarm
        logger.warning(f"ALARM RAISED: {severity.name} - {description} on {node_id}")
        return alarm_id
    def _clear_alarm(self, alarm_id):
        if alarm_id in self.alarms:
            alarm = self.alarms[alarm_id]
            alarm["status"] = "cleared"
            alarm["cleared_time"] = datetime.now().isoformat()
            logger.info(f"ALARM CLEARED: {alarm['severity']} - {alarm['description']} on {alarm['node_id']}")
            return True
        return False
    def get_alarms(self, filter_status=None):
        if filter_status:
            return {k: v for k, v in self.alarms.items() if v["status"] == filter_status}
        return self.alarms 