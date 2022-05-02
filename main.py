import pandas as pd
import numpy as np
#MÉTODO TOPSIS
## QUADRO 1 - CRITÉRIOS

nomeArq = "modelo.xlsx" #qualquer erro de importação, alterar o local do arquivo pra o caminho completo
projeto = []

df = pd.read_excel(f"{nomeArq}") #add o parametro  sheet_name =  para abrir outras abas da planilha

metTopsisColA = df.iloc[3:18,2:10] #matriz, com a tabela critérios, da coluna A até a H
metTopsisColASq = np.square(metTopsisColA) #todos os valores da matriz ao quadrado
metTopsisColASum = metTopsisColASq.sum() #soma de todos valores da matriz por coluna

normalizacao = []
PESOS = float(1/8)

for i in metTopsisColASum:
    normalizacao.append(float((f'{np.sqrt(i):.2f}'))) #faz a raiz quadrada em cada valor da soma de cada coluna individualmente, os valores têm duas casas decimais

#QUADRO 2 - CRITÉRIOS 
quadro2 = {}

for col in range(metTopsisColA.shape[1]):
    quadro2[f'coluna{col}'] = []
    for lin in range(metTopsisColA.shape[0]):
        quadro2[f'coluna{col}'].append(round((metTopsisColA.iloc[lin,col]/normalizacao[col]*PESOS),4))

idealPosNeg = [[],[]] #array duplo para não ter a necessidade de criar dois laços pra "min() e max()"
quadro2Dtf = pd.DataFrame(quadro2)

for i in quadro2.keys(): #lista 1 recebe os valores max (ideal positiva) e a lista 2 recebe os minimos (ideal negativa)
    #o condicional inverte o min e máx de acordo com a legenda de critérios (pra ficar mais dinâmico pode ser necessário mudar os teste de condicionais, obs planilha)
    if i == 'coluna5' or i == 'coluna6' or i == 'coluna7':
        quadro2[i].append(quadro2Dtf[i].min())
        quadro2[i].append(quadro2Dtf[i].max())
    else: 
        quadro2[i].append(quadro2Dtf[i].max())
        quadro2[i].append(quadro2Dtf[i].min())

dMaisDMenos = [[],[],[]]
valorTempDMais = 0
valorTempDMenos = 0

for i in range(len(quadro2[f'coluna0'])-2): #por questões de arredondamentos os resultados estão próximos, mas não literalmente iguais ao da planilha
    for j in range(len(quadro2.keys())):
        valorTempDMais += (quadro2[f'coluna{j}'][i] - quadro2[f'coluna{j}'][-2])**2 #para d+
        valorTempDMenos += (quadro2[f'coluna{j}'][i] - quadro2[f'coluna{j}'][-1])**2 #para d-
    valorTempDMais = round((np.sqrt(valorTempDMais)),7)
    valorTempDMenos = round((np.sqrt(valorTempDMenos)),7)
    dMaisDMenos[0].append(valorTempDMais)
    dMaisDMenos[1].append(valorTempDMenos)
    dMaisDMenos[2].append(round((valorTempDMenos / (valorTempDMenos + valorTempDMais)),6)) #para D
    valorTempDMais = 0
    valorTempDMenos = 0

#add a coluna d+, d- e D à tabela
quadro2['coluna8'] = dMaisDMenos[0] 
quadro2['coluna9'] = dMaisDMenos[1]
quadro2['coluna10'] = dMaisDMenos[2]

#Ranqueamento TOPSIS
#deixando a tabela com mesmo número de linhas pra cada coluna (pra que se possa transformar em dataframe)
#uma alternativa a isso seria anteriormente criar uma planilha paralela com a normalização separada da "original", apenas pra fins de cálculo
for i in quadro2.keys():
    if not(i== 'coluna8' or i == 'coluna9' or i == 'coluna10'):
        quadro2[i].pop()
        quadro2[i].pop()

quadro2Dtf = pd.DataFrame(quadro2)

#ordenação/ranqueamento pelo D:
ranqTopsis = quadro2Dtf.sort_values(by = 'coluna10', ascending= False)
ranqTopsisInvertido = quadro2Dtf.sort_values(by = 'coluna10') #ranqueado, porém tá de trás pra frente

#debug mostrar tabela ordenada (os prints devem ser excluídos futuramente)
print(ranqTopsis) 
print(ranqTopsisInvertido)

#legenda da planilha:
#coluna 0 até 7 (colunas de A até H), colunas 8 até 10 (d+, d-, D)
#nomes dos projetos não foram colocados ainda pq devemos decidir como ficará nos inputos de usuários