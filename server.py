from flask import Flask, request, render_template, redirect, url_for
import stat_collect
import json
import settings
import requests
import socket
from stat_get import get_info
from forms import ServerSettingsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = ':)'
ip = ":)" #socket.gethostbyname_ex(socket.gethostname())[-1][0]
port = settings.port
me = socket.gethostname()
srv_ip = settings.srv_ip


@app.route('/self')
def stats():
    return json.dumps(stat_collect.get_pc_info())


@app.route('/self_stat', methods=['POST', 'GET'])
def self_stat():
    form = ServerSettingsForm()
    if form.validate_on_submit():
        requests.post(f'http://{srv_ip}:{port}/set_crits', json={
            "ip": ip,
            "ram": form.ram_critical.data,
            "cpu": form.cpu_critical.data
        })
        print(ip, form.ram_critical.data, form.cpu_critical.data)
        return redirect(url_for('home'))
    elif request.method == 'GET':
        data = requests.post(f'http://{srv_ip}:{port}/my_crits', json={"ip": ip})
        if data.status_code == 200:
            form.ram_critical.data = data.json()["ram"]
            form.cpu_critical.data = data.json()["cpu"]
    return render_template('self_stat.html',
                           info=stat_collect.get_pc_info(),
                           title="Статистика",
                           ip_ad=ip,
                           pc_name=me,
                           form=form)


@app.route('/set_crits', methods=['POST'])
def set_crits():
    data = request.json
    return {"status": settings.set_critical_values(data)}


@app.route('/my_crits', methods=['POST'])
def my_crits():
    data = request.json
    return settings.get_critical_values(data["ip"])


@app.route('/self_tasks')
def self_tasks():
    return render_template('self_tasks.html', info=stat_collect.get_tasks(), title="Процессы", ip_ad=ip, pc_name=me)


@app.route('/send', methods=['POST'])
def send():
    data = request.json
    settings.add_server(data)
    return {"status": "ok"}


@app.route('/common')
def get_all():
    return settings.get_srv_stats_json()


@app.route('/kill', methods=['GET', 'POST'])
def kill_ora_session():
    if request.method == 'POST':
        data = str(request.query_string, 'utf-8')
        print(data)
        return settings.kill_ora_session({"pid": data})
    else:
        return {"status": f"Can't kill sessions via {request.method} method"}
    


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', srv_list=get_info())


if __name__ == '__main__':
    app.run(host=ip, port="5678")
