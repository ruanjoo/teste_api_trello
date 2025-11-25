Feature: Atualizar Etiqueta (Labels)

  Scenario: Atualizar uma etiqueta existente com sucesso
    Given que existe uma etiqueta criada no quadro para ser atualizada
    When eu envio uma requisição PUT para o endpoint "/labels/{id}" com novos dados
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve conter o nome e cor atualizados