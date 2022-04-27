from pulp import *
import pandas as pd

# Criando o problema de LP com o método LpProblem do pulp
prop = LpProblem("Project_Problem", LpMinimize)

df = pd.read_excel("modelo.xlsx", sheet_name=3)

# Dados dos projetos e restrições
data = df.iloc[2:20, 2:9]
rest = df.iloc[23:35, 2:3]

projectList = []
paList = []
ciList = []
hiList = []
xiList = []

restList = []

for i in rest.values:
    restList.append(i[0])

for i in data.values:
    xiList.append(i[3])
    hiList.append(i[2])
    ciList.append(i[1])  # Substituir "-" por 0???
    paList.append(i[0])
    projectList.append(i[5])

print(f'RESTRIÇÕES {restList}')
print(f'PROJETOS {projectList}')

# Dicionário com os respectivos atributos dos projetos
pa = dict(zip(projectList, paList))
ci = dict(zip(projectList, ciList))
hi = dict(zip(projectList, hiList))
xi = dict(zip(projectList, xiList))

print(f'EXEMPLO DO DICIONÁRIO DOS PROJETOS COM O ATRIBUTO CI\n {ci}\n')

# Criação das variáveis de decisão para números inteiros
projects_vars = LpVariable.dicts("Projects", projectList, lowBound=0, cat='Integer')

# Criação da função objetivo para o somatório do custo unitário pela unidade métrica
prop += lpSum([ci[i]*projects_vars[i] for i in projectList])  # função objetivo

prop += lpSum([ci[i] * projects_vars[i] for i in projectList]) >= restList[0]
prop += lpSum([hi[i] * xi[i] * projects_vars[i] for i in projectList]) >= restList[3]

status = prop.solve()
LpStatus[status]

# Projetos selecionados
for p in prop.variables():
    if p.varValue > 0:
        print(p.name)

print(value(prop.objective))
