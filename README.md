# bot_discord

Projeto com finalidade de disponibilizar informações sobre o habblet dentro de um servidor de discord e tambem fornecer uma api em fast-api para expor os mesmos dados.

### Clonar o repositório

Clone o repositório do bot_discord, incluindo os submódulos, utilizando o seguinte comando:

```
git clone https://github.com/8b1tz/bot_discord --recursive
```


### Converter os arquivos de entrypoint para formato Unix

Para rodar o ambiente é necessario converter os arquivos sh para o padrão de formatação unix.

Dentro da pasta docker do projeto, abrir o terminal do git clicando com botão direito na pasta e indo em Open Git Bash here e executar os commandos:

```
    dos2unix.exe app/*.sh
    dos2unix.exe front-end/*.sh
```

### Executando docker

No seu editor de código-fonte execute o seguinte comando no terminal:

```
    docker-compose up -d --build
```

Para subir um container sozinho usar o commando:

```
    docker-compose up -d --build --no-deps nome-do-container
```