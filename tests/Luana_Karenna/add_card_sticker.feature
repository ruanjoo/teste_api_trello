Feature: Adicionar Sticker ao Cartão

  Scenario: Adicionar um sticker de coracao a um cartao criado dinamicamente
    Given que preparei um cartao para receber um sticker
    When eu envio uma requisicao POST para adicionar um sticker "heart" com coordenadas validas
    Then o status code da resposta deve ser 200
    And a resposta deve conter o ID do sticker e a imagem correta