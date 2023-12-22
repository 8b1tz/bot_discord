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


inserir_dados_enable('Nome1', b'dados_da_imagem1')


inserir_dados_hand('Nome2', b'dados_da_imagem2')
