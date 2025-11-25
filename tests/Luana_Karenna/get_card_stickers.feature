Feature: Obter Stickers de um Cartão

  Scenario: Buscar stickers anexados a um cartao com sucesso
    Given que preparei um cartao com um sticker anexado
    When eu busco a lista de stickers desse cartao
    Then o status code da resposta deve ser 200
    And a resposta deve conter o sticker "star" que foi criado