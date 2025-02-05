from dotenv import load_dotenv
from flask import Flask, jsonify
import os
import requests

script_dir = os.path.dirname(__file__)
load_dotenv(os.path.join(script_dir, ".env"))

url = os.getenv("ZABBIX_URL") 
user = os.getenv("ZABBIX_USER")
password = os.getenv("ZABBIX_PASSWORD")

headers = {"Content-Type": "application/json"}

zabbix_token = None
list_groupid = []
list_groupname = []
list_hostname = []

def login_to_zabbix():
    payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": user,
                "password": password
            },
            "id": 1,
            "auth": None
    }

    response = requests.post(url, json=payload)
    zabbix_token = response.json()["result"]
    return zabbix_token

def fetch_host_groups():
    global zabbix_token
    global url

    if not zabbix_token:
        zabbix_token = login_to_zabbix()

    payload = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": ["groupid", "name"]
            },
            "auth": zabbix_token,
            "id": 1
    }

    response = requests.post(url, json=payload)
    return response.json().get("result", [])

def get_host_by_group(groupid):
    global zabbix_token
    global url

    payload = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host", "name"],
                "groupids": groupid
            },
            "auth": zabbix_token,
            "id": 1
    }

    response = requests.post(url, json=payload)
    return response.json().get("result", [])

def fetch_zabbix_data():
    global list_groupid
    global list_groupname
    global list_hostname

    hostgroup = fetch_host_groups()

    for group in hostgroup:
        hosts = get_host_by_group(group["groupid"])
        hostname = []

        if len(hosts) == 0:
            continue

        if group["name"] == "Zabbix servers":
            continue

        for host in hosts:
            hostname.append(host["name"])

        list_groupid.append(group["groupid"])
        list_groupname.append(group["name"])
        list_hostname.append(hostname)

fetch_zabbix_data()

index_group = 0
index_host = 0

app = Flask(__name__)

@app.route('/host', methods=['GET'])
def get_hosts():
    global index_group
    global index_host

    host = list_hostname[index_group][index_host]
    index_host += 1

    if (index_host == len(list_hostname[index_group])):
        index_host = 0
        index_group += 1

        if (index_group == len(list_groupname)):
            index_group = 0

    return jsonify({"hosts": host})

@app.route('/group', methods=['GET'])
def get_groups():
    global index_group

    return jsonify({"groups": list_groupname[index_group]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
