import threading
import time
import random
import logging
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger("OAM-Platform")

class EventType(Enum):
    NODE_FAILURE = 1
    SERVICE_FAILURE = 2
    NETWORK_CONGESTION = 3
    SECURITY_BREACH = 4
    RESOURCE_EXHAUSTION = 5
    CONFIGURATION_CHANGE = 6
    FAILOVER = 7
    RECOVERY = 8

class EventSimulator:
    """Event Simulation for 5G/LTE networks"""
    def __init__(self):
        self.running = False
        self.simulation_interval = 120  # seconds
        self.events = []
        self.network_nodes = [
            {"id": "gnb-001", "type": "gNB", "ip": "10.0.1.1", "status": "active"},
            {"id": "gnb-002", "type": "gNB", "ip": "10.0.1.2", "status": "active"},
            {"id": "amf-001", "type": "AMF", "ip": "10.0.2.1", "status": "active"},
            {"id": "smf-001", "type": "SMF", "ip": "10.0.2.2", "status": "active"},
            {"id": "upf-001", "type": "UPF", "ip": "10.0.3.1", "status": "active"},
            {"id": "pcf-001", "type": "PCF", "ip": "10.0.3.2", "status": "active"},
        ]
        self.scenarios = [
            {
                "name": "AMF Failover",
                "description": "Simulate AMF node failure and failover to backup",
                "events": [
                    {"type": EventType.NODE_FAILURE, "target_type": "AMF", "probability": 1.0},
                    {"type": EventType.FAILOVER, "target_type": "AMF", "probability": 0.9},
                    {"type": EventType.RECOVERY, "target_type": "AMF", "probability": 0.8}
                ]
            },
            {
                "name": "Network Congestion",
                "description": "Simulate network congestion affecting multiple nodes",
                "events": [
                    {"type": EventType.NETWORK_CONGESTION, "target_type": "ALL", "probability": 1.0},
                    {"type": EventType.SERVICE_FAILURE, "target_type": "UPF", "probability": 0.7},
                    {"type": EventType.RECOVERY, "target_type": "ALL", "probability": 0.9}
                ]
            },
            {
                "name": "Resource Exhaustion",
                "description": "Simulate resource exhaustion on a node",
                "events": [
                    {"type": EventType.RESOURCE_EXHAUSTION, "target_type": "SMF", "probability": 1.0},
                    {"type": EventType.SERVICE_FAILURE, "target_type": "SMF", "probability": 0.8},
                    {"type": EventType.RECOVERY, "target_type": "SMF", "probability": 0.9}
                ]
            },
            {
                "name": "Security Incident",
                "description": "Simulate a security breach and response",
                "events": [
                    {"type": EventType.SECURITY_BREACH, "target_type": "PCF", "probability": 1.0},
                    {"type": EventType.CONFIGURATION_CHANGE, "target_type": "PCF", "probability": 0.9},
                    {"type": EventType.RECOVERY, "target_type": "PCF", "probability": 0.95}
                ]
            },
            {
                "name": "Multiple Node Failure",
                "description": "Simulate multiple node failures and recovery",
                "events": [
                    {"type": EventType.NODE_FAILURE, "target_type": "gNB", "probability": 1.0},
                    {"type": EventType.NODE_FAILURE, "target_type": "UPF", "probability": 0.8},
                    {"type": EventType.FAILOVER, "target_type": "gNB", "probability": 0.9},
                    {"type": EventType.FAILOVER, "target_type": "UPF", "probability": 0.7},
                    {"type": EventType.RECOVERY, "target_type": "gNB", "probability": 0.95},
                    {"type": EventType.RECOVERY, "target_type": "UPF", "probability": 0.9}
                ]
            }
        ]
    def start(self):
        if self.running:
            return
        self.running = True
        logger.info("Starting Event Simulation module")
        threading.Thread(target=self._simulation_loop, name="event-simulation-thread", daemon=True).start()
    def stop(self):
        self.running = False
        logger.info("Stopped Event Simulation module")
    def get_status(self):
        return {
            "status": "running" if self.running else "stopped",
            "events_generated": len(self.events),
            "scenarios_available": len(self.scenarios)
        }
    def _simulation_loop(self):
        logger.info("Starting event simulation loop")
        while self.running:
            logger.info("Running event simulation cycle")
            if random.random() < 0.7:
                self._run_scenario()
            else:
                self._generate_random_events()
            time.sleep(self.simulation_interval)
    def _run_scenario(self):
        scenario = random.choice(self.scenarios)
        logger.info(f"Running scenario: {scenario['name']}")
        logger.info(f"Description: {scenario['description']}")
        for event_def in scenario['events']:
            if random.random() > event_def['probability']:
                logger.info(f"Event {event_def['type'].name} skipped due to probability")
                continue
            if event_def['target_type'] == 'ALL':
                target_nodes = self.network_nodes
            else:
                target_nodes = [node for node in self.network_nodes if node['type'] == event_def['target_type']]
            if not target_nodes:
                logger.warning(f"No matching nodes found for type {event_def['target_type']}")
                continue
            target_node = random.choice(target_nodes)
            self._generate_event(event_def['type'], target_node)
            time.sleep(random.uniform(1, 5))
    def _generate_random_events(self):
        logger.info("Generating random events")
        num_events = random.randint(1, 3)
        for _ in range(num_events):
            event_type = random.choice(list(EventType))
            target_node = random.choice(self.network_nodes)
            self._generate_event(event_type, target_node)
            time.sleep(random.uniform(1, 3))
    def _generate_event(self, event_type, target_node):
        event_id = len(self.events) + 1
        timestamp = datetime.now().isoformat()
        logger.info(f"Generating event: {event_type.name} for node {target_node['id']}")
        event = {
            "id": event_id,
            "type": event_type.name,
            "target_node": target_node['id'],
            "target_type": target_node['type'],
            "timestamp": timestamp,
            "details": {}
        }
        if event_type == EventType.NODE_FAILURE:
            event["details"] = {
                "failure_reason": random.choice(["Hardware failure", "Software crash", "Power outage", "Network connectivity loss"]),
                "severity": random.choice(["Critical", "Major", "Minor"])
            }
            target_node["status"] = "down"
        elif event_type == EventType.SERVICE_FAILURE:
            event["details"] = {
                "service_name": random.choice(["Authentication", "Session Management", "Policy Control", "User Plane"]),
                "failure_reason": random.choice(["Timeout", "Internal error", "Dependency failure", "Resource constraint"]),
                "affected_users": random.randint(10, 1000)
            }
        elif event_type == EventType.NETWORK_CONGESTION:
            event["details"] = {
                "congestion_level": random.uniform(70, 100),
                "affected_interfaces": random.choice(["N1", "N2", "N3", "N4", "N6", "All"]),
                "duration_seconds": random.randint(30, 300)
            }
        elif event_type == EventType.SECURITY_BREACH:
            event["details"] = {
                "breach_type": random.choice(["Unauthorized access", "Authentication bypass", "DDoS attack", "Data exfiltration"]),
                "severity": random.choice(["Critical", "Major", "Minor"]),
                "affected_systems": random.randint(1, 5)
            }
        elif event_type == EventType.RESOURCE_EXHAUSTION:
            event["details"] = {
                "resource_type": random.choice(["CPU", "Memory", "Disk", "Network bandwidth", "Connection pool"]),
                "utilization": random.uniform(90, 100),
                "available_capacity": random.uniform(0, 10)
            }
        elif event_type == EventType.CONFIGURATION_CHANGE:
            event["details"] = {
                "change_type": random.choice(["Parameter update", "Software upgrade", "Policy change", "Security hardening"]),
                "change_reason": random.choice(["Planned maintenance", "Performance optimization", "Security patch", "Bug fix"]),
                "change_id": f"CHG-{random.randint(1000, 9999)}"
            }
        elif event_type == EventType.FAILOVER:
            event["details"] = {
                "failover_target": f"{target_node['type']}-BACKUP",
                "failover_type": random.choice(["Automatic", "Manual", "Scheduled"]),
                "failover_duration_seconds": random.randint(5, 60)
            }
        elif event_type == EventType.RECOVERY:
            event["details"] = {
                "recovery_action": random.choice(["Restart", "Failback", "Reconfiguration", "Manual intervention"]),
                "recovery_duration_seconds": random.randint(10, 300),
                "success": random.random() < 0.9
            }
            if event["details"]["success"]:
                target_node["status"] = "active"
        self.events.append(event)
        logger.warning(f"EVENT: {event_type.name} on {target_node['id']} - {json.dumps(event['details'])}")
        return event
    def get_events(self, event_type=None, node_id=None, time_range=None):
        filtered_events = self.events
        if event_type:
            filtered_events = [e for e in filtered_events if e["type"] == event_type.name]
        if node_id:
            filtered_events = [e for e in filtered_events if e["target_node"] == node_id]
        if time_range:
            cutoff_time = (datetime.now() - time_range).isoformat()
            filtered_events = [e for e in filtered_events if e["timestamp"] >= cutoff_time]
        return filtered_events
    def run_load_test(self, target_node_type, duration_seconds=60, intensity="medium"):
        logger.info(f"Starting load test on {target_node_type} nodes for {duration_seconds} seconds at {intensity} intensity")
        target_nodes = [node for node in self.network_nodes if node["type"] == target_node_type]
        if not target_nodes:
            logger.warning(f"No nodes found of type {target_node_type}")
            return False
        if intensity == "low":
            cpu_load = random.uniform(50, 70)
            memory_load = random.uniform(40, 60)
            connection_load = random.randint(100, 500)
        elif intensity == "medium":
            cpu_load = random.uniform(70, 85)
            memory_load = random.uniform(60, 80)
            connection_load = random.randint(500, 2000)
        elif intensity == "high":
            cpu_load = random.uniform(85, 95)
            memory_load = random.uniform(80, 95)
            connection_load = random.randint(2000, 5000)
        else:
            logger.error(f"Invalid intensity: {intensity}")
            return False
        load_test_event = {
            "id": len(self.events) + 1,
            "type": "LOAD_TEST",
            "target_type": target_node_type,
            "target_nodes": [node["id"] for node in target_nodes],
            "timestamp": datetime.now().isoformat(),
            "details": {
                "duration_seconds": duration_seconds,
                "intensity": intensity,
                "cpu_load": cpu_load,
                "memory_load": memory_load,
                "connection_load": connection_load
            }
        }
        self.events.append(load_test_event)
        logger.info(f"Load test started: {json.dumps(load_test_event['details'])}")
        time.sleep(min(duration_seconds, 5))
        if intensity == "high":
            for node in target_nodes:
                if random.random() < 0.7:
                    self._generate_event(EventType.RESOURCE_EXHAUSTION, node)
        completion_event = {
            "id": len(self.events) + 1,
            "type": "LOAD_TEST_COMPLETED",
            "target_type": target_node_type,
            "target_nodes": [node["id"] for node in target_nodes],
            "timestamp": datetime.now().isoformat(),
            "details": {
                "original_test_id": load_test_event["id"],
                "success": True,
                "failures": 0,
                "performance_impact": {
                    "latency_increase_percent": random.uniform(10, 50),
                    "throughput_decrease_percent": random.uniform(5, 30),
                    "error_rate_increase_percent": random.uniform(1, 20)
                }
            }
        }
        self.events.append(completion_event)
        logger.info(f"Load test completed: {json.dumps(completion_event['details'])}")
        return True
    def simulate_failover_scenario(self, node_type):
        logger.info(f"Simulating failover scenario for {node_type} nodes")
        target_nodes = [node for node in self.network_nodes if node["type"] == node_type]
        if not target_nodes:
            logger.warning(f"No nodes found of type {node_type}")
            return False
        target_node = random.choice(target_nodes)
        failure_event = self._generate_event(EventType.NODE_FAILURE, target_node)
        detection_time = random.uniform(1, 5)
        logger.info(f"Failure detection time: {detection_time:.2f} seconds")
        time.sleep(min(detection_time, 2))
        failover_event = self._generate_event(EventType.FAILOVER, target_node)
        failover_time = failover_event["details"]["failover_duration_seconds"]
        logger.info(f"Failover time: {failover_time} seconds")
        time.sleep(min(failover_time, 3))
        recovery_success = random.random() < 0.9
        recovery_event = self._generate_event(EventType.RECOVERY, target_node)
        scenario_result = {
            "scenario": "Failover",
            "target_node": target_node["id"],
            "target_type": target_node["type"],
            "events": [
                {"id": failure_event["id"], "type": failure_event["type"]},
                {"id": failover_event["id"], "type": failover_event["type"]},
                {"id": recovery_event["id"], "type": recovery_event["type"]}
            ],
            "metrics": {
                "detection_time_seconds": detection_time,
                "failover_time_seconds": failover_time,
                "recovery_time_seconds": recovery_event["details"]["recovery_duration_seconds"],
                "total_downtime_seconds": detection_time + failover_time,
                "recovery_success": recovery_event["details"]["success"]
            }
        }
        logger.info(f"Failover scenario completed: {json.dumps(scenario_result['metrics'])}")
        return scenario_result 