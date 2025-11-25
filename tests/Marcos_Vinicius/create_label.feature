Feature: Criar Etiqueta (Labels)

  Scenario: Criar uma nova etiqueta no quadro com sucesso
    Given que possuo um ID de quadro valido para criar a etiqueta
    When eu envio uma requisição POST para o endpoint "/labels" com nome e cor
    Then o código de status da resposta deve ser 200
    And a resposta deve conter o ID, nome e cor da nova etiqueta