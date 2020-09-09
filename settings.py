import shelve
import socket
import json
import requests
import concurrent.futures
import os


port = '5678'
srv_ip = ':)'
ip = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
critical_ram_default = 89.7
critical_cpu_default = 80.0


def add_server(data):
    with shelve.open("servers") as lst:
        if data["ip"] not in lst:
            lst[data['ip']] = {
                'port': data['port'],
                'critical_ram': critical_ram_default,
                'critical_cpu': critical_cpu_default
            }


def set_critical_values(data):
    with shelve.open('servers') as lst:
        try:
            srv = lst[data["ip"]]
            srv['critical_ram'] = data['ram']
            srv['critical_cpu'] = data['cpu']
            lst[data["ip"]] = srv
            return "OK"
        except KeyError as e:
            return f'{e}'


def get_critical_values(ip):
    with shelve.open('servers') as lst:
        try:
            return {
                'ram': lst[ip]['critical_ram'],
                'cpu': lst[ip]['critical_cpu']
            }
        except KeyError:
            return {
                'ram': 'undefined',
                'cpu': 'undefined'
            }


def get_servers():
    with shelve.open("servers") as lst:
        for ip in lst.keys():
            yield [ip, lst[ip]]


def get_srv_stats(data):
    res = {}
    url = 'http://' + data[0] + ':' + data[1]["port"] + '/self'
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            res[f'{data[0]}'] = resp.json()
            res[f'{data[0]}']['critical_ram'] = data[1]["critical_ram"]
            res[f'{data[0]}']['critical_cpu'] = data[1]["critical_cpu"]
    except ConnectionRefusedError:
        res[f'{data[0]}'] = 'NO CONNECTION'
    except requests.ConnectionError:
        res[f'{data[0]}'] = 'NO CONNECTION'
    return res


def get_srv_stats_json():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = [i for i in executor.map(get_srv_stats, get_servers())]
    res_dict = {}
    for srv in result:
        key = list(srv.keys())[0]
        res_dict[key] = srv[key]
    return json.dumps(res_dict)

def kill_ora_session(data):
    res = {"status": "ok"}
    try:
        os.system(f'orakill GB3 {data["pid"]}')
    except Exception as e:
        res = {"status": f"{e}"}
    return res
