Feature: Gerenciar Reações no Trello
    Como um usuário da API
    Quero remover reações de comentários
    Para manter o histórico limpo

Scenario: Deletar uma reação existente com sucesso
    Given que existe um comentário criado no cartão alvo
    And que eu adicionei uma reação a este comentário
    When eu envio uma requisição DELETE para remover essa reação
    Then o código de status da resposta deve ser 200