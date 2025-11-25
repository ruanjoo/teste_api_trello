Feature: Consultar Ações no Trello
    Como um usuário da API
    Quero consultar os detalhes de uma ação (ex: comentário)
    Para recuperar informações históricas do cartão

Scenario: Consultar um comentário existente pelo ID
    Given que acabei de criar um comentário no cartão
    When eu envio uma requisição GET para buscar essa ação pelo ID
    Then o código de status da resposta deve ser 200
    And o texto da ação retornada deve ser igual ao texto criado