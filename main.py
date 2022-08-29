import EstacaoMetro

lista_estacoes_csv = "resources/estacoes.csv"
estacoes_coordenadas_csv = 'resources/stops.txt'

lista = EstacaoMetro.criar_estacoes(lista_estacoes_csv, estacoes_coordenadas_csv)

# EstacaoMetro.print_estacoes(lista)
print(len(lista))
