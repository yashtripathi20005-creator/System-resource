# ============================================
# File: core/resource_collector.py
# ============================================
# Core logic for collecting system resource data
# ============================================

import psutil
import time
from datetime import datetime

class ResourceCollector:
    """Collects CPU and RAM usage data from the system"""
    
    def __init__(self):
        """Initialize the collector"""
        self.cpu_history = []
        self.max_history = 60  # Store last 60 readings
        
    def get_cpu_usage(self):
        """
        Get CPU usage statistics
        
        Returns:
            dict: Contains percent, cores, load_avg, timestamp
        """
        try:
            # Get CPU percentage for all cores
            cpu_percent = psutil.cpu_percent(interval=0.5, percpu=False)
            
            # Get per-core percentages
            per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
            
            # Get CPU frequency
            freq = psutil.cpu_freq()
            
            # Get load average (Unix-like systems)
            load_avg = None
            try:
                load_avg = psutil.getloadavg()
                load_avg_str = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
            except (AttributeError, OSError):
                load_avg_str = "N/A"
            
            # Store history
            self.cpu_history.append(cpu_percent)
            if len(self.cpu_history) > self.max_history:
                self.cpu_history.pop(0)
            
            return {
                'percent': cpu_percent,
                'cores': psutil.cpu_count(),
                'per_core': per_cpu,
                'frequency': freq.current if freq else 0,
                'load_avg': load_avg_str,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
        except Exception as e:
            print(f"Error collecting CPU data: {e}")
            return {
                'percent': 0,
                'cores': 1,
                'per_core': [],
                'frequency': 0,
                'load_avg': "N/A",
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
    def get_ram_usage(self):
        """
        Get RAM usage statistics
        
        Returns:
            dict: Contains total, used, free, percent, timestamp
        """
        try:
            memory = psutil.virtual_memory()
            
            # Get swap memory info
            swap = psutil.swap_memory()
            
            return {
                'total': memory.total / (1024 ** 3),  # Convert to GB
                'available': memory.available / (1024 ** 3),
                'used': memory.used / (1024 ** 3),
                'free': memory.free / (1024 ** 3),
                'percent': memory.percent,
                'swap_total': swap.total / (1024 ** 3) if swap else 0,
                'swap_used': swap.used / (1024 ** 3) if swap else 0,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
        except Exception as e:
            print(f"Error collecting RAM data: {e}")
            return {
                'total': 0,
                'available': 0,
                'used': 0,
                'free': 0,
                'percent': 0,
                'swap_total': 0,
                'swap_used': 0,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            
    def get_system_info(self):
        """
        Get comprehensive system information
        
        Returns:
            dict: Combined system information
        """
        return {
            'cpu': self.get_cpu_usage(),
            'ram': self.get_ram_usage(),
            'timestamp': datetime.now().isoformat()
        }
