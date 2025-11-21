Feature: Trello Action Specific Field
  Como um desenvolvedor da API
  Quero recuperar um campo específico de uma Action via URL
  Para validar dados isolados sem carregar o objeto inteiro

  Scenario: Validar o retorno do campo "type" via URL direta
    Given que eu tenho credenciais válidas do Trello
    And existe um comentário recém-criado no card padrão
    When eu faço um GET na rota específica "/actions/{id}/{field}" buscando o campo "type"
    Then o status code da resposta deve ser 200
    And o JSON de resposta deve conter a chave "_value" com o valor "commentCard"