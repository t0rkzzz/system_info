import psutil
import socket


def get_pc_info():
    mem = psutil.virtual_memory()
    pc = {
        "name": socket.gethostname(),
        "CPU": psutil.cpu_percent(),
        "RAM": {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used,
            "free": mem.free
        }
    }
    return pc


def get_tasks():
    tasks = []
    for task in psutil.process_iter():
        task_dict = {"pid": f"{task.pid}"}
        try:
            task_dict["name"] = task.name()
        except Exception as e:
            task_dict["name"] = f"{e}"
        try:
            task_dict["cpu"] = task.cpu_percent()
        except Exception as e:
            task_dict["cpu"] = f"{e}"
        try:
            task_dict["RAM"] = round(task.memory_percent(), 2)
        except Exception as e:
            task_dict["RAM"] = f"{e}"
        tasks.append(task_dict)
    return tasks
