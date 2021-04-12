import random
import pandas as pd
from MergeSort import mergeSort


unidades_de_saude = [ 'São João Del Rey',	'Waldemar Monastier',	'Bacacheri',	'Cajuru',
	'São Miguel',	'Mãe Curitibana',	'Fanny Landóia',	'Santa Quitéria 1',
    'Bom Pastor',	'Santa Rita']

dict_us = {
    'São João Del Rey': 0,
    'Waldemar Monastier': 1,
    'Bacacheri': 2,
    'Cajuru': 3,
	'São Miguel': 4,
    'Mãe Curitibana': 5,
    'Fanny Landóia': 6,
    'Santa Quitéria 1': 7,
    'Bom Pastor': 8,
    'Santa Rita': 9,
    'Rodoviária': 10
}

distancias = pd.read_excel('distancias.xlsx')
media_de_tempo = pd.read_excel('media_de_tempo.xlsx', index_col=0, header=0)
# define o tamanho da população
tamPopulacao = 50
# define a taxa de recombinção entre 0 e 1
taxa_recombinacao = 0.7
# define a taxa de mutação entre 0 e 1
taxa_mutacao = 0.4
# define o número de gerações
geracoes = 50
# Considera transito ou não
com_transito = 'nao'

def preencheRotaAleatoria():
    # produzindo uma rota de forma aleatória
    rota = random.sample(unidades_de_saude, 10)
    # inserindo a rodoviária como ponto de partida
    rota.insert(0,'Rodoviária')
    # inserindo a rodoviária como ponto final
    rota.append('Rodoviária')
    return rota

def criarPopulação():
    populacao = []
    
    for index in range(tamPopulacao):
        individuo = {}
        individuo['rota'] = preencheRotaAleatoria()
        individuo['tempo_gasto'] = calculaTempoTrajeto(individuo['rota'])
        # print(individuo)
        populacao.append(individuo)
    
    return populacao

def calculaTempoTrajeto(rota):
    tempo = 0

    # Simulação do transito
    # Transito leve = x1
    # Transito médio = x1.5
    # Transito pesado = x2
    transito = [1, 1.5, 2]

    for index in range(len(rota)-1):
        # define a unidade atual
        us_atual = rota[index]
        # defina a próxima unidade a ser visitada
        us_proxima = rota[index+1]

        # busca no tabela de tempos a o tempo em minutos da unidade atual até a proxima
        # Para isso é usando o dicionário de unidades de saúde que relaciona as US com os indexes da tabela
        if(com_transito):
            tempo = tempo + (media_de_tempo.values[dict_us[us_atual]][dict_us[us_proxima]].minute)
        else:
            tempo = tempo + (media_de_tempo.values[dict_us[us_atual]][dict_us[us_proxima]].minute * transito[random.randint(0,2)])

    # retorna o tempo em minutos
    return tempo

def recombinacao(func_populacao):
    num_individuos = int((tamPopulacao*taxa_recombinacao)//1)
    if num_individuos%2 != 0:
        num_individuos = num_individuos +1

    filhos_recombinacao = []

    # Seleciona os indivíduos que sofrerão a recombinação
    individuos_selecionados = random.sample(range(0,tamPopulacao), num_individuos)

    for i in range(0, len(individuos_selecionados), 2):

        # Para implementar mundando mais do que uma cidade, basta adicionar um loop aqui
        # com o número de vezes que sejam alteradas as unidades de saúde

        filho_01 = {}
        filho_01['rota'] = func_populacao[individuos_selecionados[i]]['rota'].copy()
        filho_02 = {}
        filho_02['rota'] = func_populacao[individuos_selecionados[i+1]]['rota'].copy()
        

        # Seleciona aleatóriamente quais unidades de saúde serão trocadas
        # Sempre deixando de lado a rodoviária
        index_us_trocada = random.randint(1,10)

        # Busca no primeiro indivíduo da recombinação qual é a unidade de saúde que será trocada
        us_trocada_01 = filho_01['rota'][index_us_trocada]

        # Busca no segundo indivíduo da recombinação qual é a unidade de saúde que será trocada
        us_trocada_02 = filho_02['rota'][index_us_trocada]

        # Busca no primeiro indivíduo qual a posição da segunda unidade de saúde que participa da troca
        aux = filho_01['rota'].index(us_trocada_02)

        # Faz a troca das posições das duas unidades de saúdes no primeiro indivíduo
        filho_01['rota'][index_us_trocada] = us_trocada_02
        filho_01['rota'][aux] = us_trocada_01

        # Busca no segundo indivíduo qual a posição da primeira unidade de saúde que participa da troca
        aux = filho_02['rota'].index(us_trocada_01)

        # Faz a troca das posições das duas unidades de saúdes no segundo indivíduo
        filho_02['rota'][index_us_trocada] = us_trocada_01
        filho_02['rota'][aux] = us_trocada_02



        # Recalcula o tempo gasto
        filho_01['tempo_gasto'] = calculaTempoTrajeto(filho_01['rota'])
        filho_02['tempo_gasto'] = calculaTempoTrajeto(filho_02['rota'])

        filhos_recombinacao.append(filho_01)
        filhos_recombinacao.append(filho_02)

    return filhos_recombinacao

def mutacao(func_populacao):
    num_individuos = int((tamPopulacao*taxa_mutacao)//1)

    filhos_mutacao = []
    
    # Seleciona os indivíduos que sofrerão a mutação
    individuos_selecionados = random.sample(range(0,tamPopulacao), num_individuos)

    for i in individuos_selecionados:
        # Seleciona aleatóriamente quais unidades de saúde serão trocadas
        us_trocada_01 = random.randint(1,10)
        us_trocada_02 = random.randint(1,10)

        if us_trocada_01 != us_trocada_02:
            filho_01 = {}
            filho_01['rota'] = func_populacao[i]['rota'].copy()
            # Realiza a troca das posições entre as unidades de saúde
            auxiliar =filho_01['rota'][us_trocada_01]
            filho_01['rota'][us_trocada_01] = filho_01['rota'][us_trocada_02]
            filho_01['rota'][us_trocada_02] = auxiliar

            # Recalcula o tempo gasto no trajeto
            filho_01['tempo_gasto'] = calculaTempoTrajeto(filho_01['rota'])

            filhos_mutacao.append(filho_01)

    return filhos_mutacao


def algoritmo_genetico():
    for i in range(geracoes):
        populacao = criarPopulação()
        filhos = []
        filhos.extend(recombinacao(populacao))
        filhos.extend(mutacao(populacao))

        # Substitui os piores indivíduos pelos filhos
        mergeSort(populacao) 
        for i in range(len(filhos)):
            if len(populacao) != 0:
                populacao.pop()
            else:
                break
        populacao.extend(filhos)

    mergeSort(populacao) 
    return populacao[0]

resultados = []

for i in range(10):
    resultados.append(algoritmo_genetico())

mergeSort(resultados)
print(resultados[0])

