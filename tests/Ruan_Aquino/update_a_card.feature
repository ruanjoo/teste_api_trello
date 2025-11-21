Feature: Atualizar nome e descrição de um cartão com sucesso
    Como um usuário da API
    Quero alterar os detalhes de um cartão
    Para manter minhas tarefas atualizadas

    Scenario: Atualizar nome e descrição de um cartão com sucesso
        Given que possuo credenciais válidas e o ID de um cartão existente
        When eu envio uma requisição PUT para atualizar o nome e a descrição
        Then o código de status da resposta deve ser 200
        And os dados retornados devem corresponder aos novos valores enviados