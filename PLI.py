from pulp import *
import pandas as pd
import sys

class metodo_PLI:
    #Constructor
    def __int__(self):
        sys.setrecursionlimit(1000)

    def PLI(self, restListInput): #arquivo vem aqui e pesos que quiser customizar
        # COLOCAR O ´compareTrigger´ = 1 para testes
        compareTrigger = 0
        df = pd.read_excel("modelo.xlsx", sheet_name=3)

        rest = df.iloc[23:35, 2:3]
        restList = []
        for i in rest.values:
            restList.append(i[0])

        restList2 = restList.copy()

        df = pd.read_excel("modelo.xlsx", sheet_name=3)

        # Dados dos projetos e restrições
        data = df.iloc[2:20, 2:9]

        projectList = []
        paList = []
        ciList = []
        hiList = []
        xiList = []
        xaList = []
        xbList = []
        xcList = []
        xdList = []
        xr1List = []
        xr2List = []
        xr3List = []

        cont = 0
        for i in data.values:
            if cont < 9:
                xaList.append(1)
                xbList.append(0)
                xcList.append(0)
                xdList.append(0)
                xr1List.append(0)
                xr2List.append(0)
                xr3List.append(0)
            elif cont == 9:
                xbList.append(1)
                xaList.append(0)
                xcList.append(0)
                xdList.append(0)
                xr1List.append(0)
                xr2List.append(0)
                xr3List.append(0)
            elif cont > 9 and cont < 14:
                xcList.append(1)
                xaList.append(0)
                xbList.append(0)
                xdList.append(0)
                xr1List.append(0)
                xr2List.append(0)
                xr3List.append(0)
            elif cont == 14:
                xdList.append(1)
                xaList.append(0)
                xcList.append(0)
                xbList.append(0)
                xr1List.append(0)
                xr2List.append(0)
                xr3List.append(0)
            elif cont == 15:
                xr1List.append(1)
                xaList.append(0)
                xcList.append(0)
                xdList.append(0)
                xbList.append(0)
                xr2List.append(0)
                xr3List.append(0)
            elif cont == 16:
                xr2List.append(1)
                xaList.append(0)
                xcList.append(0)
                xdList.append(0)
                xr1List.append(0)
                xbList.append(0)
                xr3List.append(0)
            elif cont == 17:
                xr3List.append(1)
                xaList.append(0)
                xcList.append(0)
                xdList.append(0)
                xr1List.append(0)
                xr2List.append(0)
                xbList.append(0)
            xiList.append(i[3])
            hiList.append(i[2])
            ciList.append(i[1])
            paList.append(i[0])
            projectList.append(i[5])
            cont += 1

        # Dicionário com os respectivos atributos dos projetos
        pa = dict(zip(projectList, paList))
        ci = dict(zip(projectList, ciList))
        hi = dict(zip(projectList, hiList))
        xi = dict(zip(projectList, xiList))
        xa = dict(zip(projectList, xaList))
        xb = dict(zip(projectList, xbList))
        xc = dict(zip(projectList, xcList))
        xd = dict(zip(projectList, xdList))
        xr1 = dict(zip(projectList, xr1List))
        xr2 = dict(zip(projectList, xr2List))
        xr3 = dict(zip(projectList, xr3List))

        # Criação das variáveis de decisão para números inteiros
        projects_vars = LpVariable.dicts("Projects", projectList, lowBound=0, cat='Integer')

        #Checando se inputaram alguma restrição
        inputTest = [x for x in restListInput if x != 'default input value']
        if not inputTest:
            pass
        else:
            #Caso tenham inputado, trigger de comparação vai pra 1 e retorna os valores das 2 props
            compareTrigger = 1
            cont = 0
            for x in restListInput:
                if x != 'default input value':
                    restList2[cont] = x
                    cont=cont+1
                else:
                    pass
            # Criando o problema de LP com o método LpProblem do pulp
            prop2 = LpProblem("Project_Problem", LpMinimize)

            # Criação da função objetivo para o somatório do custo unitário pela unidade métrica
            prop2 += lpSum([ci[i] * projects_vars[i] for i in projectList])  # função objetivo

            prop2 += lpSum([ci[i] * projects_vars[i] for i in projectList]) >= restList2[0]
            prop2 += lpSum([ci[i] * xi[i] * projects_vars[i] for i in projectList]) >= restList2[1]
            prop2 += lpSum([hi[i] * projects_vars[i] for i in projectList]) >= restList2[2]
            prop2 += lpSum([hi[i] * xi[i] * projects_vars[i] for i in projectList]) >= restList2[3]
            prop2 += lpSum([xa[i] * projects_vars[i] for i in projectList]) >= restList2[4]
            prop2 += lpSum([xb[i] * projects_vars[i] for i in projectList]) >= restList2[5]
            prop2 += lpSum([xc[i] * projects_vars[i] for i in projectList]) >= restList2[6]
            prop2 += lpSum([xd[i] * projects_vars[i] for i in projectList]) >= restList2[7]
            prop2 += lpSum([xr1[i] * projects_vars[i] for i in projectList]) >= restList2[8]
            prop2 += lpSum([xr2[i] * projects_vars[i] for i in projectList]) >= restList2[9]
            prop2 += lpSum([xr3[i] * projects_vars[i] for i in projectList]) >= restList2[10]

            status = prop2.solve()
            LpStatus[status]

            # Projetos selecionados
            print('PROJETOS SELECIONADOS PARA OS PESOS SELECIONADOS PELO USUÁRIO')
            for p in prop2.variables():
                if p.varValue > 0:
                    print(p.name)
            print()

        # Criando o problema de LP com o método LpProblem do pulp
        prop = LpProblem("Project_Problem", LpMinimize)

        # Criação da função objetivo para o somatório do custo unitário pela unidade métrica
        prop += lpSum([ci[i]*projects_vars[i] for i in projectList])  # função objetivo

        prop += lpSum([ci[i] * projects_vars[i] for i in projectList]) >= restList[0]
        prop += lpSum([ci[i] * xi[i] * projects_vars[i] for i in projectList]) >= restList[1]
        prop += lpSum([hi[i] * projects_vars[i] for i in projectList]) >= restList[2]
        prop += lpSum([hi[i] * xi[i] * projects_vars[i] for i in projectList]) >= restList[3]
        prop += lpSum([xa[i] * projects_vars[i] for i in projectList]) >= restList[4]
        prop += lpSum([xb[i] * projects_vars[i] for i in projectList]) >= restList[5]
        prop += lpSum([xc[i] * projects_vars[i] for i in projectList]) >= restList[6]
        prop += lpSum([xd[i] * projects_vars[i] for i in projectList]) >= restList[7]
        prop += lpSum([xr1[i] * projects_vars[i] for i in projectList]) >= restList[8]
        prop += lpSum([xr2[i] * projects_vars[i] for i in projectList]) >= restList[9]
        prop += lpSum([xr3[i] * projects_vars[i] for i in projectList]) >= restList[10]

        status = prop.solve()
        LpStatus[status]

        # Projetos selecionados
        print('PROJETOS SELECIONADOS')
        for p in prop.variables():
            if p.varValue > 0:
                print(p.name)

        # Return dos objetivos da prop, 0 = sem comparação, 1 = com input do usuário, comparação
        if compareTrigger == 0:
            print(value(prop.objective))
        elif compareTrigger == 1:
            print(value(prop.objective), value(prop2.objective))

# EXEMPLO TESTE
# pli = metodo_PLI()
# pli.PLI([1653654, 823459, 6234, 3213, 5, 1, 1, 1, 1, 1, 1, 400])
