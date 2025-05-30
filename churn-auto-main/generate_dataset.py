import pandas as pd
import numpy as np
import random
from faker import Faker
import os

def gerar_dataset_clientes(n=10000, incluir_churn=True, caminho_arquivo='data/clientes.csv'):
    fake = Faker('pt_BR')
    
    np.random.seed(42)
    random.seed(42)
    
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'PE', 'CE', 'SC', 'GO']
    formas_pagamento = ['Cartão de crédito', 'Boleto', 'Pix', 'Transferência']
    
    dados = []

    for i in range(n):
        churn = np.random.choice([0, 1], p=[0.7, 0.3]) if incluir_churn else None
        
        sexo = random.choice(['Masculino', 'Feminino'])
        nome = fake.name_male() if sexo == 'Masculino' else fake.name_female()
        idade = np.random.randint(18, 60)
        tempo_cliente = np.random.randint(1, 60)
        freq_compras = round(np.random.uniform(0.2, 4), 1)
        ticket_medio = round(np.random.uniform(50, 1000), 2)
        total_gasto = round(freq_compras * tempo_cliente * ticket_medio * np.random.uniform(0.7, 1.3), 2)

        avaliacao_base = 4.2 if churn == 0 else 3.0
        avaliacao = round(np.random.normal(avaliacao_base, 0.7), 1)

        cliente = {
            'id_cliente': i + 1,
            'nome': nome,
            'sexo': sexo,
            'idade': idade,
            'estado': random.choice(estados),
            'tempo_como_cliente': tempo_cliente,
            'frequencia_compras': freq_compras,
            'ticket_medio': ticket_medio,
            'total_gasto': total_gasto,
            'forma_pagamento': random.choice(formas_pagamento),
            'ultima_compra': np.random.randint(1, 365),
            'comprou_servico_instal': np.random.choice([0, 1]),
            'reclamacoes': np.random.poisson(0.3),
            'avaliacao_media': avaliacao
        }

        if incluir_churn:
            cliente['churn'] = churn

        dados.append(cliente)

    df = pd.DataFrame(dados)
    df['avaliacao_media'] = df['avaliacao_media'].clip(1, 5)

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    df.to_csv(caminho_arquivo, index=False, encoding='utf-8-sig')
    print(f"Dataset gerado com sucesso: '{caminho_arquivo}'")

    return df

gerar_dataset_clientes(
    n=10000,
    incluir_churn=True,
    caminho_arquivo='data/clientes_churn_loja_auto.csv'
)

gerar_dataset_clientes(
    n=10,
    incluir_churn=False,
    caminho_arquivo='data/novos_clientes.csv'
)