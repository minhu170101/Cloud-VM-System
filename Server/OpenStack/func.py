import requests
import json

url = "http://172.20.60.100"

def get_token():
    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "admin",
                        "domain": {
                            "name": "Default"
                        },
                        "password": "123"
                    }
                }
            }
        }
    }
    url = "http://172.20.60.100"
    try:
        res = requests.post(url + ":5000/v3/auth/tokens",
                            headers={'content-type': 'application/json'},
                            data=json.dumps(payload))
    except:
        return ""
    return res.headers['X-Subject-Token']

def get_instances():
    try:
        instances = requests.get(url + ":8774/v2.1/servers/detail",
                                 headers={'content-type': 'application/json',
                                          'X-Auth-Token': get_token()
                                          },
                                 )
        instances_details = instances.json()
    except:
        instances_details = {}
    return instances_details

def get_images():
    try:
        images = requests.get(url + ":9292/v2.1/images",
                              headers={'content-type': 'application/json',
                                       'X-Auth-Token': get_token()
                                       },
                              )
        images_details = images.json()
    except:
        images_details = {}
    return images_details

def get_flavors():
    try:
        flavors = requests.get(url + ":8774/v2.1/flavors/detail",
                               headers={'content-type': 'application/json',
                                        'X-Auth-Token': get_token()
                                        },
                               )
        flavors_details = flavors.json()
    except:
        flavors_details = {}
    return flavors_details

def get_containers():
    try:
        containers = requests.get(url + ":9517/v1/containers/",
                                  headers={'content-type': 'application/json',
                                           'X-Auth-Token': get_token()
                                           },
                                  )
        containers_details = containers.json()
    except:
        containers_details = {}
    return containers_details

def get_vm_detail(vm_id):
    try:
        res = requests.get(url + ":8774/v2.1/servers/" + vm_id,
                           headers={'content-type': 'application/json',
                                    'X-Auth-Token': get_token()},
                           )
        data = res.json()
        return data['server']
    except:
        return {}

def get_flavor_detail(flavor_id):
    try:
        res = requests.get(url + ":8774/v2.1/flavors/" + flavor_id,
                           headers={'content-type': 'application/json',
                                    'X-Auth-Token': get_token()},
                           )
        data = res.json()
        return data['flavor']
    except:
        return {}

def create_vm(soluong,image,flavor):
    payload = {
        "server": {
            "name": "May",
            "imageRef": image,
            "flavorRef": flavor,
            "networks": [{
                "uuid": "d95692d1-d07b-4d7b-b2bb-dcab8b15842f"
            }],
            "max_count": soluong
        }
    }
    try:
        res = requests.post(url + ":8774/v2.1/servers",
                            headers={'content-type': 'application/json',
                                     'X-Auth-Token': get_token()},
                            data=json.dumps(payload)
                            )
        return res.status_code
    except:
        return -1

def delete_vm(vm_id):
    payload = {
        "forceDelete": None
    }
    try:
        res = requests.post(url + ":8774/v2.1/servers/" + vm_id + "/action",
                            headers={'content-type': 'application/json',
                                     'X-Auth-Token': get_token()},
                            data=json.dumps(payload)
                            )
        return res.status_code
    except:
        return -1

def create_snapshot(vm_id,name):
    payload = {
        "createImage": {
            "name": name,
            "metadata": {
                "meta_var": "meta_val"
            }
        }
    }
    try:
        res = requests.post(url + ":8774/v2.1/servers/" + vm_id + "/action",
                            headers={'content-type': 'application/json',
                                     'X-Auth-Token': get_token()},
                            data=json.dumps(payload)
                            )
        return res.status_code
    except:
        return -1

def start_vm(vm_id):
    payload = {
        "os-start": None
    }
    try:
        res = requests.post(url + ":8774/v2.1/servers/" + vm_id + "/action",
                            headers={'content-type': 'application/json',
                                     'X-Auth-Token': get_token()},
                            data=json.dumps(payload)
                            )
        return res.status_code
    except:
        return -1
def shutdown_vm():
    data = get_instances()
    check = 0
    for values in data['servers']:
        payload = {
            "os-stop": None
        }
        try:
            res = requests.post(url + ":8774/v2.1/servers/" + values['id'] + "/action",
                                headers={'content-type': 'application/json',
                                         'X-Auth-Token': get_token()},
                                data=json.dumps(payload)
                                )
            check = res.status_code
        except:
            check = -1
    if check == 202:
        return 202
    else:
        return -1

def start_all_vm():
    data = get_instances()
    check = 0
    for values in data['servers']:
        payload = {
            "reboot":{
                "type": "HARD"
            }
        }
        try:
            res = requests.post(url + ":8774/v2.1/servers/" + values['id'] + "/action",
                                headers={'content-type': 'application/json',
                                         'X-Auth-Token': get_token()},
                                data=json.dumps(payload)
                                )
            check = res.status_code
        except:
            check = -1
    if check == 202:
        return 202
    else:
        return -1

def reboot_vm(vm_id):
    payload = {
        "reboot": {
            "type": "HARD"
        }
    }
    try:
        res = requests.post(url + ":8774/v2.1/servers/" + vm_id + "/action",
                            headers={'content-type': 'application/json',
                                     'X-Auth-Token': get_token()},
                            data=json.dumps(payload)
                            )
        check = res.status_code
    except:
        check = -1