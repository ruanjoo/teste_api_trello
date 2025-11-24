Feature: Criar Reações no Trello
    Como um usuário da API
    Quero reagir a comentários
    Para expressar feedback visualmente

Scenario: Adicionar uma reação (Joinha) a um comentário com sucesso
    Given que existe um comentário criado no cartão
    When eu envio uma requisição POST para adicionar a reação "1F44D" neste comentário
    Then o código de status da resposta deve ser 200
    And a resposta deve conter o código do emoji "1F44D" e o ID correto