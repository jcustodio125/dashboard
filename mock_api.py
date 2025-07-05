from fastapi import FastAPI
from faker import Faker
from typing import List
from pydantic import BaseModel
import random
from datetime import datetime, timedelta

app = FastAPI()
fake = Faker("pt_BR")

# Modelo para a venda
class Venda(BaseModel):
    data: str
    produto: str
    categoria: str
    valor: float
    quantidade: int
    regiao: str

produtos = [
    ("Camiseta Preta", "Roupas"),
    ("Tênis Branco", "Calçados"),
    ("Calça Jeans", "Roupas"),
    ("Boné Azul", "Acessórios"),
    ("Jaqueta Couro", "Roupas"),
    ("Sandália Praia", "Calçados"),
]

regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

def gerar_venda():
    produto, categoria = random.choice(produtos)
    valor_base = {
        "Camiseta Preta": 89.90,
        "Tênis Branco": 219.90,
        "Calça Jeans": 139.90,
        "Boné Azul": 59.90,
        "Jaqueta Couro": 299.90,
        "Sandália Praia": 49.90,
    }[produto]
    quantidade = random.randint(1, 5)
    valor = round(valor_base * quantidade * random.uniform(0.8, 1.2), 2)
    data = fake.date_between(start_date='-30d', end_date='today').strftime("%Y-%m-%d")
    regiao = random.choice(regioes)
    return Venda(
        data=data,
        produto=produto,
        categoria=categoria,
        valor=valor,
        quantidade=quantidade,
        regiao=regiao,
    )

@app.get("/vendas", response_model=List[Venda])
def listar_vendas():
    vendas = [gerar_venda() for _ in range(100)]
    return vendas
