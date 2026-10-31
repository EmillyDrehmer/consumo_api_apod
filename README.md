# 🚀 NASA Explorer

O **NASA Explorer** é uma aplicação desenvolvida em Python que consome uma API da NASA para apresentar publicações relacionadas à astronomia e ao universo.

A plataforma permite explorar imagens, vídeos e informações astronômicas, pesquisar publicações e realizar consultas por datas específicas.

## 🌌 Funcionalidades

- **Explorar publicações:** visualizar conteúdos disponibilizados pela NASA.
- **Filtrar conteúdos:** selecionar publicações de imagens ou vídeos.
- **Pesquisar:** encontrar publicações pelo título.
- **Viagem no tempo:** consultar publicações de uma data específica.
- **Descoberta aleatória:** encontrar uma publicação astronômica aleatória.
- **Descrições:** visualizar explicações sem as marcações HTML.
- **Créditos e fontes:** acessar os créditos e a publicação original no site da NASA.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem de programação |
| Requests | Realização de requisições HTTP |
| Streamlit | Desenvolvimento da interface web |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| HTMLParser | Limpeza das marcações HTML |
| NASA API | Fornecimento dos conteúdos astronômicos |

## 🔗 API utilizada

O projeto utiliza o endpoint:

`https://science.nasa.gov/wp-json/wp/v2/apod-basic`

A API disponibiliza publicações relacionadas ao APOD (*Astronomy Picture of the Day*), incluindo informações como:

- Título da publicação;
- Data;
- Tipo de mídia;
- Imagens e vídeos;
- Descrição astronômica;
- Créditos;
- Link da publicação original.

## 📁 Estrutura do projeto

```text
consumo_api_APOD/
│
├── streamlit/
│   └── app.py
│
├── teste_api.py
├── .env
├── .gitignore
├── requirements.txt
└── venv/
```

## ⚙️ Instalação e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Entrar na pasta do projeto

```bash
cd consumo_api_APOD
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

No Windows:

```bash
.\venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar o arquivo `.env`

Crie um arquivo chamado `.env` na pasta principal do projeto e adicione:

```env
NASA_API_URL=https://science.nasa.gov/wp-json/wp/v2/apod-basic
```

### 7. Executar o teste da API

```bash
python teste_api.py
```

### 8. Iniciar a aplicação

```bash
python -m streamlit run streamlit/app.py
```

Após a execução, o Streamlit disponibilizará o endereço local para acessar a aplicação pelo navegador.

## 🔍 Como funciona?

1. O Python realiza uma requisição HTTP para a API da NASA utilizando a biblioteca Requests.
2. A API retorna as informações no formato JSON.
3. O programa interpreta os dados recebidos.
4. O HTMLParser auxilia na remoção das marcações HTML das descrições.
5. O Streamlit apresenta as informações em uma interface interativa.

## 🎯 Objetivo do projeto

O objetivo do NASA Explorer é praticar o consumo de APIs utilizando Python e desenvolver uma aplicação capaz de organizar e apresentar informações astronômicas de maneira simples e interativa.

O projeto também permite compreender conceitos como requisições HTTP, respostas JSON, variáveis de ambiente, tratamento de dados e desenvolvimento de interfaces web.

---

**Projeto desenvolvido para fins educacionais.**

Os conteúdos astronômicos apresentados são disponibilizados pela NASA.
