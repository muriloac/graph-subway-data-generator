import os

import networkx as nx
import csv

import EstacaoMetro
import generator
import Person
from datetime import datetime
from multiprocessing import Pool


def main():
    print("Criando estacoes...")
    stations = EstacaoMetro.criar_estacoes()

    print("Criando rede de estacoes...")
    g_map = EstacaoMetro.build_station_network()

    edges_map, colors = zip(*nx.get_edge_attributes(g_map, 'color').items())
    edges_map_with_weights = nx.get_edge_attributes(g_map, 'weight')

    print("Desenhando o mapa do metro")
    EstacaoMetro.draw_network(g_map, edges_map, color=colors)

    print("Calculando os caminhos mais curtos")
    EstacaoMetro.shortest_paths(g_map)
    shortest_paths = generator.read_paths()

    print("Gerando pessoas")
    persons = Person.generate_persons(stations, 60, datetime.now())

    print("Quantos dispositivos vão ser simulados? MAX 60")
    qtd_simulados = int(input('Input: '))

    pool_handler(qtd_simulados, 18850, stations, shortest_paths, persons, edges_map_with_weights)


def pool_handler(qtd_simulados, destination, stations, shortest_paths, persons, edges_map_with_weights):
    p = Pool(qtd_simulados)
    data = []
    for i in range(qtd_simulados):
        data.append((destination, stations, shortest_paths, persons[i], edges_map_with_weights))
    with open('resources/out/data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['person_id', 'time', 'lat', 'lon', 'battery'])
        csvfile.close()
    p.map(generator.generate_data, data)


if __name__ == '__main__':
    main()
