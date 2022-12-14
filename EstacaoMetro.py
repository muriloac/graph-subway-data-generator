import csv
from difflib import SequenceMatcher
from itertools import chain

import matplotlib.pyplot as plt
from unidecode import unidecode
import networkx as nx


class EstacaoMetro:
    def __init__(self, id, nome, linha, lat, lon):
        self.id = id
        self.nome = nome
        self.linha = linha
        self.lat = float(lat)
        self.lon = float(lon)

    def get_id(self):
        return self.id

    def get_nome(self):
        return self.nome

    def get_linha(self):
        return self.linha

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_coordenadas(self):
        return self.lat, self.lon

    def __str__(self):
        return f"EstacaoMetro(id={self.id}, nome={self.nome}, linha={self.linha}, lat={self.lat}, lon={self.lon})"


def criar_estacoes(lista_estacoes_file="resources/estacoes.csv", estacoes_coordenadas_file='resources/stops.txt'):
    lista_estacoes = []
    estacoes_coordenadas = []
    final_list = []

    with open(lista_estacoes_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            lista_estacoes.append([row[0], row[1]])

    with open(estacoes_coordenadas_file, 'r', encoding='utf-8') as txfile:
        reader = csv.reader(txfile)
        next(reader)
        for row in reader:
            row[1] = row[1].replace('"', '')
            estacoes_coordenadas.append([row[0], row[1], row[3], row[4]])

        for i in range(len(lista_estacoes)):
            for j in range(len(estacoes_coordenadas)):
                if similar(lista_estacoes[i][1], estacoes_coordenadas[j][1]) > 0.8:
                    final_list.append(
                        EstacaoMetro(estacoes_coordenadas[j][0], lista_estacoes[i][1], lista_estacoes[i][0],
                                     estacoes_coordenadas[j][2],
                                     estacoes_coordenadas[j][3]))
                    break

    return final_list


def print_estacoes(estacoes):
    for i in range(len(estacoes)):
        print(estacoes[i])


def similar(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def normalize(text):
    return unidecode(text).lower()


def build_station_network(filename='resources/estacoes_edges_resolved.csv'):
    t_map = nx.Graph()

    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            (source, destination, time, color) = (row[0], row[1], row[2], row[3])
            color = color.replace('\n', '')
            t_map.add_edge(source, destination, weight=float(time), color=color)

    return t_map


def draw_network(G, edges, color='black', new_plot=True, title='Metro SP', label=None):
    locations = {}
    nodes = list(chain(*edges))
    for station in criar_estacoes():
        locations[station.get_id()] = station.get_coordenadas()

    if new_plot:
        plt.figure()
        plt.title(title)
    if label is not None:
        nx.draw_networkx_labels(G, pos=locations, labels=label, font_size=6)
    nx.draw_networkx_edges(G, pos=locations, edge_color=color, edgelist=edges)
    nx.draw_networkx_nodes(G, pos=locations, node_color='black',
                           node_size=20, nodelist=nodes)
    plt.show()


def all_paths(G, source, target, cutoff=None):
    paths = []
    for path in nx.all_simple_paths(G, source=source, target=target, cutoff=cutoff):
        paths.append(path)
    return paths


def path_length(G, x):
    length = 0
    for i in range(len(x) - 1):
        length += G[x[i]][x[i + 1]]['weight']
    return length


def shortest_paths(G, cutoff=None):
    shortest_paths_list = []

    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                paths = all_paths(G, source, target, cutoff)
                shortest_path = min(paths, key=lambda x: path_length(G, x))
                shortest_paths_list.append(shortest_path)

    with open('resources/shortest_paths.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['source', 'target', 'path'])
        for path in shortest_paths_list:
            writer.writerow([path[0], path[-1], path])
