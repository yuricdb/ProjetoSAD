import pandas as pd
import numpy as np
#MÉTODO TOPSIS
## QUADRO 1 - CRITÉRIOS

nomeArq = "modelo.xlsx" #qualquer erro de importação, alterar o local do arquivo pra o caminho completo.
projeto = []

df = pd.read_excel(f"{nomeArq}") #add o parametro  sheet_name =  para abrir outras abas da planilha

metTopsisColA = df.iloc[3:18,2:10] #matriz, com a tabela critérios, da coluna A até a H
metTopsisColASq = np.square(metTopsisColA) #todos os valores da matriz ao quadrado
metTopsisColASum = metTopsisColASq.sum() #soma de todos valores da matriz por coluna

#normalizacao = np.sqrt(metTopsisColASum) #raiz quadrada de todos os valores por colunas somados
#print(normalizacao)
normalizacao = []

for i in metTopsisColASum:
    normalizacao.append(float((f'{np.sqrt(i):.2f}'))) #faz a raiz quadrada em cada valor da soma de cada coluna individualmente, os valores têm duas casas decimais

PESOS = float(1/8)

print(normalizacao) #debugando valores batem com a planilha


#QUADRO 2 - CRITÉRIOS 

