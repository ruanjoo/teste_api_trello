# Automação de Testes de API - Trello

Este projeto consiste em uma suíte de testes automatizados para a API do Trello, focando na validação de criação de comentários, manipulação de cartões e integridade dos dados retornados.

O projeto foi estruturado seguindo as melhores práticas de segurança para proteção de credenciais sensíveis, simulando um ambiente real de desenvolvimento seguro.

## Tecnologias Utilizadas

* **Python 3.13.5**
* **Pytest**: Framework para execução e asserção dos testes.
* **Requests**: Biblioteca para requisições HTTP.
* **Python-Dotenv**: Gerenciamento de variáveis de ambiente e segurança.

## Segurança e Configuração (.env)

Para garantir a segurança do projeto e evitar o vazamento de credenciais (API Key e Token), este repositório utiliza o padrão de **Variáveis de Ambiente**. As chaves **não estão hardcoded** no código fonte e **não são enviadas para o GitHub**.

Para executar os testes, é necessário configurar as credenciais localmente:

### Passo a Passo de Configuração

1.  **Localize o modelo:** Existe um arquivo chamado `.env.example` na raiz deste repositório.
2.  **Crie o arquivo real:** Crie um arquivo chamado `.env` na mesma pasta.
3.  **Preencha os dados:** Copie o conteúdo do modelo e preencha com suas chaves do Trello:

```ini
# Exemplo do conteúdo do arquivo .env
TRELLO_KEY=sua_chave_api_aqui
TRELLO_TOKEN=seu_token_aqui
TRELLO_BASE_URL=[https://api.trello.com/1](https://api.trello.com/1)
STABLE_CARD_ID=id_do_cartao_para_teste
