import sqlite3

# Conectar ao banco de dados (será criado se não existir)
conexao = sqlite3.connect('meu_banco.db')

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Criar a tabela 'enable' com os campos id, nome e imagem
cursor.execute('''CREATE TABLE IF NOT EXISTS enable (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    imagem BLOB
                )''')

# Criar a tabela 'hand' com os mesmos campos id, nome e imagem
cursor.execute('''CREATE TABLE IF NOT EXISTS hand (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    imagem BLOB
                )''')

# Salvar as alterações e fechar a conexão
conexao.commit()
conexao.close()