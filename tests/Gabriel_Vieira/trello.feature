Feature: Gerenciamento de Membros e Backgrounds do Trello
    Como um usuário da API
    Eu quero gerenciar meus dados e planos de fundo
    Para personalizar meu perfil

    Scenario: 01. Buscar um membro (GET)
        Given que possuo credenciais validas
        When eu busco os dados do membro "me"
        Then o status code da resposta deve ser 200
        And a resposta deve conter o campo "username"

    Scenario: 02. Atualizar um membro (PUT)
        Given que possuo credenciais validas
        When eu atualizo a Bio do membro para um valor aleatorio
        Then o status code da resposta deve ser 200 ou 401

    Scenario: 03. Buscar backgrounds customizados (GET)
        Given que possuo credenciais validas
        When eu busco a lista de custom board backgrounds
        Then o status code da resposta deve ser 200
        And a resposta deve ser uma lista

    Scenario: 04. Upload de novo background (POST)
        Given que possuo credenciais validas
        And eu tenho um arquivo de imagem valido
        When eu faco o upload da imagem para backgrounds
        Then o status code da resposta deve ser 200 ou 201
        And a resposta deve conter um ID de background

    Scenario: 05. Deletar background customizado (DELETE)
        Given que possuo credenciais validas
        And que um background foi criado no cenario anterior
        When eu envio uma requisicao para deletar esse background
        Then o status code da resposta deve ser 200