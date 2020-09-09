import requests
import json


def get_info():
    ip = ':)'
    port = '5678'
    url = 'http://' + ip + ':' + port + '/common'
    try:
        resp = requests.get(url)
    except requests.ConnectionError:
        return 'NO DATA'
    try:
        info = resp.json()
    except json.decoder.JSONDecodeError:
        return 'PARSING ERROR'
    result = []
    for ip in info:
        if isinstance(info[ip], str):
            result.append({
                "ip": ip,
                "PC": info[ip],
                "RAM": info[ip],
                "CPU": info[ip],
                "critical_ram": info[ip],
                "critical_cpu": info[ip]
            })
        else:
            try:
                result.append({
                    "ip": ip,
                    "PC": info[ip]["name"],
                    "RAM": info[ip]["RAM"]["percent"],
                    "CPU": info[ip]["CPU"],
                    "critical_ram": info[ip]["critical_ram"],
                    "critical_cpu": info[ip]["critical_cpu"]
                })
            except KeyError:
                result.append({
                    "ip": ip,
                    "PC": "ERROR",
                    "RAM": "ERROR",
                    "CPU": "ERROR",
                    "critical_ram": "ERROR",
                    "critical_cpu": "ERROR"
                })
    return result
