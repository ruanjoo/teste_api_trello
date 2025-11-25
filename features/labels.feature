Feature: Trello Labels API
    Como um QA de automação
    Quero validar as operações de CRUD nas Labels do Trello
    Para garantir a integridade da gestão de etiquetas

    Scenario: 1. Get a Label (GET)
        Given que existe uma label para leitura
        When eu busco essa label pelo ID
        Then o status code é 200
        And os dados da label retornam corretamente

    Scenario: 2. Update a label (PUT)
        Given que existe uma label para atualização completa
        When eu atualizo a label com nome "Update Full" e cor "red" 
        Then o status code é 200
        And o nome e a cor da label são atualizados

    Scenario: 3. Delete a Label (DEL)
        Given que existe uma label para deleção
        When eu envio o comando de delete
        Then o status code é 200
        And a label não é mais encontrada (404)

    Scenario: 4. Update a field on a label (PUT)
        Given que existe uma label para atualização de campo
        When eu atualizo apenas a cor para "blue"
        Then o status code é 200
        And a cor muda para "blue" mas o nome original é mantido

    Scenario: 5. Create a Label (POST)
        Given que tenho dados válidos para nova label
        When eu envio o comando de create
        Then o status code é 200
        And a API retorna o ID da nova label