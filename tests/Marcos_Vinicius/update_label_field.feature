Feature: Atualizar Campo de Etiqueta (Labels)

  Scenario: Atualizar o campo nome de uma etiqueta com sucesso
    Given que existe uma etiqueta criada no quadro para teste de campo
    When eu envio uma requisição PUT para o endpoint "/labels/{id}/name" com o novo valor
    Then o código de status da resposta deve ser 200
    And o nome da etiqueta deve ter sido alterado corretamente