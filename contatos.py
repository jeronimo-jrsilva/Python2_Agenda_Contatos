# Jeronimo Silva
# OPERAÇÕES SOBRE OS CONTATOS
import re


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
    return bool(re.match(padrao, nome))


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
    return bool(re.match(padrao, email))


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
