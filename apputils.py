import random
import math
import statistics
from typing import List

# -----------------------------
# Funções Estatísticas Gerais
# -----------------------------

def probabilidade_acima_x(dados: List[float], alvo: float, n: int = 100_000) -> float:
    """
    Calcula a probabilidade de os valores simulados superarem o alvo usando distribuição exponencial.
    
    :param dados: lista de multiplicadores históricos
    :param alvo: multiplicador alvo (ex: 3X)
    :param n: número de simulações Monte Carlo
    :return: probabilidade em percentual (float)
    """
    if len(dados) == 0:
        return 0.0

    media = sum(dados) / len(dados)
    lambda_ = 1 / media

    acertos = 0
    for _ in range(n):
        r = random.random()
        x = -math.log(1 - r) / lambda_
        if x >= alvo:
            acertos += 1

    return round((acertos / n) * 100, 2)


def classificar_mercado(probabilidade: float) -> str:
    """
    Classifica o mercado baseado nas regras definidas:
    10-30% -> RECOLHENDO
    40-50% -> MÉDIO
    60-80% -> PAGANDO
    Qualquer outro valor -> NEUTRO
    
    :param probabilidade: probabilidade calculada em %
    :return: string da classificação
    """
    if 10 <= probabilidade <= 30:
        return "RECOLHENDO"
    elif 40 <= probabilidade <= 50:
        return "MÉDIO"
    elif 60 <= probabilidade <= 80:
        return "PAGANDO"
    else:
        return "NEUTRO"


def gerar_sinal(dados: List[float], alvo: float) -> dict:
    """
    Gera o sinal final no formato da API:
    POSSÍVEL X
    PROBABILIDADE: YY%
    MERCADO: [RECOLHENDO|MÉDIO|PAGANDO]
    
    :param dados: lista de multiplicadores históricos
    :param alvo: multiplicador alvo
    :return: dict com sinal completo
    """
    prob = probabilidade_acima_x(dados, alvo)
    mercado = classificar_mercado(prob)

    return {
        "POSSÍVEL": f"{alvo}X",
        "PROBABILIDADE": f"{prob}%",
        "MERCADO": mercado
    }


def calcular_volatilidade(dados: List[float]) -> float:
    """
    Retorna o desvio padrão do histórico, indicador de volatilidade.
    
    :param dados: lista de multiplicadores históricos
    :return: desvio padrão arredondado
    """
    if len(dados) < 2:
        return 0.0
    return round(statistics.stdev(dados), 2)
