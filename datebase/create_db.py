import psycopg2

def create_db():
    # Conectando ao banco de dados PostgreSQL
    connect_db = psycopg2.connect(
        dbname='postgres', user='postgres', password='mysenha', host='localhost', port='5432'
    )

    connect_db.autocommit = True  # Garante que o comando CREATE DATABASE seja executado sem precisar de commit
    cursor = connect_db.cursor()

    # Criando o banco de dados
    cursor.execute('CREATE DATABASE sopapo;')
    print("Banco de dados 'sopapo' criado com sucesso!")

    # Fechar conexão com o banco de dados
    cursor.close()
    connect_db.close()

def create_table():
    # Conecta ao banco de dados que foi criado ('sopapo')
    connect_db = psycopg2.connect(
        dbname='sopapo', user='postgres', password='mysenha', host='localhost', port='5432'
    )

    cursor = connect_db.cursor()

    # Criando as tabelas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rooms (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            room_id INTEGER REFERENCES rooms(id),
            user_id INTEGER REFERENCES users(id),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    print('Tabelas criadas com sucesso')

    # Salvar as alterações
    connect_db.commit()

    # Fechar conexão com o banco de dados
    cursor.close()
    connect_db.close()

if __name__ == '__main__':
    create_db()    # Criar banco de dados
    create_table()  # Criar tabelas
