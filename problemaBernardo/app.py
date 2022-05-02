import pandas as pd
from flask import Flask, render_template, request, flash, send_file, url_for, jsonify
from main import metodo_TOPSIS
from PLI import metodo_PLI
#from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, IMAGES

app = Flask(__name__)
#app.secret_key = "super mega blaster key"
#app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    metodo = request.form['method']
    print(file)
    print(request.form['method'])
    if metodo == '1':
        print(' COMEÇANDO METODO TOPSIS:')
        print('================================================')
        value = 'TOPSIS'
        resultado = metodo_TOPSIS()
        #print(resultado.TOPSIS())
        #print(value)
        ranqTopsis, ranqTopsisInvertido = resultado.TOPSIS()
        print(ranqTopsis)
        print(ranqTopsisInvertido)
        return 'Ranqueamento TOPSIS: ' + str(ranqTopsis) + ' Ranqueamento TOPSIS invertido: ' + str(ranqTopsisInvertido)
    elif metodo == '2':
        print('COMEÇANDO METODO PLI:')
        print('================================================')
        value = 'PLI'
        #resultado = metodo_PLI()
        restList = [request.form['rest1'], request.form['rest2'], request.form['rest3'], request.form['rest4'], request.form['rest5'],
                    request.form['rest6'], request.form['rest7'], request.form['rest8'], request.form['rest9'], request.form['rest10'], request.form['rest11']]
        print(restList)
        resultado = metodo_PLI()
        inputTest = [x for x in restList if x != '']
        if not inputTest:
            print('NO INPUTS TO COMPARE')
            resultado, projetos = resultado.PLI(restList)
            stringResultado = 'Resultados do método PLI - PROJETOS SELECIONADOS: \n' + str(
                projetos) + '\n' + 'Prop objeticve value: ' + str(resultado)
            return stringResultado
        else:
            resultado1, projetos1, resultado2, projetos2 = resultado.PLI(restList)
            stringResultado = 'Resultados do método PLI número 1 - PROJETOS SELECIONADOS: \n' + str(projetos1) + '\n' + 'Prop objeticve value: ' + str(resultado1) + 'Resultados do método PLI número 2 - PROJETOS SELECIONADOS: \n' + str(projetos2) + '\n' + 'Prop objeticve value: ' + str(resultado2)
            return stringResultado

        #print(value)
        #return print(resultado.PLI())
    print(file)
    #df = pd.read_excel(file)

if __name__ == '__main__':
    app.run()
