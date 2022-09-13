import csv
from difflib import SequenceMatcher

from EstacaoMetro import criar_estacoes


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def normalize(s):
    return s.lower().replace(' ', '')


def resolve_csv(lista_estacoes, estacoes_edge='resources/estacoes_edges.csv'):
    with open(estacoes_edge, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        aux = []
        for row in reader:
            estacao1 = normalize(row[0])
            estacao2 = normalize(row[1])
            tempo = row[2]
            cor = row[3]
            for estacao in lista_estacoes:
                if similar(estacao1, normalize(estacao.nome)) > 0.8:
                    estacao1 = estacao.id
                if similar(estacao2, normalize(estacao.nome)) > 0.8:
                    estacao2 = estacao.id
            aux.append([estacao1, estacao2, tempo, cor])

    with open('resources/estacoes_edges_resolved.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['estacao1', 'estacao2', 'tempo', 'cor'])
        for row in aux:
            writer.writerow(row)


resolve_csv(criar_estacoes())
