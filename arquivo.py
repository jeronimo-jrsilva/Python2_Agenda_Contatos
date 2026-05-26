# Jeronimo Silva
# MANIPULAÇÃO DE ARQUIVOS CSV
import csv

# Arquivo onde constam os contatos, com cabeçalho, em formato csv
# Aprendi que arquivos de caminho costumam ter variáveis ALL CAPS relacionadas
ARQUIVO_AGENDA = "agenda.csv"


# Separa o arquivo de agenda em cabeçalho e contatos.
# Remove contatos vazios ou sem nome
# Organiza os contatos alfabeticamente.
def desmembrar() -> tuple:  # Retorna um tuple com o cabeçalho e os contatos limpos.
                            # Não entendi pq tupla, só aceitei.
    with open(ARQUIVO_AGENDA, "r", newline="", encoding="utf-8") as agenda:
        reader = csv.reader(agenda, delimiter=",")
        tudao = list(reader)
        cabecalho = tudao[0]
        contatos = tudao[1:]
        # Remove as linhas vazias:
        # se a linha estiver vazia, o 'if linha' retorna falso,
        # e ela não entra nos contatos limpos
        contatos_limpos = [linha for linha in contatos if linha[0] != ""]
        # contatos_limpos = [linha for linha in contatos if len(linha) > 0 and linha[0] != ""]
        contatos_limpos = sorted(contatos_limpos)

        return cabecalho, contatos_limpos


# Une cabeçalho e contatos para gerar um arquivo de agenda.
def reconstruir_agenda(campos, contatos) -> None:
    contatos = sorted(contatos)  # Organiza os contatos alfabeticamente.
    with open(ARQUIVO_AGENDA, "w", encoding="utf-8", newline="") as agenda:
        writer = csv.writer(agenda, delimiter=",")
        writer.writerow(campos)
        writer.writerows(contatos)


# Pesquisa um termo no CSV e retorna uma lista dos encontrados.
# O termo pode estar em qualquer campo.
def lista_achados(termo) -> list:
    termo = termo.lower()
    achados = []
    # List comprehension funcional (tendi p***a nenhuma)
    # achados = [linha for linha in reader if any(termo in coluna.lower() for coluna in linha)]
    cabecalho, contatos = desmembrar()
    for linha in contatos:
        for coluna in linha:
            if termo in coluna.lower():
                achados.append(linha)
                break
    return achados
