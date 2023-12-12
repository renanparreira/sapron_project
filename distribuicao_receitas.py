import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

class Reserva:
    def __init__(self, propriedade_id, data_reserva, valor_reserva, proprietario_id, anfitriao_id, percentual_proprietario, percentual_anfitriao):
        self.propriedade_id = propriedade_id
        self.data_reserva = datetime.strptime(data_reserva, "%Y-%m-%d")
        self.valor_reserva = float(valor_reserva)
        self.proprietario_id = proprietario_id
        self.anfitriao_id = anfitriao_id
        self.percentual_proprietario = float(percentual_proprietario)
        self.percentual_anfitriao = float(percentual_anfitriao)

class DistribuidorReceita:
    def __init__(self, diretorio_csv):
        self.diretorio_csv = diretorio_csv
        self.reservas = []

    def carregar_reservas(self, propriedade_id):
        #Itera sobre os arquivos no diretório CSV
        for filename in os.listdir(self.diretorio_csv):
            if filename.endswith(".csv"):
                #Lê cada arquivo CSV e adiciona as reservas correspondentes à lista
                with open(os.path.join(self.diretorio_csv, filename), mode='r') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:                        
                        if row['propriedade_id'] == propriedade_id:
                            reserva = Reserva(**row)
                            self.reservas.append(reserva)
 
    #Calcula a distribuicao de receitas
    def calcular_distribuicao(self):
        resultados = {}
        for reserva in self.reservas:
            mes_ano = reserva.data_reserva.strftime("%m/%Y")
            valor_calculado_proprietario = reserva.valor_reserva * (reserva.percentual_proprietario / 100)
            valor_calculado_anfitriao = reserva.valor_reserva * (reserva.percentual_anfitriao / 100)

            # Agrupa os resultados por mês
            if mes_ano not in resultados:
                #resultados[mes_ano] = {'Proprietario': 0, 'Anfitriao': 0}
                resultados[mes_ano] = {'ID_Propriedade': reserva.propriedade_id,'ID_Proprietario': reserva.proprietario_id, 'Proprietario': 0, 'ID_Anfitriao': reserva.anfitriao_id, 'Anfitriao': 0}

            resultados[mes_ano]['Proprietario'] += valor_calculado_proprietario
            resultados[mes_ano]['Anfitriao'] += valor_calculado_anfitriao

        print('resultados:')
        print(resultados)

        return resultados

    #Gera novo arquico CSV com a distribuição de receitas
    def gerar_distriuicao_receitas(self, resultados):
        # Salva os resultados em um novo arquivo CSV
        agora = datetime.now()
        data_hora = agora.strftime("%Y%m%d%H%M%S")
        arq_distribuicao = f'distribuicao_{data_hora}.csv'
        with open(arq_distribuicao, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            #writer.writerow(['Mes', 'Valor_Proprietario', 'Valor_Anfitriao'])
            writer.writerow(['ID_Propriedade', 'Mes', 'ID_Proprietario', 'Valor_Proprietario', 'ID_Anfitriao', 'Valor_Anfitriao'])

            for mes_ano, valores in resultados.items():
                #writer.writerow([mes_ano, round(valores['Proprietario'],2), round(valores['Anfitriao'],2)])
                writer.writerow([valores['ID_Propriedade'], mes_ano, valores['ID_Proprietario'], round(valores['Proprietario'],2), valores['ID_Anfitriao'], round(valores['Anfitriao'],2)])

        return arq_distribuicao

#Servico criado no caminho /distribuir_receita. Foi utilizado metodo get para obter o ID da propriedade 
#TODO Refatorar o codigo para realizar o calculo da distribução de receitas nao apenas por id de propriedade mas tambem de um periodo especifico de todas as propriedades
@app.route('/distribuir_receita', methods=['GET'])
def distribuir_reserva():
    try:
        propriedade_id = request.args.get('propriedade_id')

        if not propriedade_id:
            raise ValueError('ID da propriedade deve ser fornecido.')

        #Diretório exemplo onde estão armazenados os arquivos CSV
        diretorio_csv = 'reservas/csv'  
        
        distribuidor = DistribuidorReceita(diretorio_csv)
        distribuidor.carregar_reservas(propriedade_id)

        #Calcula a distribuição de receitas e gera em um novo arquivo CSV com o resultado 
        resultados = distribuidor.calcular_distribuicao()
        output_file = distribuidor.gerar_distriuicao_receitas(resultados)

        return jsonify({'status': 'success', 'message': f'Distribuição de receitas gerada no arquivo {output_file}'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
