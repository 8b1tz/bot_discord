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

### Comandos/Respostas

#### $maketickets
Cria um layout para abrir tickets de suporte ou entrar para a equipe.

![Layout de tickets](https://github.com/8b1tz/bot_discord/assets/53948477/da56c0dd-0a42-4958-9a85-641c21f730b2)

Ao clicar na opção de "Entrar para a equipe", você verá:

![Entrar para a equipe](https://github.com/8b1tz/bot_discord/assets/53948477/349a5596-9b8c-4849-94c8-54c1a2b9a770)

#### $hand
Retorna o objeto com o ID especificado.

#### $enable
Retorna o efeito com o ID especificado.

![Objeto e Efeito](https://github.com/8b1tz/bot_discord/assets/53948477/c7920564-ff32-4d03-a3ac-fbaa3ccf4e15)

#### $image {nome_do_personagem} {ocasião (natal/ pascoa/ aniversário)}
Retorna uma imagem do personagem especificado na ocasião indicada.

![Imagem do personagem](https://github.com/8b1tz/bot_discord/assets/53948477/ac14937c-c552-4a75-837c-7b400a8b509e)
