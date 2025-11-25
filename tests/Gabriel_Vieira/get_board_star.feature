Feature: Obter Favorito de Quadro (Board Star)

  Scenario: Buscar um board star especifico criado dinamicamente
    Given que eu criei um quadro e o favoritei para gerar um ID de star
    When eu busco esse board star especifico pelo ID
    Then o status code da resposta deve ser 200
    And a resposta deve conter o ID do quadro correto