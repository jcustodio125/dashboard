# Dashboard de Vendas com API Mock

Este projeto consiste em um dashboard Streamlit que exibe dados de vendas obtidos de uma API mockada construída com FastAPI.  O projeto é containerizado com Docker para facilitar a execução e garantir a consistência do ambiente.

## Pré-requisitos

*   Docker e Docker Compose instalados.  Você pode encontrá-los em:
    *   [Docker Desktop](https://www.docker.com/products/docker-desktop) (inclui Docker Compose)
    *   Ou instale separadamente seguindo as instruções para o seu sistema operacional.

## Como Executar

1.  **Clone o repositório:**

    Se você ainda não clonou o repositório, faça-o:

    ```bash
    git clone <https://github.com/jcustodio125/dashboard.git>
    cd <dashboard>
    ```

2.  **Execute com Docker Compose:**

    A forma mais simples de rodar o projeto é usando o Docker Compose.  No diretório raiz do projeto (onde o arquivo `docker-compose.yml` está localizado), execute o seguinte comando:

    ```bash
    docker-compose up -d
    ```

    Este comando irá construir as imagens Docker para a API e o dashboard (se ainda não tiverem sido construídas) e então iniciar os contêineres em segundo plano.

3.  **Acesse o Dashboard:**

    Após alguns segundos para os contêineres iniciarem, abra o seu navegador e acesse a seguinte URL:

    ```
    http://localhost:8501
    ```

    Você deverá ver o dashboard do Streamlit exibindo os dados de vendas.

4.  **Parar a Execução:**

    Para parar os contêineres, execute:

    ```bash
    docker-compose down
    ```

## Estrutura do Projeto

*   `Dockerfile.api`: Define a imagem Docker para a API FastAPI.
*   `mock_api.py`: Código da API FastAPI que gera dados de vendas mockados.
*   `Dockerfile`: Define a imagem Docker para o dashboard Streamlit.
*   `dashboard.py`: Código do dashboard Streamlit que consome os dados da API e exibe os gráficos.
*   `requirements.txt`: Lista de dependências Python para ambos os serviços.
*   `docker-compose.yml`: Arquivo de configuração do Docker Compose para orquestrar os serviços da API e do dashboard.

## Observações

*   O dashboard tenta se conectar à API na URL `http://api:8000/vendas`.  Essa URL funciona dentro do ambiente Docker Compose, onde os serviços podem se comunicar pelo nome do serviço (`api`).  Se você quiser rodar o dashboard ou a API fora do Docker, precisará ajustar a URL no código do dashboard.