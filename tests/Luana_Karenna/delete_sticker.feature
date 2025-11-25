Feature: Deletar Sticker do Cartão

  Scenario: Remover um sticker existente de um cartao
    Given que preparei um cartao com um sticker para ser deletado
    When eu envio uma requisicao DELETE para remover esse sticker
    Then o status code da resposta deve ser 200
    And o sticker nao deve mais ser encontrado no cartao