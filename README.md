# Automação de Testes de API – Trello

Este repositório contém uma suíte de testes automatizados para a API REST do Trello, escrita em Python e estruturada com metodologia BDD. Os testes validam operações de criação, leitura, atualização e exclusão de recursos como quadros, cartões, listas e etiquetas.

## Tecnologias Utilizadas

O projeto utiliza as seguintes ferramentas e versões:

Python 3.13 – Linguagem principal  
Pytest 9.0.1 – Framework de testes  
Pytest-BDD 8.1.0 – Suporte a BDD com sintaxe Gherkin  
Requests 2.32.5 – Cliente HTTP para interações com a API  
Allure-Pytest 2.15.0 – Geração de relatórios gráficos  
Python-dotenv 1.2.1 – Carregamento de variáveis de ambiente

## Pré-requisitos

Antes de iniciar, instale em seu ambiente:

Python 3.13 ou superior  
Git  
Allure Commandline (opcional, utilizado para visualizar relatórios HTML)

## Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/ruanjoo/teste_api_trello.git
cd teste_api_trello
```

## 2. Criar e ativar o ambiente virtual

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```
### Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Configurar variáveis de ambiente
Crie um arquivo .env na raiz do projeto baseado no .env.example.

```bash
TRELLO_KEY=sua_api_key
TRELLO_TOKEN=seu_token
BASE_URL=https://api.trello.com/1
```

O arquivo .env não é versionado por razões de segurança.

## Execução dos Testes
### Executar toda a suíte
```bash
pytest -v
```

### Executar um teste específico
```bash
pytest -v tests/caminho/do/arquivo_test.py
```

## Relatórios com Allure
### Gerar resultados
```bash
pytest --alluredir=allure-results
```

### Gerar e visualizar relatório
```bash
allure serve allure-results
```

## Estrutura do Projeto
projeto segue uma divisão modular:

tests/ – Contém os testes Python e arquivos .feature, organizados por autores (Gabriel Vieira, Luana Karenna, Marcos Vinicius, Ruan Aquino, Victor Fernandes).

pytest.ini – Configuração global do Pytest.

requirements.txt – Dependências do projeto.
