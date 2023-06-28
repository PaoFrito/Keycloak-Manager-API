# Keycloak Management API
Este projeto é um modelo para gerenciar o Keycloak a partir de outro sistema. Ele usa o framework web FastApi com a biblioteca fastapi_keycloak.

## Instalação
Docker e Docker-Compose são necessários para executar o projeto.

Primeiro, construa o dockerfile com o seguinte comando:
```bash
docker build -it any_name_you_want:version .
```
Uma vez construído, vá para o arquivo docker-compose e altere o nome da imagem para o que você acabou de construir.

## Uso
Antes de executar a aplicação, você precisará executar um aplicativo Keycloak (recomendo a versão 18). Você pode ver mais informações <a href="https://fastapi-keycloak.code-specialist.com/quick_start/">aqui</a>.
Após configurar o serviço do Keycloak, adicione as informações necessárias (conforme o arquivo config em src/core/config.py) nas variáveis de um arquivo chamado .env .

Para executar a aplicação em modo de desenvolvimento, use o seguinte comando:

```bash
docker-compose up
```
Isso iniciará o servidor em http://localhost:8080/. Você pode alterar a porta no arquivo docker-compose.yml.

## Documentação da API
A documentação da API pode ser acessada visitando o endpoint /docs, que abrirá o Swagger UI no seu navegador. Esta interface fornece uma interface interativa para explorar e testar os endpoints da API.