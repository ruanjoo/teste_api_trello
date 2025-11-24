Feature: Atualizar Ações no Trello
    Como um usuário da API
    Quero corrigir ou alterar o texto de um comentário
    Para manter as informações do cartão atualizadas

Scenario: Atualizar o texto de um comentário existente com sucesso
    Given que existe um comentário com o texto "Texto Original"
    When eu envio uma requisição PUT para alterar o texto para "Texto Editado via BDD"
    Then o código de status da resposta deve ser 200
    And a resposta deve mostrar o novo texto atualizado