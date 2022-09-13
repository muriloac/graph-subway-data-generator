import csv
import datetime
import random

from event_variables import CLIMA, CHUVA


def generate_data(destination, stations, shortest_paths, persons, edges_map_with_weights):
    for i in range(len(persons)):
        persons[i].path = get_path_for_person(persons[i], shortest_paths, destination)

    aux = []
    for i in range(10):
        for person in persons:
            aux.append(simulate_path_with_time(person, edges_map_with_weights, stations, random.choice(CLIMA),
                                               random.choice(CHUVA)))

    with open('resources/out/data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['id','time', 'lat', 'lon'])
        for i in range(len(aux)):
            for j in range(len(aux[i])):
                writer.writerow([aux[i][j][0], aux[i][j][1], aux[i][j][2][0], aux[i][j][2][1]])


def generate_point_on_path_ratio(lat1, lon1, lat2, lon2, ratio):
    lat = lat1 + (lat2 - lat1) * ratio
    lon = lon1 + (lon2 - lon1) * ratio
    return lat, lon


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

    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        time_edge = edges_map_with_weights.get(edge) if edges_map_with_weights.get(
            edge) is not None else edges_map_with_weights.get(
            (path[i + 1], path[i]))
        current_station = (x for x in stations if x.id == path[i + 1]).__next__()

        if chuva == 'sim' and clima == 'quente':
            time_edge = time_edge * 1.7
        elif clima == 'quente':
            time_edge = time_edge * 1.2
        elif chuva == 'sim':
            time_edge = time_edge * 1.5

        time = time + datetime.timedelta(minutes=time_edge)
        time_list.append((person.get_id(), time.time(), current_station.get_coordenadas()))

    return time_list
