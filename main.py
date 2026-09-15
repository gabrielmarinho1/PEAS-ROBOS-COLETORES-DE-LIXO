import random

# Configurações do ambiente
TAMANHO = 20

QUANTIDADE_ORGANICO = 10
QUANTIDADE_RECICLAVEL = 5

POSICAO_INICIAL = (1, 1)
POSICAO_LIXEIRA = (20, 20)

# Mantém a mesma distribuição dos lixos em todas as execuções
SEMENTE = 42


def criar_ambiente():
    random.seed(SEMENTE)

    posicoes_disponiveis = []

    for linha in range(1, TAMANHO + 1):
        for coluna in range(1, TAMANHO + 1):

            posicao = (linha, coluna)

            if posicao != POSICAO_INICIAL and posicao != POSICAO_LIXEIRA:
                posicoes_disponiveis.append(posicao)

    quantidade_total = (
        QUANTIDADE_ORGANICO
        + QUANTIDADE_RECICLAVEL
    )

    posicoes_lixos = random.sample(
        posicoes_disponiveis,
        quantidade_total
    )

    lixos = {}

    # 10 lixos orgânicos
    for posicao in posicoes_lixos[:QUANTIDADE_ORGANICO]:
        lixos[posicao] = "O"

    # 5 lixos recicláveis
    for posicao in posicoes_lixos[QUANTIDADE_ORGANICO:]:
        lixos[posicao] = "R"

    return lixos


def mostrar_ambiente(lixos):

    print("\nMATRIZ 20 x 20\n")

    for linha in range(1, TAMANHO + 1):

        linha_visual = []

        for coluna in range(1, TAMANHO + 1):

            posicao = (linha, coluna)

            if posicao == POSICAO_INICIAL:
                simbolo = "A"

            elif posicao == POSICAO_LIXEIRA:
                simbolo = "X"

            elif posicao in lixos:
                simbolo = lixos[posicao]

            else:
                simbolo = "."

            linha_visual.append(simbolo)

        print(" ".join(linha_visual))


def mostrar_resumo(lixos):

    organicos = 0
    reciclaveis = 0

    for tipo in lixos.values():

        if tipo == "O":
            organicos += 1

        elif tipo == "R":
            reciclaveis += 1

    print("\nRESUMO DO AMBIENTE")
    print("Posição inicial do robô:", POSICAO_INICIAL)
    print("Posição da lixeira:", POSICAO_LIXEIRA)
    print("Lixos orgânicos:", organicos)
    print("Lixos recicláveis:", reciclaveis)
    print("Total de lixos:", len(lixos))


def main():

    lixos = criar_ambiente()

    mostrar_ambiente(lixos)

    mostrar_resumo(lixos)

    print("\nLEGENDA")
    print("A = Agente")
    print("X = Lixeira")
    print("O = Lixo orgânico")
    print("R = Lixo reciclável")
    print(". = Espaço vazio")


if __name__ == "__main__":
    main()