import statistics
import random

# Importa as configurações e os agentes do seu arquivo principal
from main import (
    TAMANHO, QUANTIDADE_ORGANICO, QUANTIDADE_RECICLAVEL,
    POSICAO_INICIAL, POSICAO_LIXEIRA,
    agente_reativo_simples, agente_baseado_em_modelos,
    agente_baseado_em_objetivos, agente_baseado_em_utilidades
)

# Configuração da análise
NUM_EXECUCOES = 30  # Número de vezes que cada agente será testado


def criar_ambiente_aleatorio(semente):
    """
    Versão modificada do criar_ambiente que aceita sementes variáveis
    para testarmos os agentes em diferentes distribuições de lixo.
    """
    random.seed(semente)
    posicoes_disponiveis = []

    for linha in range(1, TAMANHO + 1):
        for coluna in range(1, TAMANHO + 1):
            posicao = (linha, coluna)
            if posicao != POSICAO_INICIAL and posicao != POSICAO_LIXEIRA:
                posicoes_disponiveis.append(posicao)

    quantidade_total = QUANTIDADE_ORGANICO + QUANTIDADE_RECICLAVEL
    posicoes_lixos = random.sample(posicoes_disponiveis, quantidade_total)

    lixos = {}
    for posicao in posicoes_lixos[:QUANTIDADE_ORGANICO]:
        lixos[posicao] = "O"
    for posicao in posicoes_lixos[QUANTIDADE_ORGANICO:]:
        lixos[posicao] = "R"

    return lixos


def exibir_tabela_estatistica(titulo, dados, metrica):
    """Função auxiliar para imprimir os resultados formatados em tabela."""
    print(f"\n{titulo}")
    print("-" * 85)
    print(f"{'Agente':<25} | {'Mínimo (Melhor)':<15} | {'Máximo (Pior)':<15} | {'Média':<10} | {'Desvio Padrão':<15}")
    print("-" * 85)

    for agente, valores in dados.items():
        lista_valores = valores[metrica]
        minimo = min(lista_valores)
        maximo = max(lista_valores)
        media = statistics.mean(lista_valores)
        desvio = statistics.stdev(lista_valores) if len(lista_valores) > 1 else 0.0

        print(f"{agente:<25} | {minimo:<15.2f} | {maximo:<15.2f} | {media:<10.2f} | {desvio:<15.2f}")
    print("-" * 85)


def main():
    print(f"Iniciando análise de desempenho com {NUM_EXECUCOES} execuções...")

    # Dicionário para armazenar o histórico de todas as execuções
    historico = {
        "Reativo Simples": {"passos": [], "tempo": []},
        "Baseado em Modelos": {"passos": [], "tempo": []},
        "Baseado em Objetivos": {"passos": [], "tempo": []},
        "Baseado em Utilidades": {"passos": [], "tempo": []}
    }

    for i in range(NUM_EXECUCOES):
        # A cada iteração, gera um mapa diferente (usando 'i' como semente)
        lixos = criar_ambiente_aleatorio(semente=i)

        # Executa os 4 agentes no mesmo mapa 'i' para ser justo
        res_simples = agente_reativo_simples(lixos, verboso=False)
        res_modelos = agente_baseado_em_modelos(lixos, verboso=False)
        res_objetivos = agente_baseado_em_objetivos(lixos, verboso=False)
        res_utilidades = agente_baseado_em_utilidades(lixos, verboso=False)

        # Salva os resultados
        historico["Reativo Simples"]["passos"].append(res_simples["numero_passos"])
        historico["Reativo Simples"]["tempo"].append(res_simples["tempo_execucao_ms"])

        historico["Baseado em Modelos"]["passos"].append(res_modelos["numero_passos"])
        historico["Baseado em Modelos"]["tempo"].append(res_modelos["tempo_execucao_ms"])

        historico["Baseado em Objetivos"]["passos"].append(res_objetivos["numero_passos"])
        historico["Baseado em Objetivos"]["tempo"].append(res_objetivos["tempo_execucao_ms"])

        historico["Baseado em Utilidades"]["passos"].append(res_utilidades["numero_passos"])
        historico["Baseado em Utilidades"]["tempo"].append(res_utilidades["tempo_execucao_ms"])

        if (i + 1) % 5 == 0:
            print(f"Progresso: {i + 1}/{NUM_EXECUCOES} execuções concluídas...")

    # Exibe os relatórios
    print("\nANÁLISE CONCLUÍDA! GERANDO RELATÓRIOS...\n")

    exibir_tabela_estatistica(
        "ANÁLISE DE PASSOS (Esforço do Agente - Quanto menor, mais inteligente/eficiente)",
        historico,
        "passos"
    )

    exibir_tabela_estatistica(
        "ANÁLISE DE TEMPO DE EXECUÇÃO EM MS (Custo Computacional - Quanto menor, mais rápido)",
        historico,
        "tempo"
    )


if __name__ == "__main__":
    main()