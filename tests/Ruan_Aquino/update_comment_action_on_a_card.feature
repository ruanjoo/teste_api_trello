Feature: Gestão de Comentários no Card
    Como um usuário da API do Trello
    Quero atualizar comentários nos cards
    Para corrigir informações erradas

    Scenario: Atualizar um comentário com sucesso
        Given que tenho um card ativo em um board temporário
        And existe um comentário nesse card com o texto "Reunião às 14h"
        When eu envio uma requisição PUT para atualizar o comentário para "Reunião reagendada para 16h"
        Then o status code da resposta deve ser 200
        And o campo "text" na resposta deve ser "Reunião reagendada para 16h"