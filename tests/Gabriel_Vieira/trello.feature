Feature: Gerenciamento de Membros e Backgrounds do Trello
    Como um usuário da API
    Eu quero gerenciar meus dados e planos de fundo
    Para personalizar meu perfil

    Scenario: 01. Buscar um membro (GET)
        Given que possuo credenciais validas
        When eu busco os dados do membro "me"
        Then o status code da resposta deve ser 200
        And a resposta deve conter o campo "username"

    Scenario: Atualizar a bio e as iniciais do membro com sucesso
        Given que possuo credenciais validas e recupero meu ID
        When eu envio uma requisicao PUT para atualizar a "bio" para "Bio Automatizada" e "initials" para "BT"
        Then o status code da resposta deve ser 200
        And o corpo da resposta deve conter a "bio" igual a "Bio Automatizada"

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