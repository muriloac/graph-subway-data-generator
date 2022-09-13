import networkx as nx

import EstacaoMetro
import generator
import Person
import datetime

stations = EstacaoMetro.criar_estacoes()

G_map = EstacaoMetro.build_station_network()

edges_map, colors = zip(*nx.get_edge_attributes(G_map, 'color').items())
edges_map_with_weights = nx.get_edge_attributes(G_map, 'weight')
EstacaoMetro.draw_network(G_map, edges_map, color=colors)
EstacaoMetro.shortest_paths(G_map)

shortest_paths = generator.read_paths()
climate = generator.read_climate_data()
persons = Person.generate_persons(stations, 60, datetime.datetime(100, 1, 1, 18, 0, 0))

generator.generate_data(18850, stations, shortest_paths, persons, edges_map_with_weights)
