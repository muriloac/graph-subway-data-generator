import csv
import datetime
import random
import time
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

from event_variables import CLIMA, CHUVA


def generate_data(data):
    destination, stations, shortest_paths, person, edges_map_with_weights = data
    person.path = get_path_for_person(person, shortest_paths, destination)

    person_data = simulate_path_with_time(person, edges_map_with_weights, stations, random.choice(CLIMA),
                                          random.choice(CHUVA))

    with open('resources/out/data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(person_data)):
            if person_data[i][2] is not None or person_data[i][2] is not None:
                writer.writerow([person_data[i][0], person_data[i][1].strftime("%H:%M:%S"), person_data[i][2][0],
                                 person_data[i][2][1],
                                 person_data[i][3]])
            else:
                writer.writerow(
                    [person_data[i][0], person_data[i][1].strftime("%H:%M:%S"), None, None, person_data[i][3]])
            csvfile.flush()

        last_time = None
        current_time = None
        print("Iniciando envio de dados do dispositivo {}".format(person.id))
        for i in range(len(person_data)):
            if last_time is None:
                last_time = person_data[i][1]
                current_time = person_data[i][1]
            else:
                last_time = current_time
                current_time = person_data[i][1]
            time_to_sleep = (datetime.datetime.combine(datetime.date.min, current_time) - datetime.datetime.combine(
                datetime.date.min, last_time)).seconds
            if time_to_sleep > 0:
                print("Esperando {} segundos".format(time_to_sleep))
                time.sleep(time_to_sleep)
            if person_data[i][2] is not None or person_data[i][2] is not None:
                asyncio.run(
                    send_message(person.id,
                                 ''.join(map(str, [person_data[i][2][0],
                                                   person_data[i][2][1],
                                                   person_data[i][3]]))))
            else:
                asyncio.run(
                    send_message(person.id,
                                 ''.join(
                                     map(str, [None, None, person_data[i][3]]))))


async def send_message(id, data):
    conn_str = os.getenv("IOTHUB_DEVICE{}_CONNECTION_STRING".format(id))
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    await device_client.connect()
    print("Mandando mensagem do dispositivo {}".format(id))
    await device_client.send_message(data)
    print("Mensagem enviada do dispositivo {}!".format(id))
    await device_client.shutdown()


def generate_point_on_path_ratio(lat1, lon1, lat2, lon2, ratio):
    lat = lat1 + (lat2 - lat1) * ratio
    lon = lon1 + (lon2 - lon1) * ratio
    return round(lat, 3), round(lon, 3)


def read_climate_data(climate_data_file='resources/clima_chuva.csv'):
    with open(climate_data_file, 'r', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        aux = []
        for row in reader:
            aux.append([row[0], row[1], row[7]])
    return aux


def read_paths(shortest_paths_csv='resources/shortest_paths.csv'):
    with open(shortest_paths_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        aux = []
        for row in reader:
            aux.append([row[0], row[1], row[2]])
    return aux


def get_path_for_person(person, shortest_paths, destination):
    shortest_path = []
    for path in shortest_paths:
        if path[1] == str(destination) and path[0] == str(person.get_initial_station()):
            shortest_path = path[2]
            break

    return shortest_path


def simulate_path_with_time(person, edges_map_with_weights, stations, clima, chuva):
    path = person.path
    time = person.initial_time
    time_list = []
    path = path.replace("'", '').replace('[', '').replace(']', '').replace(' ', '').split(',')
    battery = person.initial_battery

    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        time_edge = edges_map_with_weights.get(edge) if edges_map_with_weights.get(
            edge) is not None else edges_map_with_weights.get(
            (path[i + 1], path[i]))
        current_station = (x for x in stations if x.id == path[i + 1]).__next__()
        last_station = (x for x in stations if x.id == path[i]).__next__()

        if chuva == 'sim' and clima == 'quente':
            time_edge = time_edge * 1.7
        elif clima == 'quente':
            time_edge = time_edge * 1.2
        elif chuva == 'sim':
            time_edge = time_edge * 1.5

        ratio = random.random()
        random_int = random.randint(0, 100)
        battery = round(battery - 0.005, 3)
        time = time + datetime.timedelta(minutes=time_edge)
        if random_int < 5:
            time_list.append((person.id, time.time(),
                              generate_point_on_path_ratio(last_station.lat, last_station.lon, current_station.lat,
                                                           current_station.lon, ratio), battery))
        elif 10 > random_int >= 5:
            time_list.append((person.id, time.time(), None, battery))
        else:
            lat, lon = current_station.get_coordenadas()
            time_list.append((person.get_id(), time.time(), (round(lat, 3), round(lon, 3)), battery))

    return time_list
