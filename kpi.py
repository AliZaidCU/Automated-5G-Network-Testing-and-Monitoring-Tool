import threading
import time
import random
import logging
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json

logger = logging.getLogger("OAM-Platform")

class KPIMonitoring:
    """KPI Monitoring Framework for 5G/LTE networks"""
    def __init__(self):
        self.running = False
        self.collection_interval = 60  # seconds
        self.kpi_definitions = [
            {"id": "node_availability", "name": "Node Availability", "description": "Percentage of time a node is available", "unit": "%", "target": 99.99, "warning_threshold": 99.9, "critical_threshold": 99.5, "category": "availability"},
            {"id": "service_latency", "name": "Service Latency", "description": "Average latency for service requests", "unit": "ms", "target": 50, "warning_threshold": 100, "critical_threshold": 200, "category": "performance"},
            {"id": "error_rate", "name": "Error Rate", "description": "Percentage of requests resulting in errors", "unit": "%", "target": 0.1, "warning_threshold": 1.0, "critical_threshold": 5.0, "category": "quality"},
            {"id": "cpu_utilization", "name": "CPU Utilization", "description": "Average CPU utilization of nodes", "unit": "%", "target": 60, "warning_threshold": 80, "critical_threshold": 90, "category": "resource"},
            {"id": "memory_utilization", "name": "Memory Utilization", "description": "Average memory utilization of nodes", "unit": "%", "target": 70, "warning_threshold": 85, "critical_threshold": 95, "category": "resource"},
            {"id": "throughput", "name": "Network Throughput", "description": "Average network throughput", "unit": "Mbps", "target": 1000, "warning_threshold": 500, "critical_threshold": 100, "category": "performance"},
            {"id": "connection_success_rate", "name": "Connection Success Rate", "description": "Percentage of successful connection attempts", "unit": "%", "target": 99.9, "warning_threshold": 99.0, "critical_threshold": 95.0, "category": "quality"},
            {"id": "recovery_time", "name": "Recovery Time", "description": "Average time to recover from failures", "unit": "seconds", "target": 30, "warning_threshold": 60, "critical_threshold": 300, "category": "availability"}
        ]
        self.kpi_data = {kpi["id"]: defaultdict(lambda: deque(maxlen=1000)) for kpi in self.kpi_definitions}
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
        logger.info("Starting KPI Monitoring Framework")
        threading.Thread(target=self._collection_loop, name="kpi-collection-thread", daemon=True).start()
    def stop(self):
        self.running = False
        logger.info("Stopped KPI Monitoring Framework")
    def get_status(self):
        return {
            "status": "running" if self.running else "stopped",
            "kpi_count": len(self.kpi_definitions),
            "node_count": len(self.network_nodes),
            "data_points": sum(len(data) for kpi_id, node_data in self.kpi_data.items() for node_id, data in node_data.items())
        }
    def _collection_loop(self):
        logger.info("Starting KPI collection loop")
        while self.running:
            logger.info("Collecting KPI data")
            for node in self.network_nodes:
                self._collect_node_kpis(node)
            self._analyze_kpi_data()
            time.sleep(self.collection_interval)
    def _collect_node_kpis(self, node):
        node_id = node["id"]
        timestamp = datetime.now().isoformat()
        availability = 100.0 if node["status"] == "active" else 0.0
        self.kpi_data["node_availability"][node_id].append({"timestamp": timestamp, "value": availability})
        cpu_util = random.uniform(20, 95)
        self.kpi_data["cpu_utilization"][node_id].append({"timestamp": timestamp, "value": cpu_util})
        memory_util = random.uniform(30, 90)
        self.kpi_data["memory_utilization"][node_id].append({"timestamp": timestamp, "value": memory_util})
        latency = random.uniform(10, 200)
        self.kpi_data["service_latency"][node_id].append({"timestamp": timestamp, "value": latency})
        error_rate = random.uniform(0, 10)
        self.kpi_data["error_rate"][node_id].append({"timestamp": timestamp, "value": error_rate})
        throughput = random.uniform(100, 2000)
        self.kpi_data["throughput"][node_id].append({"timestamp": timestamp, "value": throughput})
        success_rate = random.uniform(90, 100)
        self.kpi_data["connection_success_rate"][node_id].append({"timestamp": timestamp, "value": success_rate})
        if node["status"] == "active" and random.random() < 0.1:
            recovery_time = random.uniform(10, 500)
            self.kpi_data["recovery_time"][node_id].append({"timestamp": timestamp, "value": recovery_time})
        logger.info(f"Collected KPI data for node {node_id}")
    def _analyze_kpi_data(self):
        logger.info("Analyzing KPI data")
        issues = []
        for kpi in self.kpi_definitions:
            kpi_id = kpi["id"]
            warning_threshold = kpi["warning_threshold"]
            critical_threshold = kpi["critical_threshold"]
            for node_id, data_points in self.kpi_data[kpi_id].items():
                if not data_points:
                    continue
                latest = data_points[-1]
                value = latest["value"]
                if kpi["category"] in ["availability", "quality"]:
                    if value < critical_threshold:
                        severity = "CRITICAL"
                    elif value < warning_threshold:
                        severity = "WARNING"
                    else:
                        severity = "OK"
                else:
                    if value > critical_threshold:
                        severity = "CRITICAL"
                    elif value > warning_threshold:
                        severity = "WARNING"
                    else:
                        severity = "OK"
                if severity != "OK":
                    issues.append({
                        "node_id": node_id,
                        "kpi_id": kpi_id,
                        "kpi_name": kpi["name"],
                        "value": value,
                        "unit": kpi["unit"],
                        "severity": severity,
                        "timestamp": latest["timestamp"]
                    })
        if issues:
            logger.warning(f"Found {len(issues)} KPI issues")
            for issue in issues:
                logger.warning(f"KPI Issue: {issue['severity']} - {issue['kpi_name']} on {issue['node_id']}: {issue['value']}{issue['unit']}")
        else:
            logger.info("No KPI issues found")
        return issues
    def get_kpi_data(self, kpi_id=None, node_id=None, time_range=None):
        result = {}
        if kpi_id:
            if kpi_id not in self.kpi_data:
                return {}
            kpi_data = {kpi_id: self.kpi_data[kpi_id]}
        else:
            kpi_data = self.kpi_data
        for kpi_id, node_data in kpi_data.items():
            result[kpi_id] = {}
            if node_id:
                if node_id not in node_data:
                    continue
                filtered_node_data = {node_id: node_data[node_id]}
            else:
                filtered_node_data = node_data
            for node_id, data_points in filtered_node_data.items():
                if time_range:
                    cutoff_time = datetime.now() - timedelta(seconds=time_range)
                    cutoff_str = cutoff_time.isoformat()
                    filtered_data = [dp for dp in data_points if dp["timestamp"] >= cutoff_str]
                else:
                    filtered_data = list(data_points)
                if filtered_data:
                    result[kpi_id][node_id] = filtered_data
        return result
    def get_kpi_summary(self, kpi_id=None, node_id=None, time_range=None):
        data = self.get_kpi_data(kpi_id, node_id, time_range)
        summary = {}
        for kpi_id, node_data in data.items():
            summary[kpi_id] = {}
            for node_id, data_points in node_data.items():
                if not data_points:
                    continue
                values = [dp["value"] for dp in data_points]
                summary[kpi_id][node_id] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "count": len(values),
                    "latest": data_points[-1]["value"],
                    "latest_timestamp": data_points[-1]["timestamp"]
                }
        return summary
    def export_kpi_data(self, file_path, kpi_id=None, node_id=None, time_range=None):
        data = self.get_kpi_data(kpi_id, node_id, time_range)
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Exported KPI data to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting KPI data: {str(e)}")
            return False 