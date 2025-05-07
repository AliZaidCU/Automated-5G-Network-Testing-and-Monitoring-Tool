import threading
import time
import random
import logging
from datetime import datetime
from collections import defaultdict

try:
    from scapy.all import IP, IPv6, TCP, UDP, ICMP, ICMPv6EchoRequest, send, wrpcap
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

logger = logging.getLogger("OAM-Platform")

class IPTrafficSimulator:
    """IP Traffic Simulation for 5G/LTE networks using Scapy"""
    def __init__(self):
        self.running = False
        self.simulation_interval = 30  # seconds
        self.stats = {
            "ipv4_packets_sent": 0,
            "ipv6_packets_sent": 0,
            "packets_received": 0,
            "latency_ms": defaultdict(list),
            "packet_loss": defaultdict(int),
            "jitter_ms": defaultdict(list)
        }
        self.network_topology = [
            {"name": "gNB-1", "ipv4": "192.168.1.1", "ipv6": "2001:db8::1"},
            {"name": "gNB-2", "ipv4": "192.168.1.2", "ipv6": "2001:db8::2"},
            {"name": "AMF", "ipv4": "192.168.2.1", "ipv6": "2001:db8:1::1"},
            {"name": "SMF", "ipv4": "192.168.2.2", "ipv6": "2001:db8:1::2"},
            {"name": "UPF", "ipv4": "192.168.3.1", "ipv6": "2001:db8:2::1"},
            {"name": "PCF", "ipv4": "192.168.3.2", "ipv6": "2001:db8:2::2"},
            {"name": "UE-1", "ipv4": "192.168.4.1", "ipv6": "2001:db8:3::1"},
            {"name": "UE-2", "ipv4": "192.168.4.2", "ipv6": "2001:db8:3::2"}
        ]
        self.qos_classes = [
            {"name": "Conversational", "dscp": 46, "priority": "High"},
            {"name": "Streaming", "dscp": 34, "priority": "Medium-High"},
            {"name": "Interactive", "dscp": 26, "priority": "Medium"},
            {"name": "Background", "dscp": 0, "priority": "Low"}
        ]
    def start(self):
        if self.running:
            return
        self.running = True
        logger.info("Starting IP Traffic Simulation module")
        if not SCAPY_AVAILABLE:
            logger.warning("Scapy not available. Running in limited simulation mode.")
        threading.Thread(target=self._simulation_loop, name="ip-simulation-thread", daemon=True).start()
    def stop(self):
        self.running = False
        logger.info("Stopped IP Traffic Simulation module")
    def get_status(self):
        return {
            "status": "running" if self.running else "stopped",
            "scapy_available": SCAPY_AVAILABLE,
            "ipv4_packets_sent": self.stats["ipv4_packets_sent"],
            "ipv6_packets_sent": self.stats["ipv6_packets_sent"],
            "packets_received": self.stats["packets_received"]
        }
    def _simulation_loop(self):
        logger.info("Starting IP traffic simulation loop")
        while self.running:
            logger.info("Running IP traffic simulation cycle")
            self._simulate_ipv4_traffic()
            self._simulate_ipv6_traffic()
            self._simulate_qos_traffic()
            self._analyze_traffic_stats()
            time.sleep(self.simulation_interval)
    def _simulate_ipv4_traffic(self):
        logger.info("Simulating IPv4 traffic")
        if not SCAPY_AVAILABLE:
            self._mock_ipv4_simulation()
            return
        try:
            src_node = random.choice(self.network_topology)
            dst_node = random.choice([n for n in self.network_topology if n != src_node])
            src_ip = src_node["ipv4"]
            dst_ip = dst_node["ipv4"]
            logger.info(f"Sending IPv4 packets from {src_node['name']} to {dst_node['name']}")
            packets = []
            tcp_packet = IP(src=src_ip, dst=dst_ip, ttl=64) / TCP(sport=random.randint(1024, 65535), dport=80)
            packets.append(("TCP", tcp_packet))
            udp_packet = IP(src=src_ip, dst=dst_ip, ttl=64) / UDP(sport=random.randint(1024, 65535), dport=53)
            packets.append(("UDP", udp_packet))
            icmp_packet = IP(src=src_ip, dst=dst_ip, ttl=64) / ICMP(type=8, code=0)
            packets.append(("ICMP", icmp_packet))
            for packet_type, packet in packets:
                start_time = time.time()
                send(packet, verbose=0)
                response_time = random.uniform(5, 100)
                logger.info(f"Sent {packet_type} packet: {src_ip} -> {dst_ip}, RTT: {response_time:.2f}ms")
                self.stats["ipv4_packets_sent"] += 1
                self.stats["latency_ms"][f"{src_ip}->{dst_ip}"].append(response_time)
                if random.random() < 0.05:
                    self.stats["packet_loss"][f"{src_ip}->{dst_ip}"] += 1
                else:
                    self.stats["packets_received"] += 1
            wrpcap("ipv4_simulation.pcap", [p[1] for p in packets], append=True)
        except Exception as e:
            logger.error(f"Error in IPv4 simulation: {str(e)}")
    def _simulate_ipv6_traffic(self):
        logger.info("Simulating IPv6 traffic")
        if not SCAPY_AVAILABLE:
            self._mock_ipv6_simulation()
            return
        try:
            src_node = random.choice(self.network_topology)
            dst_node = random.choice([n for n in self.network_topology if n != src_node])
            src_ip = src_node["ipv6"]
            dst_ip = dst_node["ipv6"]
            logger.info(f"Sending IPv6 packets from {src_node['name']} to {dst_node['name']}")
            packets = []
            tcp_packet = IPv6(src=src_ip, dst=dst_ip, hlim=64) / TCP(sport=random.randint(1024, 65535), dport=80)
            packets.append(("TCP6", tcp_packet))
            udp_packet = IPv6(src=src_ip, dst=dst_ip, hlim=64) / UDP(sport=random.randint(1024, 65535), dport=53)
            packets.append(("UDP6", udp_packet))
            icmp_packet = IPv6(src=src_ip, dst=dst_ip, hlim=64) / ICMPv6EchoRequest()
            packets.append(("ICMPv6", icmp_packet))
            for packet_type, packet in packets:
                start_time = time.time()
                send(packet, verbose=0)
                response_time = random.uniform(5, 100)
                logger.info(f"Sent {packet_type} packet: {src_ip} -> {dst_ip}, RTT: {response_time:.2f}ms")
                self.stats["ipv6_packets_sent"] += 1
                self.stats["latency_ms"][f"{src_ip}->{dst_ip}"].append(response_time)
                if random.random() < 0.05:
                    self.stats["packet_loss"][f"{src_ip}->{dst_ip}"] += 1
                else:
                    self.stats["packets_received"] += 1
            wrpcap("ipv6_simulation.pcap", [p[1] for p in packets], append=True)
        except Exception as e:
            logger.error(f"Error in IPv6 simulation: {str(e)}")
    def _simulate_qos_traffic(self):
        logger.info("Simulating QoS traffic")
        if not SCAPY_AVAILABLE:
            self._mock_qos_simulation()
            return
        try:
            src_node = random.choice(self.network_topology)
            dst_node = random.choice([n for n in self.network_topology if n != src_node])
            src_ip = src_node["ipv4"]
            dst_ip = dst_node["ipv4"]
            logger.info(f"Simulating QoS traffic from {src_node['name']} to {dst_node['name']}")
            for qos_class in self.qos_classes:
                tos_value = qos_class["dscp"] << 2
                packet = IP(src=src_ip, dst=dst_ip, tos=tos_value) / UDP(sport=random.randint(1024, 65535), dport=80)
                send(packet, verbose=0)
                if qos_class["priority"] == "High":
                    response_time = random.uniform(5, 20)
                elif qos_class["priority"] == "Medium-High":
                    response_time = random.uniform(15, 40)
                elif qos_class["priority"] == "Medium":
                    response_time = random.uniform(30, 70)
                else:
                    response_time = random.uniform(50, 150)
                logger.info(f"Sent QoS packet with class {qos_class['name']} (DSCP {qos_class['dscp']}): {src_ip} -> {dst_ip}, RTT: {response_time:.2f}ms")
                self.stats["ipv4_packets_sent"] += 1
                self.stats["latency_ms"][f"QoS-{qos_class['name']}"] .append(response_time)
                if len(self.stats["latency_ms"][f"QoS-{qos_class['name']}"]) > 1:
                    prev_latency = self.stats["latency_ms"][f"QoS-{qos_class['name']}"][-2]
                    jitter = abs(response_time - prev_latency)
                    self.stats["jitter_ms"][f"QoS-{qos_class['name']}"] .append(jitter)
        except Exception as e:
            logger.error(f"Error in QoS simulation: {str(e)}")
    def _mock_ipv4_simulation(self):
        src_node = random.choice(self.network_topology)
        dst_node = random.choice([n for n in self.network_topology if n != src_node])
        src_ip = src_node["ipv4"]
        dst_ip = dst_node["ipv4"]
        logger.info(f"[MOCK] Sending IPv4 packets from {src_node['name']} to {dst_node['name']}")
        packet_types = ["TCP", "UDP", "ICMP"]
        for packet_type in packet_types:
            response_time = random.uniform(5, 100)
            logger.info(f"[MOCK] Sent {packet_type} packet: {src_ip} -> {dst_ip}, RTT: {response_time:.2f}ms")
            self.stats["ipv4_packets_sent"] += 1
            self.stats["latency_ms"][f"{src_ip}->{dst_ip}"].append(response_time)
            if random.random() < 0.05:
                self.stats["packet_loss"][f"{src_ip}->{dst_ip}"] += 1
            else:
                self.stats["packets_received"] += 1
    def _mock_ipv6_simulation(self):
        src_node = random.choice(self.network_topology)
        dst_node = random.choice([n for n in self.network_topology if n != src_node])
        src_ip = src_node["ipv6"]
        dst_ip = dst_node["ipv6"]
        logger.info(f"[MOCK] Sending IPv6 packets from {src_node['name']} to {dst_node['name']}")
        packet_types = ["TCP6", "UDP6", "ICMPv6"]
        for packet_type in packet_types:
            response_time = random.uniform(5, 100)
            logger.info(f"[MOCK] Sent {packet_type} packet: {src_ip} -> {dst_ip}, RTT: {response_time:.2f}ms")
            self.stats["ipv6_packets_sent"] += 1
            self.stats["latency_ms"][f"{src_ip}->{dst_ip}"].append(response_time)
            if random.random() < 0.05:
                self.stats["packet_loss"][f"{src_ip}->{dst_ip}"] += 1
            else:
                self.stats["packets_received"] += 1
    def _mock_qos_simulation(self):
        src_node = random.choice(self.network_topology)
        dst_node = random.choice([n for n in self.network_topology if n != src_node])
        src_ip = src_node["ipv4"]
        dst_ip = dst_node["ipv4"]
        logger.info(f"[MOCK] Simulating QoS traffic from {src_node['name']} to {dst_node['name']}")
        for qos_class in self.qos_classes:
            if qos_class["priority"] == "High":
                response_time = random.uniform(5, 20)
            elif qos_class["priority"] == "Medium-High":
                response_time = random.uniform(15, 40)
            elif qos_class["priority"] == "Medium":
                response_time = random.uniform(30, 70)
            else:
                response_time = random.uniform(50, 150)
            logger.info(f"[MOCK] Sent QoS packet with class {qos_class['name']} (DSCP {qos_class['dscp']}): {src_ip} -> {dst_ip}, RTT: {response_time:.2f}ms")
            self.stats["ipv4_packets_sent"] += 1
            self.stats["latency_ms"][f"QoS-{qos_class['name']}"] .append(response_time)
            if len(self.stats["latency_ms"][f"QoS-{qos_class['name']}"]) > 1:
                prev_latency = self.stats["latency_ms"][f"QoS-{qos_class['name']}"][-2]
                jitter = abs(response_time - prev_latency)
                self.stats["jitter_ms"][f"QoS-{qos_class['name']}"] .append(jitter)
    def _analyze_traffic_stats(self):
        logger.info("Analyzing traffic statistics")
        avg_latency = {}
        for path, latencies in self.stats["latency_ms"].items():
            if latencies:
                avg_latency[path] = sum(latencies) / len(latencies)
        avg_jitter = {}
        for qos_class, jitters in self.stats["jitter_ms"].items():
            if jitters:
                avg_jitter[qos_class] = sum(jitters) / len(jitters)
        packet_loss_rate = {}
        for path, loss_count in self.stats["packet_loss"].items():
            total_sent = len(self.stats["latency_ms"].get(path, []))
            if total_sent > 0:
                packet_loss_rate[path] = (loss_count / total_sent) * 100
        logger.info(f"Total IPv4 packets sent: {self.stats['ipv4_packets_sent']}")
        logger.info(f"Total IPv6 packets sent: {self.stats['ipv6_packets_sent']}")
        logger.info(f"Total packets received: {self.stats['packets_received']}")
        for path, latency in avg_latency.items():
            logger.info(f"Average latency for {path}: {latency:.2f}ms")
        for qos_class, jitter in avg_jitter.items():
            logger.info(f"Average jitter for {qos_class}: {jitter:.2f}ms")
        for path, loss_rate in packet_loss_rate.items():
            logger.info(f"Packet loss rate for {path}: {loss_rate:.2f}%")
        return {
            "avg_latency": avg_latency,
            "avg_jitter": avg_jitter,
            "packet_loss_rate": packet_loss_rate
        } 