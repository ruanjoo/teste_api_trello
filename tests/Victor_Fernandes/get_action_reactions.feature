Feature: Consultar Reações no Trello
    Como um usuário da API
    Quero consultar os detalhes de uma reação específica
    Para validar se a interação foi registrada corretamente

Scenario: Consultar detalhes de uma reação existente pelo ID
    Given que existe um comentário com uma reação criada
    When eu envio uma requisição GET para buscar essa reação pelo ID
    Then o código de status da resposta deve ser 200
    And os dados da reação retornada devem corresponder à reação criada