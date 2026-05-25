import csv
import re

# Arquivo onde constam os contatos, com cabeçalho, em formato csv
arquivo = 'agenda.csv'

# ---- Parâmetros de exibição ----

# Variáveis de formatação, inicializadas;
espaco = 22  # largura total da exibição na tela
espacinho = []  # largura de cada seção exibida
separador = ""  # Separa seções verticalmene
entradas = 0  # número total de contatos na agenda
limite = 20  # limite de contatos exibidos de uma vez
cor = True


# ---- Funções de formatação e exibição ----

# Separa o arquivo de agenda em cabeçalho e contatos.
# Remove contatos vazios ou sem nome
def desmembrar():
    with open(arquivo, 'r', newline='', encoding='utf-8') as agenda:
        reader = csv.reader(agenda, delimiter=',')
        tudao = list(reader)
        cabecalho = tudao[0]
        contatos = tudao[1:]
        # Remove as linhas vazias:
        # se a linha estiver vazia, o 'if linha' retorna falso,
        # e ela não entra nos contatos limpos
        contatos_limpos = [linha for linha in contatos if linha[0] != ""]
        # contatos_limpos = [linha for linha in contatos if len(linha) > 0 and linha[0] != ""]

        return cabecalho, contatos_limpos


# Une cabeçalho e contatos para gerar um arquivo de agenda.
def reconstruir_agenda(campos, contatos) -> None:
    global entradas
    entradas = len(contatos)
    contatos = sorted(contatos)  # Organiza os contatos alfabeticamente.
    with open(arquivo, 'w', encoding='utf-8', newline='') as agenda:
        writer = csv.writer(agenda, delimiter=',')
        writer.writerow(campos)
        writer.writerows(contatos)


# Serve para, na inicialização (ou sempre que recarregarmos
# o menu principal), recalcular o número de contatos na agenda.
def saneamento() -> None:
    global entradas
    campos, contatos = desmembrar()
    entradas = len(contatos)
    reconstruir_agenda(campos, contatos)


# Exibe o cabeçalho da agenda
def mostrar_cabecalho(cabecalho: list) -> None:
    print(f"{"":-^{espaco}}")
    contato_unico(cabecalho)
    print(f"{"":-^{espaco}}")


# Calcula os parâmetros de formatação
def inicializar_agenda() -> None:
    global espaco, espacinho, separador
    maiores = [0, 0, 0]
    campos, contatos = desmembrar()
    for linha in contatos:
        if len(linha) < 3:
            continue
        maiores = [max(len(linha[i]), maiores[i]) for i in range(3)]
    espaco = sum(maiores) + 2
    espacinho = maiores
    separador = f"{'':-^{espaco}}"


# ---- Manipulação de arquivos externos ----

# Insere contato na agenda, obedecendo regras de validação
def inserir_na_agenda() -> bool:
    # Se o contato for inserido com sucesso,
    # retorna verdadeiro, caso contrário, retorna falso.
    campos, contatos = desmembrar()

    nome = input("Digite nome: ")
    if not validar_nome(nome):
        return False
    nome = nome.title()
    email = input("Digite email: ")
    if not validar_email(email):
        return False
    telefone = input("Digite telefone: ")
    if not validar_telefone(telefone):
        return False

    # Caso o usuário deixe todos os campos vazios,
    # retorna verdadeiro, mas não adiciona o contato
    # ao arquivo externo, e avisa o usuário.
    if not nome and not email and not telefone:
        print(f"\n{'Inserção de contato cancelada!':^{espaco}}\n")
        return True
    # Só formata o telefone se for um número válido
    if telefone:
        telefone = formatar_telefone(telefone)

    novo_contato = [nome, email, telefone]
    contatos.append(novo_contato)
    # Reconstrói a agenda com o contato novo. Lembre-se que
    # a reconstrução também ordena alfabeticamente.
    reconstruir_agenda(campos, contatos)
    print(f"\n{'Contato adicionado com sucesso!':^{espaco}}\n")
    contato_unico(novo_contato)
    return True


def validar_nome(nome) -> bool:
    if not nome:
        return True
    # Regex (regular expressions) são uma das coisas mais impressionantes (na minha opinião).
    # É uma forma de procurar texto usando texto, e é mágico.
    # Entendo um pouco, mas essa expressão eu construío com a ajuda do Gemini.

    # r-strings são usadas quando precisamos que a contrabarra \ não seja
    # considerada um caracter de verdade, ao invés de 'character escape'

    # Esse padrão diz que o nome deve começar (^) com qualquer caracter de A a z,
    # maiúsculo ou minúsculo, com qualquer acentuação, e ser seguido de um ou
    # mais caracteres do mesmo grupo ou espaço até o final ($). Caso um caracter
    # não obedeça essas regras, o nome será invalidado.
    padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$"

    # re.match() retorna um objeto se o nome inteiro casar com o padrão,
    # senão retorna None. O bool() transforma o objeto em True e o None em False.

    # O "and name" serve para considerar apenas os nomes não vazios.
    if not bool(re.match(padrao, nome)):
        print(f"{"\nNome inválido! (para cancelar, deixe todos os campos em branco)":^{espaco}}\n")
        return False

    # Caso o nome seja vazio, a função retorna True,
    # o que permite cancelar a inserção na agenda
    return True


def validar_email(email) -> bool:
    if not email:
        return True

    # Expressão regular padrão para e-mails comuns. Aqui temos:
    # letras minúsculas, letras maiúsculas, números e outros
    # símbolos (um ou mais desses), seguidos da arroba, seguida
    # de letras ou números ou ponto ou traço, seguida de ponto,
    # seguida de pelo menos duas letras. As regras não permitem
    # caracteres acentuados.
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # re.match() retorna um objeto se o nome inteiro casar com o padrão,
    # senão retorna None. O bool() transforma o objeto em True e o None em False.

    # O "and email" serve para considerar apenas os nomes não vazios.
    if not bool(re.match(padrao, email)):
        print(f"{"\nEmail inválido! (para cancelar, deixe todos os campos em branco)":^{espaco}}\n")
        return False
    # Caso o email seja vazio, a função retorna True,
    # o que permite cancelar a inserção na agenda
    return True


def validar_telefone(telefone) -> bool:
    if not telefone:
        return True
    numeros = ""  # string vazia
    # Passa por cada caractere do número que o usuário digitou.
    # Se for um número, adiciona na nossa variável 'numeros'
    for caractere in telefone:  # para cada caracter na string fornecida
        if caractere.isdigit():  # caso o caracter seja um dígito (número)
            numeros += caractere  # adiciona ao final da minha string de números
    if len(numeros) != 11:  # se não tem 11 dígitos (e nem é vazio), rejeita.
        print(f"{"\nTelefone inválido inválido! (para cancelar, deixe todos os campos em branco)":^{espaco}}\n")
        return False
    # se tem 11 dígitos OU é vazio, retorna verdadeiro.
    return True


# Deveria estar na parte da formatação, mas preferi deixar aqui.
# Formata os números telefônicos digitados.
# Essa função é chamada após validar o telefone, então
# sabemos que ele tem 11 dígitos.
def formatar_telefone(telefone_bruto) -> str:
    numeros = ""
    for caractere in telefone_bruto:
        if caractere.isdigit():
            numeros += caractere
    # Formatação do tipo (XX) XXXXX-XXXX
    telefone_formatado = f"({numeros[0:2]}) {numeros[2:7]}-{numeros[7:]}"
    return telefone_formatado


# OBSOLETA
# def validar_contato(contato) -> bool:
#     if len(contato) == 3:
#         if validar_nome(contato[0]) and validar_email(contato[1]) and validar_telefone(contato[2]):
#             return True
#     return False

# Remove contatos do arquivo externo.
def remover_da_agenda(eliminar) -> None:
    campos, contatos = desmembrar()
    # Os contatos restantes são construídos a partir da lista original,
    # removendo aquele cujo nome (c[0]) é igual ao que o usuário digitou (eliminar).
    contatos_restantes = [c for c in contatos if c[0].lower() != eliminar.lower()]
    # Se depois desse processo a agenda continua do mesmo tamanho, nenum contato foi removido.
    if len(contatos_restantes) == len(contatos):
        print(f"\n{'Contato não encontrado':^{espaco}}\n")
    # Se ela muda de tamanho, o contato foi removido.
    # No caso de contatos duplicados, AMBOS SÃO REMOVIDOS.
    # (uma das limitações da minha abordagem).
    else:
        reconstruir_agenda(campos, contatos_restantes)
        print(f"\n{"Contato removido:":^{espaco}}\n")

        print(f"{eliminar.title():^{espaco}}")


# Mostra a agenda inteira.
def mostrar_agenda() -> None:
    apresentar_secao("Visualizar agenda")
    campos, contatos = desmembrar()
    mostrar_cabecalho(campos)
    mostrar_lista(contatos)
    print(separador)


# Mostra só um contatinho.
def contato_unico(linha: list[str]) -> None:
    global espaco, espacinho, separador
    contato = f"{linha[0]:^{espacinho[0]}}|{linha[1]:^{espacinho[1]}}|{linha[2]:^{espacinho[2]}}"
    print(contato)


# Mostra contatos que obedecem a um critério de busca
def mostrar_lista(lista) -> None:
    global limite
    # if len(lista) == 0:
    if not lista:
        print(f"\n{'Nenhum contato encontrado':^{espaco}}")
    else:
        print(f"\n{'Contato(s) encontrado(s):':^{espaco}}\n")

        # O range vai de 0 até o tamanho da lista, pulando
        # conforme o 'limite' definido lá no início.
        for i in range(0, len(lista), limite):
            # Pega o pedaço exato da lista usando o limite atual
            bloco = lista[i: i + limite]

            # Exibe os contatos deste bloco específico
            for linha in bloco:
                contato_unico(linha)

            # Checando se ainda há próximos itens
            if i + limite < len(lista):
                # Ajustado '{i + 1}' para a contagem humana começar do 1 (ex: Exibindo 1 a 20)
                input(f"\nExibindo {i + 1} a {i + len(bloco)} de {len(lista)}. Pressione ENTER para ver os próximos\n")
                # Isso é outra coisa que aprendi nesse trabalho: um input "vazio", não atribuído a uma variável,
                # pode ser utilizado como uma pausa com continuação manual (enter). Irado!


# Pesquisa um termo no CSV e retorna uma lista dos encontrados.
# O termo pode estar em qualquer campo.
def lista_achados() -> list:
    termo = input("Digite o termo a pesquisar: ").lower()
    achados = []
    with open(arquivo, 'r', encoding='utf-8') as agenda:
        reader = csv.reader(agenda, delimiter=',')
        # List comprehension funcional (tendi p***a nenhuma)
        # achados = [linha for linha in reader if any(termo in coluna.lower() for coluna in linha)]
        for linha in reader:
            for coluna in linha:
                if termo in coluna.lower():
                    achados.append(linha)
                    break
    return achados


def apresentar_secao(secao) -> None:
    # Adiciona espaços antes e depois do título da seção, por opção estética.
    secao = " " + secao + " "

    # Linha separadora, e linha de título (centralizada).
    linha_sep = f'{"":-^{espaco}}'
    linha_texto = f'{secao:=^{espaco}}'

    match cor:
        case True:
            # Cores passadas diretamente para a função externa
            ciano = (0, 255, 255)
            magenta = (255, 0, 255)

            # APENAS a linha do texto recebe a função colorir
            print(f"\n{colorir(linha_sep)}\n{colorir(linha_texto, ciano, magenta)}\n{colorir(linha_sep)}\n")

        case False:
            print(f"\n{linha_sep}\n{linha_texto}\n{linha_sep}\n")


def colorir(texto, c1=(0, 255, 255), c2=(255, 0, 255)) -> str:
    """Aplica um degradê True Color ANSI entre duas cores RGB."""
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


# Seção de busca, chama funções mais específicas para fazer o trabalho pesado.
def busca_contato() -> None:
    apresentar_secao("Buscar contato")
    encontrados = lista_achados()
    mostrar_lista(encontrados)


# Seção correspondente.
def criar_contato() -> None:
    apresentar_secao("Criar contato")
    repete = True
    while repete:
        # A função inserir_na_agenda() retorna True se teve sucesso e False se não inseriu.
        # Quero que o loop while repita só quando a função falhar.
        # Ou seja, quero que 'repete' seja verdadeiro quando a função retornar False
        repete = not inserir_na_agenda()


# Ditto.
def remover_contato() -> None:
    apresentar_secao("Remover contato")
    encontrados = lista_achados()
    mostrar_lista(encontrados)
    eliminar = input("Digite EXATAMENTE o nome do contato que você quer remover: ")
    remover_da_agenda(eliminar)


# Mermo igual.
def atualizar_contato() -> None:
    apresentar_secao("Atualizar contato")
    encontrados = lista_achados()
    mostrar_lista(encontrados)
    print("")

    print("Digite EXATAMENTE o nome do contato que você quer alterar: ")
    alterar = input()
    if inserir_na_agenda():
        remover_da_agenda(alterar)


# def sobre():
#     print('''
# Erros conhecidos:
#
#     1 - A agenda permite contatos e campos duplicados.
#         Em CVS, o tratamento de entradas duplicadas exige
#         mais esforço que quando trabalhamos com bancos de
#         dados (SQL), e eu tava com preguiça.
#
#     2 - No caso de contatos duplicados, apagando um
#         apagam-se todos.
#
#     3 - A agenda é destruída e reconstruída o tempo
#         todo, ao invés de se fazer alterações pontuais.
#         Achei mais direto fazer assim, mas entendo que não
#         seja eficiente. Ainda assim, preferi experimentar
#         dessa forma.
#
#     4 - A agenda funciona para números de telefonia
#         móvel brasileiros sem DDI. Números fixos (10
#         algarismos com DDD) ou números internacionais
#         (iniciados por '+', e com quantidade de algarismos
#         variando conforme o país) são rejeitados pelo filtro
#         regex.
#
# Obrigado!
#     ''')
#     c1 = (0, 255, 255)
#     c2 = (255, 0, 255)
#     c3 = (255, 255, 0)
#     aluno = f"{'Jeronimo Silva':^{espaco}}"
#     telefone = f"{'(85) 9 9129 2744':^{espaco}}"
#     email = f"{'shaolin.jr@gmail.com':^{espaco}}"
#     github = f"{'https://github.com/jeronimo-jrsilva':^{espaco}}"
#     professor = f"{'Me. Nator Júnior':^{espaco}}"
#     disciplina = f"{'Lógica de programação':^{espaco}}"
#     print(f"\n\n{"Desenvolvido por:":<{espaco}}\n\n"
#           f"{colorir(aluno, c1, c2):^{espaco}}\n"
#           f"{colorir(telefone, c2, c3):^{espaco}}\n"
#           f"{colorir(email, c3, c1):^{espaco}}\n"
#           f"{github:^{espaco}}\n\n"
#           f"{"Disciplina:":<{espaco}}\n\n"
#           f"{colorir(disciplina, c1, c3):^{espaco}}\n\n"
#           f"{"Professor:":<{espaco}}\n\n"
#           f"{colorir(professor, c3, c2):^{espaco}}\n\n"
#           )

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

        "2 - No caso de contatos duplicados, apagando um\n"
        "    apagam-se todos.",

        "3 - A agenda é destruída e reconstruída o tempo\n"
        "    todo, ao invés de se fazer alterações pontuais.\n"
        "    Achei mais direto fazer assim, mas entendo que não\n"
        "    seja eficiente. Ainda assim, preferi experimentar\n"
        "    dessa forma.",

        "4 - A agenda funciona para números de telefonia\n"
        "    móvel brasileiros sem DDI. Números fixos (10\n"
        "    algarismos com DDD) ou números internacionais\n"
        "    (iniciados por '+', e com quantidade de algarismos\n"
        "    variando conforme o país) são rejeitados pelo filtro\n"
        "    regex."
    ]

    # Passa pelos erros exibindo um por um
    for i, erro in enumerate(erros, start=1):
        print(erro)
        print(separador)
        # Se não for o último erro, pede ENTER para o próximo. Se for o último, avança para os créditos.
        if i < len(erros):
            input("Pressione ENTER para ler o próximo erro... ")
            print("\n")
        else:
            input("Pressione ENTER para ver os créditos do sistema... ")
            print("\n")

    # --- Seção de Créditos ---
    c1 = (0, 255, 255)  # Ciano
    c2 = (255, 0, 255)  # Magenta
    c3 = (255, 255, 0)  # Amarelo

    # Centralizando os textos PUROS primeiro
    aluno = f"{'Jeronimo Silva':^{espaco}}"
    telefone = f"{'(85) 9 9129 2744':^{espaco}}"
    email = f"{'shaolin.jr@gmail.com':^{espaco}}"
    github = f"{'https://github.com/jeronimo-jrsilva':^{espaco}}"
    professor = f"{'Msc. Nator Júnior Carvalho da Costa':^{espaco}}"
    disciplina = f"{'Lógica de programação':^{espaco}}"

    # Colorindo geral:
    if cor:
        aluno = f"{colorir(aluno, c1, c2)}"
        telefone = f"{colorir(telefone, c2, c3)}"
        email = f"{colorir(email, c3, c1)}"
        disciplina = f"{colorir(disciplina, c1, c3)}"
        professor = f"{colorir(professor, c3, c2)}"

    # Impressão limpa (visto que as variáveis já estão centralizadas e coloridas)
    print(f"Desenvolvido por:\n"
          # f"{colorir(aluno, c1, c2)}\n"
          # f"{colorir(telefone, c2, c3)}\n"
          # f"{colorir(email, c3, c1)}\n"
          f"{aluno}\n"
          f"{telefone}\n"
          f"{email}\n"
          f"{github}\n\n"
          f"Disciplina:\n"
          f"{disciplina}\n\n"
          # f"{colorir(disciplina, c1, c3)}\n\n"
          f"Professor:\n"
          f"{professor}\n\n"
          # f"{colorir(professor, c3, c2)}\n\n"
          f"Obrigado!\n"
          )


# Cardápio em francês
def menu() -> None:
    saneamento()
    inicializar_agenda()
    apresentar_secao("Menu")
    msg = f"Número de contatos: {entradas}"
    print(f"{msg:>{espaco}}\n")
    print(f"{"1 - Mostrar agenda":<{espaco}}\n"
          f"{"2 - Buscar contato":<{espaco}}\n"
          f"{"3 - Adicionar contato":<{espaco}}\n"
          f"{"4 - Atualizar contato":<{espaco}}\n"
          f"{"5 - Remover contato":<{espaco}}\n\n"
          f"{"6 - Sobre":<{espaco}}\n\n"
          f"{"c - Alterar esquema de cores":>{espaco}}\n"
          f"{"Outra opção - Sair":>{espaco}}")

# Esposa do pain (baianês).
def main() -> None:
    global cor
    while True:
        menu()
        print("")
        print(f"{"Insira uma opção: ":^{espaco}}")
        opcao = input()
        match opcao:
            case "1":
                mostrar_agenda()
            case "2":
                busca_contato()
            case "3":
                criar_contato()
            case "4":
                atualizar_contato()
            case "5":
                remover_contato()
            case "6":
                sobre()
            case "c":
                cor = not cor
                print("\nEsquema de cores alterado.\n")
            case _:
                apresentar_secao("Agenda encerrada")
                break
        input("\n[Pressione Enter para voltar ao menu]")