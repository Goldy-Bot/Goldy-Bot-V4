import os
import psutil
import platform

class System():
    """Goldy Bot class used to check how much Goldy is utalizing on the host system."""
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    @property
    def os(self) -> str:
        return f"{platform.system()} {platform.release()} {platform.version()}"

    @property
    def cpu(self) -> int:
        """Returns amount of CPU Goldy Bot is using on this system."""
        return self.process.cpu_percent(0.5)

    @property
    def ram(self) -> int:
        """Returns amount of ram Goldy Bot is using on this system."""
        return self.convert_to_GB(self.process.memory_info().rss)

    @property
    def disk(self):
        disk_process = self.process.io_counters() 
        disk_usage_process = disk_process[2] + disk_process[3]

        disk_system = psutil.disk_io_counters()
        disk_system_total = disk_system[2] + disk_system[3]

        return self.convert_to_MB(disk_usage_process/disk_system_total * 100)

    def convert_to_GB(self, size):
        return(f"{size/float(1<<30):,.2f}")

    def convert_to_MB(self, size):
        return (f"{size/float(1<<20):,.2f}")