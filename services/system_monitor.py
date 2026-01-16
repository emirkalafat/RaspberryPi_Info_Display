import psutil
import subprocess

class SystemMonitorService:
    def get_stats(self):
        """Returns a dict with ip, cpu, ram, temp."""
        return {
            "ip": self._get_ip_address(),
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "temp": self._get_cpu_temp(),
        }

    def _get_ip_address(self):
        try:
            cmd = "hostname -I | cut -d' ' -f1"
            return subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        except:
            return "No IP"

    def _get_cpu_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = float(f.read()) / 1000.0
            return temp
        except:
            return 0.0
