Feature: Obter Etiqueta (Labels)

  Scenario: Obter uma etiqueta existente com sucesso
    Given que existe uma etiqueta criada no quadro
    When eu envio uma requisição GET para o endpoint "/labels/{id}"
    Then o código de status da resposta deve ser 200
    And o corpo da resposta deve conter o nome correto da etiqueta