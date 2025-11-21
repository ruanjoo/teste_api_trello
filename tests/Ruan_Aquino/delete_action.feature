Feature: Deletar Comentários (Actions)

  Scenario: Deletar um comentário existente com sucesso
    Given que existe um comentário criado em um cartão
    When eu envio uma requisição DELETE para o endpoint "/actions/{id}"
    Then o código de status da resposta deve ser 200
    And o comentário não deve mais ser encontrado ao consultar a API