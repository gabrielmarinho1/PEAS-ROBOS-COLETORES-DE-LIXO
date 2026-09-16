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


def distancia_manhattan(p1, p2):
    """Calcula a Distância de Manhattan entre dois pontos (linha, coluna)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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


# ---------------------------------------------------------------------------
# Agente Reativo Baseado em Modelos (com Estado Interno)
# ---------------------------------------------------------------------------

def agente_baseado_em_modelos(lixos_iniciais, limite_passos=20000, verboso=False):
    """Executa o Agente Reativo Baseado em Modelos até coletar e entregar
    todos os lixos (ou até atingir o limite de passos).

    Diferença central em relação ao Reativo Simples:
    - Mantém uma memória interna V[linha][coluna] com a contagem de visitas
      a cada célula do grid 20×20.
    - Na fase de exploração (sem lixo visível nos 8 vizinhos), em vez de
      escolher um vizinho aleatório, consulta V e escolhe o(s) vizinho(s)
      menos visitado(s), quebrando empates com random.choice.
    - Isso reduz loops e redundâncias, melhorando a eficiência de cobertura.

    Parâmetros
    ----------
    lixos_iniciais : dict
        Dicionário {(linha, coluna): tipo} com os lixos do ambiente.
    limite_passos : int
        Número máximo de passos antes de encerrar por segurança.
    verboso : bool
        Se True, imprime cada ação realizada pelo agente.

    Retorna
    -------
    dict
        Métricas de desempenho da execução.
    """

    # --- Cópia do ambiente (não altera o original) ---
    lixos = dict(lixos_iniciais)

    # --- Estado interno do agente ---
    posicao_agente = POSICAO_INICIAL
    carga = None  # Pode ser None (Livre), "O" (Orgânico) ou "R" (Reciclável)

    # --- Memória interna: matriz de visitas V[linha][coluna] ---
    # Indexada de 1 a TAMANHO para corresponder às coordenadas do grid.
    V = [[0] * (TAMANHO + 1) for _ in range(TAMANHO + 1)]

    # Registra a posição inicial como já visitada
    linha_i, coluna_i = POSICAO_INICIAL
    V[linha_i][coluna_i] = 1

    # --- Contadores de desempenho ---
    pontuacao = 0
    lixos_coletados = 0
    passos = 0

    tempo_inicio = time.perf_counter()

    while lixos or carga is not None:

        # Segurança: encerra se o limite de passos for atingido
        if passos >= limite_passos:
            print("Limite de passos atingido. Encerrando execução.")
            break

        # --- Regra 1: Está sobre um lixo e está Livre → Pega o lixo ---
        if posicao_agente in lixos and carga is None:
            carga = lixos.pop(posicao_agente)

            if verboso:
                print(f"Passo {passos}: Pegar Lixo ({carga}) em {posicao_agente}")

        # --- Regra 2: Tem carga e chegou à lixeira → Solta e pontua ---
        elif carga is not None and posicao_agente == POSICAO_LIXEIRA:
            valor = VALOR_RECICLAVEL if carga == "R" else VALOR_ORGANICO
            pontuacao += valor
            lixos_coletados += 1

            if verboso:
                print(f"Passo {passos}: Soltar Lixo ({carga}) em {posicao_agente} "
                      f"(+{valor} pontos)")

            carga = None

        # --- Regra 3: Tem carga mas não está na lixeira → Move à lixeira ---
        elif carga is not None:
            posicao_agente = passo_em_direcao(posicao_agente, POSICAO_LIXEIRA)
            passos += 1

            # Atualiza memória de visitas
            l, c = posicao_agente
            V[l][c] += 1

            if verboso:
                print(f"Passo {passos}: Mover em direção à lixeira -> {posicao_agente}")

        # --- Regra 4: Livre e detecta lixo vizinho → Move ao lixo (R > O) ---
        elif carga is None:
            vizinho_alvo = escolher_vizinho_com_lixo(posicao_agente, lixos)

            if vizinho_alvo is not None:
                # Há lixo detectado nos 8 vizinhos: move em direção a ele
                posicao_agente = passo_em_direcao(posicao_agente, vizinho_alvo)
                passos += 1

                l, c = posicao_agente
                V[l][c] += 1

                if verboso:
                    print(f"Passo {passos}: Mover em direção ao lixo -> {posicao_agente}")

            else:
                # --- Regra 5 (Exploração baseada no modelo): ---
                # Nenhum lixo nos vizinhos → consulta V e move ao menos visitado
                vizinhos_validos = obter_vizinhos(posicao_agente)

                # Encontra o menor contador de visitas entre os vizinhos válidos
                menor_visitas = min(V[l][c] for l, c in vizinhos_validos)

                # Filtra apenas os vizinhos empatados no menor número de visitas
                candidatos = [
                    v for v in vizinhos_validos
                    if V[v[0]][v[1]] == menor_visitas
                ]

                # Quebra empates aleatoriamente entre os candidatos empatados
                posicao_agente = random.choice(candidatos)
                passos += 1

                l, c = posicao_agente
                V[l][c] += 1

                if verboso:
                    print(f"Passo {passos}: Exploração (modelo) -> {posicao_agente} "
                          f"(visitas={V[l][c]})")

    tempo_fim = time.perf_counter()
    tempo_execucao_ms = (tempo_fim - tempo_inicio) * 1000

    resultado = {
        "arquitetura": "Baseado em Modelos",
        "lixos_coletados": lixos_coletados,
        "pontuacao_total": pontuacao,
        "numero_passos": passos,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
    }

    return resultado


# ---------------------------------------------------------------------------
# Agente BDI / Baseado em Objetivos
# ---------------------------------------------------------------------------

def agente_baseado_em_objetivos(lixos_iniciais, limite_passos=20000, verboso=False):
    """Executa o Agente BDI / Baseado em Objetivos até coletar e entregar
    todos os lixos (ou até atingir o limite de passos).

    Arquitetura mental BDI (Beliefs, Desires, Intentions):
    - Crenças (Beliefs):
        * Posição atual do robô R1 (linha, coluna).
        * Estado do inventário C: Livre (None), Orgânico ('O') ou Reciclável ('R').
        * Localização conhecida e fixa da lixeira X em (20, 20).
        * Mapa conhecido V[linha][coluna] registrando as visitas a cada célula.
        * Mapa de crenças dos lixos conhecidos detectados pelos sensores locais
          (célula atual e 8 vizinhos imediatos).
    - Desejos (Desires):
        * Coletar lixos recicláveis (+5 pontos).
        * Coletar lixos orgânicos (+1 ponto).
        * Descarregar e esvaziar a carga na lixeira X(20, 20).
        * Otimizar rotas e minimizar passos.
    - Intenções (Intentions) & Planejamento:
        * Se ocupado (carga != None): compromete-se com a meta da lixeira (20, 20)
          seguindo a rota de menor custo.
        * Se livre (carga == None):
            1. Busca focada em recicláveis: se houver recicláveis conhecidos,
               define a meta como o reciclável mais próximo.
            2. Se não houver recicláveis conhecidos, mas houver orgânicos conhecidos,
               define a meta como o orgânico mais próximo.
            3. Caso nenhum lixo seja conhecido: busca exploratória ativa, elegendo
               como meta a célula não visitada (ou menos visitada) mais próxima no grid.

    Parâmetros
    ----------
    lixos_iniciais : dict
        Dicionário {(linha, coluna): tipo} com os lixos do ambiente.
    limite_passos : int
        Número máximo de passos antes de encerrar por segurança.
    verboso : bool
        Se True, imprime cada ação e intenção realizada pelo agente.

    Retorna
    -------
    dict
        Métricas de desempenho da execução.
    """

    # --- Cópia do ambiente (não altera o original) ---
    lixos = dict(lixos_iniciais)

    # --- Crenças (Beliefs) do agente ---
    crencas = {
        "posicao": POSICAO_INICIAL,
        "carga": None,  # None (Livre), "O" (Orgânico) ou "R" (Reciclável)
        "lixeira": POSICAO_LIXEIRA,
        "V": [[0] * (TAMANHO + 1) for _ in range(TAMANHO + 1)],
        "lixos_conhecidos": {}  # {(linha, coluna): tipo}
    }

    # Registra a posição inicial na memória de visitas
    linha_i, coluna_i = POSICAO_INICIAL
    crencas["V"][linha_i][coluna_i] = 1

    def atualizar_percepcao():
        """Função sensorial: atualiza as crenças do agente sobre os lixos
        observados na posição atual e nos 8 vizinhos imediatos."""
        pos = crencas["posicao"]

        # Percepção da célula atual
        if pos in lixos:
            crencas["lixos_conhecidos"][pos] = lixos[pos]
        elif pos in crencas["lixos_conhecidos"]:
            del crencas["lixos_conhecidos"][pos]

        # Percepção dos 8 vizinhos imediatos
        for vizinho in obter_vizinhos(pos):
            if vizinho in lixos:
                crencas["lixos_conhecidos"][vizinho] = lixos[vizinho]
            elif vizinho in crencas["lixos_conhecidos"]:
                del crencas["lixos_conhecidos"][vizinho]

    # Percepção inicial no ponto de partida
    atualizar_percepcao()

    # --- Contadores de desempenho ---
    pontuacao = 0
    lixos_coletados = 0
    passos = 0

    tempo_inicio = time.perf_counter()

    while lixos or crencas["carga"] is not None:

        if passos >= limite_passos:
            print("Limite de passos atingido. Encerrando execução.")
            break

        posicao_agente = crencas["posicao"]
        carga = crencas["carga"]

        reciclaveis_conhecidos = [
            p for p, t in crencas["lixos_conhecidos"].items() if t == "R"
        ]

        # --- Regra 1: Está sobre um lixo e está Livre ---
        # Priorização de coleta: se for 'R' ou se não houver 'R' conhecido em outro local
        if posicao_agente in lixos and carga is None and (
            lixos[posicao_agente] == "R" or not reciclaveis_conhecidos
        ):
            carga = lixos.pop(posicao_agente)
            crencas["carga"] = carga
            crencas["lixos_conhecidos"].pop(posicao_agente, None)

            if verboso:
                print(f"Passo {passos}: Pegar Lixo ({carga}) em {posicao_agente}")

        # --- Regra 2: Tem carga e chegou à lixeira → Solta e pontua ---
        elif carga is not None and posicao_agente == POSICAO_LIXEIRA:
            valor = VALOR_RECICLAVEL if carga == "R" else VALOR_ORGANICO
            pontuacao += valor
            lixos_coletados += 1

            if verboso:
                print(f"Passo {passos}: Soltar Lixo ({carga}) em {posicao_agente} "
                      f"(+{valor} pontos)")

            carga = None
            crencas["carga"] = None

        # --- Regra 3: Ocupado com carga → Intenção: Descarregar na lixeira (20, 20) ---
        elif carga is not None:
            intencao = "DESCARREGAR_LIXEIRA"
            meta = POSICAO_LIXEIRA

            posicao_agente = passo_em_direcao(posicao_agente, meta)
            passos += 1

            crencas["posicao"] = posicao_agente
            l, c = posicao_agente
            crencas["V"][l][c] += 1
            atualizar_percepcao()

            if verboso:
                print(f"Passo {passos}: [{intencao}] Mover em direção à lixeira {meta} -> {posicao_agente}")

        # --- Regra 4: Livre → Deliberação BDI e Planejamento de Metas ---
        else:
            organicos_conhecidos = [
                p for p, t in crencas["lixos_conhecidos"].items() if t == "O"
            ]

            if reciclaveis_conhecidos:
                # Intenção 1 (Prioritária): Coletar reciclável conhecido mais próximo
                intencao = "COLETAR_RECICLAVEL"
                meta = min(
                    reciclaveis_conhecidos,
                    key=lambda p: distancia_manhattan(posicao_agente, p)
                )

            elif organicos_conhecidos:
                # Intenção 2: Coletar orgânico conhecido mais próximo
                intencao = "COLETAR_ORGANICO"
                meta = min(
                    organicos_conhecidos,
                    key=lambda p: distancia_manhattan(posicao_agente, p)
                )

            else:
                # Intenção 3: Busca exploratória focada em recicláveis
                # Seleciona como meta a célula não visitada (ou menos visitada) mais próxima
                intencao = "EXPLORAR"
                nao_visitadas = [
                    (l, c) for l in range(1, TAMANHO + 1) for c in range(1, TAMANHO + 1)
                    if crencas["V"][l][c] == 0
                ]

                if nao_visitadas:
                    meta = min(
                        nao_visitadas,
                        key=lambda p: (distancia_manhattan(posicao_agente, p), p[0], p[1])
                    )
                else:
                    menor_visitas = min(
                        crencas["V"][l][c] for l in range(1, TAMANHO + 1) for c in range(1, TAMANHO + 1)
                    )
                    candidatos = [
                        (l, c) for l in range(1, TAMANHO + 1) for c in range(1, TAMANHO + 1)
                        if crencas["V"][l][c] == menor_visitas
                    ]
                    meta = min(
                        candidatos,
                        key=lambda p: (distancia_manhattan(posicao_agente, p), p[0], p[1])
                    )

            posicao_agente = passo_em_direcao(posicao_agente, meta)
            passos += 1

            crencas["posicao"] = posicao_agente
            l, c = posicao_agente
            crencas["V"][l][c] += 1
            atualizar_percepcao()

            if verboso:
                print(f"Passo {passos}: [{intencao}] Mover em direção a {meta} -> {posicao_agente}")

    tempo_fim = time.perf_counter()
    tempo_execucao_ms = (tempo_fim - tempo_inicio) * 1000

    resultado = {
        "arquitetura": "Baseado em Objetivos",
        "lixos_coletados": lixos_coletados,
        "pontuacao_total": pontuacao,
        "numero_passos": passos,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
    }

    return resultado

# ---------------------------------------------------------------------------
# Agente Baseado em Utilidades
# ---------------------------------------------------------------------------

def agente_baseado_em_utilidades(lixos_iniciais, limite_passos=20000, verboso=False):
    """Executa o Agente Baseado em Utilidade avaliando o custo-benefício."""
    lixos = dict(lixos_iniciais)

    crencas = {
        "posicao": POSICAO_INICIAL,
        "carga": None,
        "lixeira": POSICAO_LIXEIRA,
        "V": [[0] * (TAMANHO + 1) for _ in range(TAMANHO + 1)],
        "lixos_conhecidos": {}
    }

    linha_i, coluna_i = POSICAO_INICIAL
    crencas["V"][linha_i][coluna_i] = 1

    def atualizar_percepcao():
        pos = crencas["posicao"]
        if pos in lixos:
            crencas["lixos_conhecidos"][pos] = lixos[pos]
        elif pos in crencas["lixos_conhecidos"]:
            del crencas["lixos_conhecidos"][pos]

        for vizinho in obter_vizinhos(pos):
            if vizinho in lixos:
                crencas["lixos_conhecidos"][vizinho] = lixos[vizinho]
            elif vizinho in crencas["lixos_conhecidos"]:
                del crencas["lixos_conhecidos"][vizinho]

    atualizar_percepcao()
    pontuacao = 0
    lixos_coletados = 0
    passos = 0
    tempo_inicio = time.perf_counter()

    while lixos or crencas["carga"] is not None:
        if passos >= limite_passos:
            break

        posicao_agente = crencas["posicao"]
        carga = crencas["carga"]

        # 1. Pegar lixo (Priorizando reciclável local)
        if posicao_agente in lixos and carga is None:
            carga = lixos.pop(posicao_agente)
            crencas["carga"] = carga
            crencas["lixos_conhecidos"].pop(posicao_agente, None)

        # 2. Soltar lixo na lixeira
        elif carga is not None and posicao_agente == POSICAO_LIXEIRA:
            pontuacao += VALOR_RECICLAVEL if carga == "R" else VALOR_ORGANICO
            lixos_coletados += 1
            carga = None
            crencas["carga"] = None

        # 3. Levar carga para a lixeira
        elif carga is not None:
            meta = POSICAO_LIXEIRA
            posicao_agente = passo_em_direcao(posicao_agente, meta)
            passos += 1
            crencas["posicao"] = posicao_agente
            crencas["V"][posicao_agente[0]][posicao_agente[1]] += 1
            atualizar_percepcao()

        # 4. Decisão por Utilidade
        else:
            if crencas["lixos_conhecidos"]:
                melhor_lixo = None
                maior_utilidade = -float('inf')

                for pos_lixo, tipo_lixo in crencas["lixos_conhecidos"].items():
                    valor = VALOR_RECICLAVEL if tipo_lixo == "R" else VALOR_ORGANICO
                    d_agente_lixo = distancia_manhattan(posicao_agente, pos_lixo)
                    d_lixo_lixeira = distancia_manhattan(pos_lixo, POSICAO_LIXEIRA)

                    # Custo-benefício da ação
                    utilidade = valor - (1 * d_agente_lixo) - d_lixo_lixeira

                    if utilidade > maior_utilidade:
                        maior_utilidade = utilidade
                        melhor_lixo = pos_lixo

                meta = melhor_lixo
            else:
                # Explorar mapa (célula não visitada mais próxima)
                nao_visitadas = [
                    (l, c) for l in range(1, TAMANHO + 1) for c in range(1, TAMANHO + 1)
                    if crencas["V"][l][c] == 0
                ]
                if nao_visitadas:
                    meta = min(nao_visitadas, key=lambda p: (distancia_manhattan(posicao_agente, p), p[0], p[1]))
                else:
                    menor_visitas = min(
                        crencas["V"][l][c] for l in range(1, TAMANHO + 1) for c in range(1, TAMANHO + 1))
                    candidatos = [(l, c) for l in range(1, TAMANHO + 1) for c in range(1, TAMANHO + 1) if
                                  crencas["V"][l][c] == menor_visitas]
                    meta = min(candidatos, key=lambda p: (distancia_manhattan(posicao_agente, p), p[0], p[1]))

            posicao_agente = passo_em_direcao(posicao_agente, meta)
            passos += 1
            crencas["posicao"] = posicao_agente
            crencas["V"][posicao_agente[0]][posicao_agente[1]] += 1
            atualizar_percepcao()

    tempo_execucao_ms = (time.perf_counter() - tempo_inicio) * 1000
    return {
        "arquitetura": "Baseado em Utilidade",
        "lixos_coletados": lixos_coletados,
        "pontuacao_total": pontuacao,
        "numero_passos": passos,
        "tempo_execucao_ms": round(tempo_execucao_ms, 3),
    }

# ---------------------------------------------------------------------------
# Exibição de resultados
# ---------------------------------------------------------------------------

def mostrar_resultado_agente(resultado):
    """Exibe o resultado individual de um agente de forma legível."""
    total_lixos = QUANTIDADE_ORGANICO + QUANTIDADE_RECICLAVEL
    arquitetura = resultado["arquitetura"]
    print(f"\nRESULTADO — AGENTE {arquitetura.upper()}")
    print(f"  Lixos coletados : {resultado['lixos_coletados']} / {total_lixos}")
    print(f"  Pontuação total : {resultado['pontuacao_total']}")
    print(f"  Número de passos: {resultado['numero_passos']}")
    print(f"  Tempo (ms)      : {resultado['tempo_execucao_ms']}")


def mostrar_tabela_comparativa(resultados):
    """Exibe uma tabela comparativa lado a lado entre os agentes fornecidos.

    Parâmetros
    ----------
    resultados : list[dict]
        Lista com os dicionários de resultado de cada agente (na ordem
        em que devem aparecer na tabela).
    """
    total_lixos = QUANTIDADE_ORGANICO + QUANTIDADE_RECICLAVEL

    # Larguras das colunas
    col_metrica = 24
    col_valor   = 22

    n = len(resultados)
    cabecalhos = [r["arquitetura"] for r in resultados]

    separador = "+" + ("-" * col_metrica) + "+" + ("+".join(["-" * col_valor] * n)) + "+"

    print("\n" + "=" * len(separador))
    print("  TABELA COMPARATIVA DE AGENTES")
    print("=" * len(separador))
    print(separador)

    # Linha de cabeçalhos das arquiteturas
    cabecalho_linha = "|" + " Métrica".ljust(col_metrica) + "|"
    for cab in cabecalhos:
        cabecalho_linha += cab.center(col_valor) + "|"
    print(cabecalho_linha)
    print(separador)

    # Linhas de dados
    metricas = [
        ("Lixos Coletados",  lambda r: f"{r['lixos_coletados']} / {total_lixos}"),
        ("Pontuação Total",  lambda r: str(r["pontuacao_total"])),
        ("Número de Passos", lambda r: str(r["numero_passos"])),
        ("Tempo (ms)",       lambda r: str(r["tempo_execucao_ms"])),
    ]

    for nome_metrica, extrator in metricas:
        linha = "|" + f" {nome_metrica}".ljust(col_metrica) + "|"
        for r in resultados:
            linha += extrator(r).center(col_valor) + "|"
        print(linha)

    print(separador)
    print()


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def main():

    # Gera o ambiente determinístico com SEMENTE = 42
    lixos = criar_ambiente()

    mostrar_ambiente(lixos)
    mostrar_resumo(lixos)

    print("\nLEGENDA")
    print("A = Agente")
    print("X = Lixeira")
    print("O = Lixo orgânico")
    print("R = Lixo reciclável")
    print(". = Espaço vazio")

    # --- Arquitetura 1: Agente Reativo Simples ---
    resultado_simples = agente_reativo_simples(lixos, verboso=False)
    mostrar_resultado_agente(resultado_simples)

    # --- Arquitetura 2: Agente Baseado em Modelos ---
    resultado_modelos = agente_baseado_em_modelos(lixos, verboso=False)
    mostrar_resultado_agente(resultado_modelos)

    # --- Arquitetura 3: Agente BDI / Baseado em Objetivos ---
    resultado_objetivos = agente_baseado_em_objetivos(lixos, verboso=False)
    mostrar_resultado_agente(resultado_objetivos)

    # --- Arquitetura 4: Agente Baseado em Utilidade ---
    resultado_utilidade = agente_baseado_em_utilidades(lixos, verboso=False)
    mostrar_resultado_agente(resultado_utilidade)

    # --- Tabela Comparativa ---
    mostrar_tabela_comparativa([resultado_simples, resultado_modelos, resultado_objetivos, resultado_utilidade])

if __name__ == "__main__":
    main()