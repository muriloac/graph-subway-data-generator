import csv
from difflib import SequenceMatcher
from unidecode import unidecode


class EstacaoMetro:
    def __init__(self, nome, linha, lat, lon):
        self.nome = nome
        self.linha = linha
        self.lat = lat
        self.lon = lon

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
        return self.nome + " - " + self.linha + " - " + self.lat + " - " + self.lon


def criar_estacoes(lista_estacoes_file, estacoes_coordenadas_file):
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
            estacoes_coordenadas.append([row[1], row[3], row[4]])

        for i in range(len(lista_estacoes)):
            for j in range(len(estacoes_coordenadas)):
                if similar(lista_estacoes[i][1], estacoes_coordenadas[j][0]) > 0.8:
                    final_list.append(
                        EstacaoMetro(lista_estacoes[i][1], lista_estacoes[i][0], estacoes_coordenadas[j][1],
                                     estacoes_coordenadas[j][2]))
                    break

    return final_list


def print_estacoes(estacoes):
    for i in range(len(estacoes)):
        print(estacoes[i])


def similar(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def normalize(text):
    return unidecode(text).lower()
