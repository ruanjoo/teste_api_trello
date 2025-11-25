Feature: Deletar Etiqueta (Labels)

  Scenario: Deletar uma etiqueta existente com sucesso
    Given que existe uma etiqueta criada no quadro para ser deletada
    When eu envio uma requisição DELETE para o endpoint "/labels/{id}"
    Then o código de status da resposta deve ser 200
    And a etiqueta não deve mais ser encontrada ao consultar a API