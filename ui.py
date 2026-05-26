# Jeronimo Silva
# INTERFACE

import arquivo  # manipulação de arquivos CSV
import contatos as logic  # operações sobre os contatos

# import os
import subprocess
import sys

# Observação:
# Tentei deixar a tipagem explícita, ao menos em relação
# às funções (retorno). Pensei isso no último dia, e 
# alterar também os parâmetros e as variáveis daria trabalho
#  demais e poderia introduzir erros (coisa que não quero 
# horas antes da apresentação)

# ---- Parâmetros de exibição (Herança do jero_aux) ----

# Variáveis de formatação, inicializadas;
espacinho = [15, 15, 10]  # largura de cada seção exibida
espaco = sum(espacinho) + 2  # largura total da exibição na tela
separador = ""  # Separa seções verticalmene
entradas = 0  # número total de contatos na agenda
limite = 20  # limite de contatos exibidos de uma vez
cor = True

# Interruptor que alterna entre True e False, colorindo ou não
# certas partes da interface.
def muda_cor() -> None:
    global cor
    cor = not cor


def colorir(texto, c1=(0, 255, 255), c2=(255, 0, 255)) -> str:
    # Aplica um degradê True Color ANSI entre duas cores RGB.

    # Não entendi, só aceitei. Tem a ver com RBG, e com uma taxa
    # de incremento, aplicada a cada caracter.
    res = ""
    n = len(texto)

    # Evita divisão por zero caso a string seja vazia ou tenha 1 caractere
    if n <= 1:
        # Será que um dia consigo entender isso aqui DE VERDADE?!?!
        return f"\033[38;2;{c1[0]};{c1[1]};{c1[2]}m{texto}\033[0m"

    # Sei que o enumerate itera tanto no índice quanto no valor,
    # mas o que ele faz aqui é um mistério.
    for i, char in enumerate(texto):
        ratio = (i / (n - 1)) ** 1.3
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        res += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
    return res


def apresentar_secao(secao) -> None:
    # Adiciona espaços antes e depois do título da seção, por opção estética.
    secao = " " + secao + " "

    # Linha separadora, e linha de título (centralizada).
    linha_sep = f"{'':-^{espaco}}"
    linha_texto = f"{secao:=^{espaco}}"

    if cor:
        # Cores passadas diretamente para a função externa
        ciano = (0, 255, 255)
        magenta = (255, 0, 255)

        # APENAS a linha do texto recebe a função colorir
        print(
            f"\n{colorir(linha_sep)}\n{colorir(linha_texto, ciano, magenta)}\n{colorir(linha_sep)}\n"
        )
    else:
        print(f"\n{linha_sep}\n{linha_texto}\n{linha_sep}\n")


# Serve para, na inicialização (ou sempre que recarregarmos
# o menu principal), recalcular o número de contatos na agenda.
# Também calcula os parâmetros de formatação e organiza os contatos.
def inicializar_agenda() -> None:
    global espaco, espacinho, separador, entradas
    campos, lista_contatos = arquivo.desmembrar()
    arquivo.reconstruir_agenda(campos, lista_contatos)
    # Quantidade de contatos na agenda:
    entradas = len(lista_contatos)

    # Se não houver contatos, usa valores padrão
    if not lista_contatos:
        espacinho = [15, 15, 10]
        espaco = sum(espacinho) + 2

    else:
        maiores = [len(c) for c in campos]
        for linha in lista_contatos:
            if len(linha) < 3:
                continue
            maiores = [max(len(linha[i]), maiores[i]) for i in range(3)]
        espacinho = maiores
        espaco = sum(maiores) + 2
    separador = f"{'':-^{espaco}}"


# Mostra só um contatinho. Cada campo é centralizado
# na coluna correspondente.
def contato_unico(linha: list[str]) -> None:
    contato = f"{linha[0]:^{espacinho[0]}}|{linha[1]:^{espacinho[1]}}|{linha[2]:^{espacinho[2]}}"
    print(contato)


# Mostra contatos que obedecem a um critério de busca
def mostrar_lista(lista) -> None:
    continuar = ""
    if not lista:
        print(f"\n{'Nenhum contato encontrado':^{espaco}}")
    else:
        # O range vai de 0 até o tamanho da lista, pulando
        # conforme o 'limite' definido lá no início.
        for i in range(0, len(lista), limite):
            # Pega o pedaço exato da lista usando o limite atual
            bloco = lista[i : i + limite]

            # Exibe os contatos deste bloco específico
            limpar_tela()
            print(f"\n{'Contato(s) encontrado(s):':^{espaco}}")
            print(separador)
            for linha in bloco:
                contato_unico(linha)

            # Checando se ainda há próximos itens
            if i + limite < len(lista):
                # Ajustado '{i + 1}' para a contagem humana começar do 1 (ex: Exibindo 1 a 20)
                continuar = input(
                    f"\n\nExibindo {i + 1} a {i + len(bloco)} de {len(lista)}\n"
                    f"Pressione ENTER para ver os próximos\n"
                    f"ou o 'c' seguido de ENTER para cancelar\n\n"
                )
                if continuar == "c":
                    break
                # Isso é outra coisa que aprendi nesse trabalho: um input "vazio", não atribuído a uma variável,
                # pode ser utilizado como uma pausa com continuação manual (enter). Irado!
        print(separador)


# Mostra a agenda inteira.
def mostrar_agenda() -> None:
    apresentar_secao("Visualizar agenda")
    campos, lista_contatos = arquivo.desmembrar()
    # Exibe o cabeçalho da agenda
    print(f"{'':-^{espaco}}")
    contato_unico(campos)
    print(f"{'':-^{espaco}}")
    mostrar_lista(lista_contatos)


# Insere contato na agenda, obedecendo regras de validação
# Pode retornar 3 tipos diferentes:
# CANCEL (string) - se o usuário cancelar a operação
#   (deixando todos os campos em branco)
# None - se o contato não for válido (alguma das funções de validação retornar False)
# list - se o contato for válido (organizadinho como no resto da agenda)
def criar_contato() -> str | None | list:
    nome = input("Digite nome: ")
    if not logic.validar_nome(nome):
        print(
            f"{'\nNome inválido! (para cancelar, deixe todos os campos em branco)':^{espaco}}\n"
        )
        return None

    email = input("Digite email: ")
    if not logic.validar_email(email):
        print(
            f"{'\nEmail inválido! (para cancelar, deixe todos os campos em branco)':^{espaco}}\n"
        )
        return None

    telefone = input("Digite telefone: ")
    if not logic.validar_telefone(telefone):
        print(
            f"{'\nTelefone inválido! (para cancelar, deixe todos os campos em branco)':^{espaco}}\n"
        )
        return None

    # Caso o usuário deixe todos os campos vazios,
    # retorna verdadeiro, mas não adiciona o contato
    # ao arquivo externo, e avisa o usuário.
    if not nome and not email and not telefone:
        return "CANCEL"

    # Só formata o telefone se for um número válido
    return [nome.title(), email, logic.formatar_telefone(telefone) if telefone else ""]


# Mostra (alguns dos) bugs conhecidos, e os créditos.
def sobre() -> None:
    global separador
    apresentar_secao("Erros Conhecidos")

    # Lista contendo os erros conhecidos:
    erros = [
        "1 - A agenda permite contatos e campos duplicados.\n"
        "    Em CSV, o tratamento de entradas duplicadas exige\n"
        "    mais esforço que quando trabalhamos com bancos de\n"
        "    dados (SQL), e eu tava com preguiça.",
        "2 - No caso de contatos duplicados, apagando um\n    apagam-se todos.",
        "3 - A agenda é destruída e reconstruída o tempo\n"
        "    todo, ao invés de se fazer alterações pontuais.\n"
        "    Achei mais direto fazer assim, mas entendo que não\n"
        "    seja eficiente. Ainda assim, preferi experimentar\n"
        "    dessa forma.",
        "4 - A agenda comporta telefones com um total de 11 dígitos,\n"
        "    nada mais, nada menos. Portanto, comporta números da\n"
        "    telefonia móvel brasileira, mas não telefones fixos,\n"
        "    números estrangeiros, ou números emergenciais ou \n"
        "    especiais.",
        "5 - A agenda também não permite números no campo nome,\n"
        "    inviabilizando contatos tipo:\n\n"
        "    Namorada\n"
        "    Namorada2\n"
        "    Namorada3\n"
        "    ...",
    ]

    # Passa pelos erros exibindo um por um
    for i, erro in enumerate(erros, start=1):
        limpar_tela()
        apresentar_secao("Erros conhecidos")
        print(erro)
        print("")
        print(separador)
        # Se não for o último erro, pede ENTER para o próximo. Se for o último, avança para os créditos.
        if i < len(erros):
            print("")
            input("Pressione ENTER para ler o próximo erro... ")
            print("")
        else:
            print("")
            input("Pressione ENTER para ver os créditos do sistema... ")
            print("")

    # --- Seção de Créditos ---
    c1 = (0, 255, 255)  # Ciano
    c2 = (255, 0, 255)  # Magenta
    c3 = (255, 255, 0)  # Amarelo

    # Centralizando os textos PUROS primeiro
    aluno = f"{'Jeronimo Silva':^{espaco}}"
    telefone = f"{'(85) 9 9129 2744':^{espaco}}"
    email = f"{'shaolin.jr@gmail.com':^{espaco}}"
    github = f"{'https://github.com/jeronimo-jrsilva':^{espaco}}"
    professor = f"{'M.Sc. Nator Júnior Carvalho da Costa':^{espaco}}"
    disciplina = f"{'Lógica de programação':^{espaco}}"

    # Colorindo geral:
    if cor:
        aluno = f"{colorir(aluno, c1, c2)}"
        telefone = f"{colorir(telefone, c2, c3)}"
        email = f"{colorir(email, c3, c1)}"
        disciplina = f"{colorir(disciplina, c1, c3)}"
        professor = f"{colorir(professor, c3, c2)}"

    # Impressão limpa (visto que as variáveis já estão centralizadas e coloridas)
    limpar_tela()
    apresentar_secao("Créditos")
    print(
        f"Desenvolvido por:\n"
        f"{aluno}\n"
        f"{telefone}\n"
        f"{email}\n"
        f"{github}\n\n"
        f"Disciplina:\n"
        f"{disciplina}\n\n"
        f"Professor:\n"
        f"{professor}\n\n"
        f"Obrigado!\n"
    )

def limpar_tela() -> None:
    # Limpa a tela com o comando 'clear' para macOS/Linux, 'cls' para Windows
    # Poderia usar 'os.system('cls')' mas não funcionaria no Linux (parte do
    # programa foi feita no Linux). Além disso, o Pyright (type checker do Zed)
    # reclama sobre 'os.system' mas funciona corretamente.
    command = 'clear' if sys.platform != 'win32' else 'cls'
    subprocess.run(command, shell=True)


# Cardápio em francês
def menu() -> None:
    limpar_tela()
    inicializar_agenda()
    apresentar_secao("Menu")
    msg = f"Número de contatos: {entradas}"
    print(f"{msg:>{espaco}}\n")
    print(
        f"{'1 - Mostrar agenda':<{espaco}}\n"
        f"{'2 - Buscar contato':<{espaco}}\n"
        f"{'3 - Adicionar contato':<{espaco}}\n"
        f"{'4 - Atualizar contato':<{espaco}}\n"
        f"{'5 - Remover contato':<{espaco}}\n\n"
        f"{'6 - Sobre':<{espaco}}\n\n"
        f"{'c - Alterar esquema de cores':>{espaco}}\n"
        f"{'Outra opção - Sair':>{espaco}}"
    )


# Esposa do pain (baianês).
def main() -> None:
    """Loop principal do programa (Manteve-se a lógica original de match-case)."""
    while True:
        menu()
        print("")
        print(f"{'Insira uma opção: ':^{espaco}}")
        opcao = input()
        match opcao:
            case "1": # Mostrar agenda
                limpar_tela()
                mostrar_agenda()
            case "2": # Buscar contato
                limpar_tela()
                # Seção de busca, chama funções mais específicas para fazer o trabalho pesado.
                apresentar_secao("Buscar contato")
                termo = input("Digite o termo a pesquisar: ")
                mostrar_lista(arquivo.lista_achados(termo))
            case "3": # Criar contato
                limpar_tela()
                # Seção correspondente.
                apresentar_secao("Criar contato")
                repete = True
                while repete:
                    dados = criar_contato()
                    if dados == "CANCEL":
                        print(f"\n{'Inserção de contato cancelada!':^{espaco}}\n")
                        repete = False
                    elif dados:
                        campos, contatos = arquivo.desmembrar()
                        contatos.append(dados)
                        # Reconstrói a agenda com o contato novo. Lembre-se que
                        # a reconstrução também ordena alfabeticamente.
                        arquivo.reconstruir_agenda(campos, contatos)
                        print(f"\n{'Contato adicionado com sucesso!':^{espaco}}\n")
                        # contato_unico(dados)
                        repete = False
                    else:
                        repete = True  # Erro de validação, repete
            case "4": # Atualizar contato
                limpar_tela()
                # Mermo igual.
                apresentar_secao("Atualizar contato")
                termo = input("Digite o nome para buscar e atualizar: ")
                achados = arquivo.lista_achados(termo)
                mostrar_lista(achados)
                print("")
                print("Digite EXATAMENTE o nome do contato que você quer alterar: ")
                nome_exato = input()
                novos_dados = criar_contato()
                if novos_dados and novos_dados != "CANCEL":
                    campos, contatos = arquivo.desmembrar()
                    # Os contatos restantes são construídos a partir da lista original,
                    # removendo aquele cujo nome (c[0]) é igual ao que o usuário digitou.
                    contatos = [
                        c for c in contatos if c[0].lower() != nome_exato.lower()
                    ]
                    contatos.append(novos_dados)
                    arquivo.reconstruir_agenda(campos, contatos)
            case "5": # Remover contato
                limpar_tela()
                # Ditto.
                apresentar_secao("Remover contato")
                termo = input("Digite o termo para buscar e remover: ")
                mostrar_lista(arquivo.lista_achados(termo))
                eliminar = input(
                    "Digite EXATAMENTE o nome do contato que você quer remover: "
                )
                campos, contatos = arquivo.desmembrar()
                # Se depois desse processo a agenda continua do mesmo tamanho, nenum contato foi removido.
                novos_contatos = [
                    c for c in contatos if c[0].lower() != eliminar.lower()
                ]
                if len(novos_contatos) == len(contatos):
                    print(f"\n{'Contato não encontrado':^{espaco}}\n")
                else:
                    arquivo.reconstruir_agenda(campos, novos_contatos)
                    print(f"\n{'Contato removido:':^{espaco}}\n")
                    print(f"{eliminar.title():^{espaco}}")
            case "6": # Sobre
                limpar_tela()
                # Mostra (alguns dos) bugs conhecidos, e os créditos.
                sobre()
            case "c":
                muda_cor()
                print("\nEsquema de cores alterado.\n")
            case _:
                limpar_tela()
                apresentar_secao("Agenda encerrada")
                break
        input("\n[Pressione Enter para voltar ao menu]")
