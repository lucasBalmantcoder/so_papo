import psycopg2
from psycopg2 import sql

def create_db():
    # conectando ao bd do postgreeSQL
    connect_db = psycopg2.connect(

        # faça as alterações aqui para fazer funcioanar 
        dbname = 'postgres', user = 'postgres', password = 'postgres', host = 'localhost', port = '5432'
    )

    connect_db.autocommit = True
    cursor = connect_db.cursor()

    # criando o banco de dados
    cursor.execute('CREATE DATABASE sopapo;')
    print("Banco de dados 'sopapo' criado com sucesso!")


    #fechar conexeão com o bd 'postgreeSQL'
    cursor.close()
    connect_db.close()

    def create_table():

        #conecta ao bd que foi criado '-'
        connect_db = psycopg2.connect(
            dbname = 'postgres', user = 'postgres', password = 'postgres', host = 'localhost', port = '5432'
        )

        cursor = connect_db.cursor()

        #criando a tabela
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL
            );
                       
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
            );
            
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                room_id INTEGER REFERENCES rooms(id),
                user_id INTEGER REFERENCES users(id),
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                       
            
""")
        
    print('tabelas criadas com sucesso')

    #fechar conexeão com o bd 'postgreeSQL'
    cursor.close()
    connect_db.commit()
    connect_db.close()

    if __name__ == '__main__':
        create_db()   #criar banco de dados
        create_table()  #criar tabelas