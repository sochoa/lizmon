import psutil
import time

def gather_cpu():
    return psutil.cpu_percent(interval = 1, percpu = False)

def gather_mem():
    return psutil.virtual_memory().percent

def gather_stats():
    return {
        "ts": int(time.time()),
        "cpu": gather_cpu(),
        "mem": gather_mem(),
    }
