import requests 
import csv
from datetime import datetime

ano = 2010

tipos_de_proposicoes = ["PL", "PEC", "PLP", "MPV", "MSC", "MSG", "PDC", "PLN", "PLV", "PRC", "VET"] 
soma = 0
soma_pl = 0
soma_pec = 0
soma_plp = 0
soma_mpv = 0
soma_msc = 0
soma_msg = 0
soma_pdc = 0
soma_pln = 0
soma_plv = 0
soma_prc = 0
soma_vet = 0
soma_fora = 0

dados_csv = []

for c in range(1, 6):
    url_proposicoes = "http://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-{}.json".format(ano)

    url_autores = "http://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/json/proposicoesAutores-{}.json".format(
        ano)
    response_proposicoes = requests.get(url_proposicoes)

    response_autores = requests.get(url_autores)

    if response_proposicoes.status_code == 200 and response_autores.status_code == 200:
        dados_proposicoes = response_proposicoes.json()["dados"]
        dados_autores = response_autores.json()["dados"]

    for autor in dados_autores:
        for proposicao in dados_proposicoes:
            if proposicao["id"] == autor["idProposicao"] and autor["ordemAssinatura"] == "1" and proposicao["siglaTipo"] in tipos_de_proposicoes:
                soma += 1
                dados_combinados = {
                    "id": proposicao["id"],
                    "siglaTipo": proposicao["siglaTipo"],
                    "numero": proposicao["numero"],
                    "ano": proposicao["ano"],
                    "nomeAutor": autor["nomeAutor"],
                    "siglaPartidoAutor": autor["siglaPartidoAutor"],
                    "siglaUFAutor": autor["siglaUFAutor"],
                    "dataultimoStatus": proposicao["ultimoStatus"]["data"],
                    "siglaOrgao": proposicao["ultimoStatus"]["siglaOrgao"],
                    "descricaoSituacao": proposicao["ultimoStatus"]["descricaoSituacao"]
                }
                if dados_combinados["siglaTipo"] == "PL":
                    soma_pl += 1
                if dados_combinados["siglaTipo"] == "PEC":
                    soma_pec += 1
                if dados_combinados["siglaTipo"] == "PLP":
                    soma_plp += 1
                if dados_combinados["siglaTipo"] == "MPV":
                    soma_mpv += 1
                if dados_combinados["siglaTipo"] == "MSC":
                    soma_msc += 1
                if dados_combinados["siglaTipo"] == "MSG":
                    soma_msg += 1
                if dados_combinados["siglaTipo"] == "PDC":
                    soma_pdc += 1
                if dados_combinados["siglaTipo"] == "PLN":
                    soma_pln += 1
                if dados_combinados["siglaTipo"] == "PLV":
                    soma_plv += 1
                if dados_combinados["siglaTipo"] == "PRC":
                    soma_prc += 1
                if dados_combinados["siglaTipo"] == "VET":
                    soma_vet += 1

                data_original = proposicao["ultimoStatus"]["data"]
                data_convertida = datetime.strptime(data_original, "%Y-%m-%dT%H:%M:%S")
                data_formatada = data_convertida.strftime("%d/%m/%Y")
                proposicao["ultimoStatus"]["data"] = data_formatada

                dados_csv.append([
                    dados_combinados["id"],
                    dados_combinados["nomeAutor"],
                    dados_combinados["siglaPartidoAutor"],
                    dados_combinados["siglaUFAutor"],
                    dados_combinados["siglaTipo"],
                    dados_combinados["numero"],
                    dados_combinados["ano"],
                    data_formatada,
                    dados_combinados["siglaOrgao"],
                ])

                print("Proposição {:,}".format(soma))
                print("id: {}\nParlamentar: {} {}/{}\nProjeto: {} {}/{}\nData Tramitação: {}\nLocalização Atual: {}\nDescrição: {}".format(
                        dados_combinados["id"], dados_combinados["nomeAutor"], dados_combinados["siglaPartidoAutor"],
                        dados_combinados["siglaUFAutor"], dados_combinados["siglaTipo"], dados_combinados["numero"],
                        dados_combinados["ano"], data_formatada, dados_combinados["siglaOrgao"], dados_combinados["descricaoSituacao"]))

            if proposicao["siglaTipo"] not in tipos_de_proposicoes:
                soma_fora += 1

    ano += 1

with open("dados_proposicoes.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Autor", "Partido", "UF", "Tipo", "Número", "Ano", "Data Tramitação", "Localização"])
    writer.writerows(dados_csv)

print("Quantidade total: {:,}".format(soma))
print("PL:{:,}\nPEC:{:,}\nPLP:{:,}\nMPV:{:,}\nMSC:{:,}\nMSG:{:,}\nPDC:{:,}\nPLN:{:,}\nPLV:{:,}\nPRC:{:,}\nVET:{:,}".format(soma_pl, soma_pec, soma_plp, soma_mpv, soma_msc, soma_msg, soma_pdc, soma_pln, soma_plv, soma_prc, soma_vet))
print("Quantidade de proposições fora da lista: {:,}".format(soma_fora))
