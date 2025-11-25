Feature: Obter Sticker Específico

  Scenario: Buscar um sticker especifico pelo ID
    Given que preparei um cartao e adicionei um sticker nele
    When eu envio uma requisicao GET para buscar esse sticker especifico
    Then o status code da resposta deve ser 200
    And a resposta deve conter o ID e a imagem do sticker criado