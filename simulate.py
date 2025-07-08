from algorithms import measure_time, generate_points, closest_pair_brute_force, closest_pair_divide_and_conquer
from math import dist
import random
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime

def format_seconds(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def run_experiment(alg1, alg2, name1="Força Bruta", name2="Divisão e Conquista"):
    k = random.randint(100, 200)
    m = random.randint(10, 20)
    print(f"📊 k = {k}, m = {m} (total de execuções: {k*m})")

    sizes = [10 + i * ((10000 - 10) // (k - 1)) for i in range(k)]

    data = []
    total_runs = k * m
    count = 0
    start_time = time.perf_counter()
    
    # Variável de suavização
    avg_time = None
    alpha = 0.1  # Peso da média exponencial

    for n in sizes:
        for _ in range(m):
            count += 1
            points = generate_points(n)

            t1, r1 = measure_time(alg1, points)
            t2, r2 = measure_time(alg2, points)

            d1 = dist(*r1)
            d2 = dist(*r2)

            if round(d1, 6) != round(d2, 6):
                print(f"⚠️ Resultado diferente em n={n}")

            data.append({'Tamanho': n, 'Tempo': t1, 'Algoritmo': name1})
            data.append({'Tamanho': n, 'Tempo': t2, 'Algoritmo': name2})

            # Estimativa com suavização exponencial
            elapsed = time.perf_counter() - start_time
            time_per_run = elapsed / count

            if avg_time is None:
                avg_time = time_per_run
            else:
                avg_time = alpha * time_per_run + (1 - alpha) * avg_time

            if count > total_runs * 0.05:  # só mostra após 5% das execuções
                remaining = avg_time * (total_runs - count)
                print(f"[{count}/{total_runs}] ⏱️ Elapsed: {format_seconds(elapsed)} | Remaining: ~{format_seconds(remaining)}", end='\r')

    print("\n✅ Experimento concluído.")
    return pd.DataFrame(data)

def plotar_grafico(df, filename):

    plt.figure(figsize=(12, 6))

    # Agrupa os dados por algoritmo e tamanho e calcula média e desvio padrão
    grouped = df.groupby(['Algoritmo', 'Tamanho'])['Tempo']
    mean = grouped.mean().unstack(level=0)
    std = grouped.std().unstack(level=0)

    # Plota com barras de erro
    for algoritmo in mean.columns:
        plt.errorbar(
            mean.index,                 # Tamanhos de entrada (n)
            mean[algoritmo],            # Tempo médio
            yerr=std[algoritmo],        # Desvio padrão
            label=algoritmo,            # Nome do algoritmo
            capsize=3                   # Barras de erro com "tampinha"
        )

    plt.title("Comparação de Desempenho: Par de Pontos Mais Próximos")
    plt.xlabel("Tamanho da Entrada (n)")
    plt.ylabel("Tempo de Execução (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def main():
    # Passo 1: Importar ou definir os algoritmos
    # Certifique-se de que essas funções já estão definidas no mesmo notebook/script:
    # closest_pair_brute_force, closest_pair_divide_and_conquer

    # Passo 2: Rodar os experimentos
    print("⏳ Rodando experimentos, isso pode demorar um pouco...")
    df_resultados = run_experiment(
        closest_pair_brute_force,
        closest_pair_divide_and_conquer,
        name1="Força Bruta",
        name2="Divisão e Conquista"
    )

    # Passo 3: Plotar e salvar gráfico
    print("📊 Gerando e salvando gráfico...")
    plotar_grafico(df_resultados, filename="grafico_par_pontos_mais_proximos.png")

    # Passo 4 (opcional): Salvar dados em CSV
    df_resultados.to_csv("resultados_tempos.csv", index=False)
    print("📝 Resultados salvos em 'resultados_tempos.csv'.")

if __name__ == "__main__":
    main()

