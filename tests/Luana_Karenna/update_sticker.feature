Feature: Atualizar Sticker no Cartão

  Scenario: Atualizar a posicao de um sticker existente
    Given que preparei um cartao com um sticker original na posicao zero
    When eu envio uma requisicao PUT para mover o sticker para novas coordenadas
    Then o status code da resposta deve ser 200
    And a resposta deve conter as novas coordenadas atualizadas