import sqlite3


def inserir_dados_enable(nome, imagem):
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO enable (nome, imagem) VALUES (?, ?)", (nome, 
                                                                       imagem))
    conexao.commit()
    conexao.close()


def inserir_dados_hand(nome, imagem):
    conexao = sqlite3.connect('meu_banco.db')
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO hand (nome, imagem) VALUES (?, ?)", (nome, 
                                                                     imagem))
    conexao.commit()
    conexao.close()


