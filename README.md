# Distribuição de Reservas - API

Este é um projeto de demonstração que fornece uma API Flask para distribuir valores de reservas entre proprietários e anfitriões com base no ID da propriedade.

## Requisitos

- Python 3.x
- Biblioteca flask  

## Execução

1. **Execute o aplicativo:**

    '''bash
    python distribuicao_receitas.py
    '''

2. **Se a execução for diretamente na maquina local (localhost), a API estará disponível em 'http://127.0.0.1:5000/'. Acesse esse endereço em seu navegador ou utilize ferramentas como [Postman](https://www.postman.com/) para interagir com a API.**

3. **Massa de testes: No diretório raiz onde está o arquivo de execução do código Python deve ser criado o subdiretório 'reservas/csv' para armazenar os arquivos ".csv" com as reservas.
Neste repositorio (sapron_project) foi criado o subdiretório 'reservas/csv' com um arquivo simples para testes testes chamado arq_1.csv

## Uso da API

### Distribuir Reserva

- **Endpoint:** '/distribuir_receita'
- **Método:** GET
- **Parâmetros:**
  - 'propriedade_id' (obrigatório): ID da propriedade para distribuição de reservas.

**Exemplo**

Em um cliente de API, como o Postman, executar a URL http://127.0.0.1:5000/distribuir_receita?propriedade_id=5001, para calcular a distribuição da propriedade 5001.

**Resultado**

Será gerado, no mesmo diretório do código Python, um novo arquivo ".csv" com a distribuição de receitas entre o proprietário e o anfitrião, agrupados por mês.
O nome desse arquivo será da seguinte forma: distribuicao_yyyymmddhhMMss.csv.
