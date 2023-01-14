import json

def web_page(url = "index.html"):
    with open(url, "r") as file:
        return file.read()

def add_sensor_to_list(sensor, List):
    """Ajoute un capteur à la liste si celui-ci n'est pas déjà présent dans la liste."""
    for s in List:
        if s['id'] == sensor['id']:
            s['rate'] = sensor['rate']
            return  # Le capteur est déjà dans la liste, on ne l'ajoute pas
    List.append(sensor)  # Le capteur n'est pas dans la liste, on l'ajoute

def get_sensor(id, List):
    for s in List:
        if s['id'] == id:
            return s
    return 0


def handler(request, conn, sensor_list):
    if request.split('?')[0] == 'api':
            if len(request.split('?')) > 1:
                st = request.split('?')[1].split('-')
                add_sensor_to_list({"id" : st[1].split('=')[1], "rate" : st[0].split('=')[1]}, sensor_list)

    elif request == 'setting':
            conn.send(str(0))

    elif request == 'stopServer':
            SERVER_RUNNING = False
            conn.sendall('Server off ! ')
    elif request.split('?')[0] == 'sensors':
        if len(request.split('?')) > 1:
            searchedSensor = get_sensor(request.split('?')[1].split('=')[1], sensor_list)
            if searchedSensor != 0:
                conn.sendall(str(json.dumps(searchedSensor)))
            else:
                conn.sendall('Not found')
    elif request.split('?')[0] == 'cmd': #DEV ONLY
        exec(request.split('?')[1])

    elif request.split('?')[0] == 'AllSensors':
            conn.sendall(json.dumps(sensor_list))
            print(json.dumps(sensor_list))

    elif request == 'Sensors':
        conn.sendall(web_page('sensorsPage.html'))

    else :
        conn.send(web_page())