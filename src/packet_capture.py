from scapy.all import sniff, conf, get_if_list
from scapy.layers.inet import IP
import pandas as pd
from datetime import datetime
import queue
import threading
import os
import sys

class PacketCapture:
    def __init__(self, packet_queue, stop_event):
        self.packet_queue = packet_queue
        self.stop_event = stop_event
        self.packets = []
        self.interface = self._get_default_interface()
        
    def _get_default_interface(self):
        """Get the default network interface for packet capture."""
        try:
            # Get list of available interfaces
            interfaces = get_if_list()
            
            # Filter out loopback interface if others are available
            valid_interfaces = [iface for iface in interfaces if not iface.startswith('lo')]
            
            if valid_interfaces:
                return valid_interfaces[0]
            elif interfaces:
                return interfaces[0]
            else:
                raise Exception("No network interfaces found")
                
        except Exception as e:
            print(f"Error getting default interface: {str(e)}")
            sys.exit(1)

    def _check_permissions(self):
        """Check if the script has necessary permissions."""
        if os.geteuid() != 0:
            print("Error: This script requires root privileges to capture packets.")
            print("Please run with sudo or as root.")
            sys.exit(1)

    def process_packet(self, packet):
        """Process captured packets and add them to the queue."""
        try:
            if IP in packet:
                packet_info = {
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Source': packet[IP].src,
                    'Destination': packet[IP].dst,
                    'Protocol': packet[IP].proto,
                    'Length': len(packet),
                    'Interface': self.interface
                }
                self.packets.append(packet_info)
                self.packet_queue.put(packet_info)
                
                # Convert to DataFrame every 10 packets for batch processing
                if len(self.packets) >= 10:
                    df = pd.DataFrame(self.packets)
                    self.packets = []  # Clear the buffer
                    return df
        except Exception as e:
            print(f"Error processing packet: {str(e)}")
        return None

    def capture_packets(self):
        """Start packet capture on the specified interface."""
        try:
            # Check for root privileges
            self._check_permissions()
            
            print(f"Starting packet capture on interface: {self.interface}")
            sniff(
                iface=self.interface,
                prn=self.process_packet,
                stop_filter=lambda x: self.stop_event.is_set(),
                store=0  # Don't store packets in memory
            )
        except Exception as e:
            print(f"Error during packet capture: {str(e)}")
            if "permission denied" in str(e).lower():
                print("Permission denied. Please ensure you're running with sudo privileges.")
            self.stop_event.set()

    def start_capture(self):
        """Start the capture thread."""
        try:
            capture_thread = threading.Thread(target=self.capture_packets)
            capture_thread.daemon = True  # Thread will exit when main program exits
            capture_thread.start()
            return capture_thread
        except Exception as e:
            print(f"Error starting capture thread: {str(e)}")
            self.stop_event.set()
            return None
