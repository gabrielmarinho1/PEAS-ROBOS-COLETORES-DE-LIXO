import random
import time

# Configurações do ambiente
TAMANHO = 20

QUANTIDADE_ORGANICO = 10
QUANTIDADE_RECICLAVEL = 5

POSICAO_INICIAL = (1, 1)
POSICAO_LIXEIRA = (20, 20)

# Mantém a mesma distribuição dos lixos em todas as execuções
SEMENTE = 42

VALOR_ORGANICO = 1
VALOR_RECICLAVEL = 5


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

    for posicao in posicoes_lixos[:QUANTIDADE_ORGANICO]:
        lixos[posicao] = "O"

    for posicao in posicoes_lixos[QUANTIDADE_ORGANICO:]:
        lixos[posicao] = "R"

    return lixos


def mostrar_ambiente(lixos, posicao_agente=None):

    print("\nMATRIZ 20 x 20\n")

    for linha in range(1, TAMANHO + 1):

        linha_visual = []

        for coluna in range(1, TAMANHO + 1):

            posicao = (linha, coluna)

            if posicao_agente is not None and posicao == posicao_agente:
                simbolo = "A"

            elif posicao == POSICAO_INICIAL and posicao_agente is None:
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

#Agente Simples

def obter_vizinhos(posicao):
    linha, coluna = posicao
    vizinhos = []

    for delta_linha in (-1, 0, 1):
        for delta_coluna in (-1, 0, 1):

            if delta_linha == 0 and delta_coluna == 0:
                continue

            nova_linha = linha + delta_linha
            nova_coluna = coluna + delta_coluna

            if 1 <= nova_linha <= TAMANHO and 1 <= nova_coluna <= TAMANHO:
                vizinhos.append((nova_linha, nova_coluna))

    return vizinhos


def passo_em_direcao(origem, destino):
    """Retorna a próxima posição ao mover 1 passo (linha/coluna) na
    direção do destino (Mover Esquerda/Direita/Cima/Baixo)."""

    linha_origem, coluna_origem = origem
    linha_destino, coluna_destino = destino

    nova_linha = linha_origem
    nova_coluna = coluna_origem

    if linha_destino > linha_origem:
        nova_linha += 1
    elif linha_destino < linha_origem:
        nova_linha -= 1
    elif coluna_destino > coluna_origem:
        nova_coluna += 1
    elif coluna_destino < coluna_origem:
        nova_coluna -= 1

    return (nova_linha, nova_coluna)


def escolher_vizinho_com_lixo(posicao, lixos):
    """Percebe os 8 vizinhos e retorna o vizinho com lixo, priorizando
    reciclável (R) sobre orgânico (O). Retorna None se nenhum vizinho
    tiver lixo."""

    vizinhos = obter_vizinhos(posicao)

    vizinhos_com_reciclavel = [v for v in vizinhos if lixos.get(v) == "R"]
    if vizinhos_com_reciclavel:
        return random.choice(vizinhos_com_reciclavel)

    vizinhos_com_organico = [v for v in vizinhos if lixos.get(v) == "O"]
    if vizinhos_com_organico:
        return random.choice(vizinhos_com_organico)

    return None


def agente_reativo_simples(lixos_iniciais, limite_passos=20000, verboso=False):
    """Executa o Agente Reativo Simples até coletar e entregar todos os
    lixos (ou até atingir o limite de passos, como segurança)."""

    lixos = dict(lixos_iniciais)

    posicao_agente = POSICAO_INICIAL
    carga = None  

    pontuacao = 0
    lixos_coletados = 0
    passos = 0

    tempo_inicio = time.perf_counter()

    while lixos or carga is not None:

        if passos >= limite_passos:
            print("Limite de passos atingido. Encerrando execução.")
            break
        if posicao_agente in lixos and carga is None:
            carga = lixos.pop(posicao_agente)

            if verboso:
                print(f"Passo {passos}: Pegar Lixo ({carga}) em {posicao_agente}")

        elif carga is not None and posicao_agente == POSICAO_LIXEIRA:
            valor = VALOR_RECICLAVEL if carga == "R" else VALOR_ORGANICO
            pontuacao += valor
            lixos_coletados += 1

            if verboso:
                print(f"Passo {passos}: Soltar Lixo ({carga}) em {posicao_agente} "
                      f"(+{valor} pontos)")

            carga = None

        elif carga is None:
            vizinho_alvo = escolher_vizinho_com_lixo(posicao_agente, lixos)

            if vizinho_alvo is not None:
                posicao_agente = passo_em_direcao(posicao_agente, vizinho_alvo)
                passos += 1

                if verboso:
                    print(f"Passo {passos}: Mover em direção ao lixo -> {posicao_agente}")

            else:
                vizinhos_validos = obter_vizinhos(posicao_agente)
                posicao_agente = random.choice(vizinhos_validos)
                passos += 1

                if verboso:
                    print(f"Passo {passos}: Mover aleatoriamente (exploração) -> {posicao_agente}")
        else:
            posicao_agente = passo_em_direcao(posicao_agente, POSICAO_LIXEIRA)
            passos += 1

            if verboso:
                print(f"Passo {passos}: Mover em direção à lixeira -> {posicao_agente}")

    tempo_fim = time.perf_counter()
    tempo_execucao_ms = (tempo_fim - tempo_inicio) * 1000

    resultado = {
        "arquitetura": "Reativo Simples",
        "lixos_coletados": lixos_coletados,
        "pontuacao_total": pontuacao,
        "numero_passos": passos,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
    }

    return resultado


def mostrar_resultado_agente(resultado):
    print("\nRESULTADO — AGENTE REATIVO SIMPLES")
    print("Lixos coletados:", f"{resultado['lixos_coletados']} / 15")
    print("Pontuação total:", resultado["pontuacao_total"])
    print("Número de passos:", resultado["numero_passos"])
    print("Tempo de execução (ms):", resultado["tempo_execucao_ms"])


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

    # Executa o Agente Reativo Simples sobre o mesmo ambiente gerado
    resultado = agente_reativo_simples(lixos, verboso=False)
    mostrar_resultado_agente(resultado)


if __name__ == "__main__":
    main()