import sqlite3
import os

def create_database():
    # Conectar ao banco de dados (cria se não existir)
    conn = sqlite3.connect('queez.db')
    cursor = conn.cursor()
    
    # Script SQL completo
    sql_script = """
-- Tabela de Quizzes
CREATE TABLE IF NOT EXISTS Quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL CHECK (type IN ('python', 'personalidade', 'tecnologias'))
);

-- Tabela de Perguntas
CREATE TABLE IF NOT EXISTS Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('python', 'js', 'sql', 'html', 'carreira', 'pessoal'))
);

-- Tabela de Respostas
CREATE TABLE IF NOT EXISTS Answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT 0,
    personality_value VARCHAR(50) NULL,
    FOREIGN KEY (question_id) REFERENCES Questions(id) ON DELETE CASCADE
);

-- Tabela de Relacionamento Quiz-Perguntas
CREATE TABLE IF NOT EXISTS Quiz_Questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    question_order INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Questions(id) ON DELETE CASCADE,
    UNIQUE(quiz_id, question_id, question_order)
);

-- Tabela de Jogadores
CREATE TABLE IF NOT EXISTS Players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Pontuações
CREATE TABLE IF NOT EXISTS Player_Scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(id) ON DELETE CASCADE
);

-- Inserir os 3 tipos de quizzes
INSERT INTO Quizzes (title, description, type) VALUES 
('Quiz Python', 'Teste seus conhecimentos em Python', 'python'),
('Teste de Personalidade', 'Descubra seu perfil na TI', 'personalidade'),
('Quiz de Tecnologias', 'Conhecimentos gerais em programação', 'tecnologias');
    """
    
    try:
        # Executar o script completo
        cursor.executescript(sql_script)
        conn.commit()
        print("✅ Banco de dados criado com sucesso!")
        print("📊 Tabelas: Quizzes, Questions, Answers, Quiz_Questions, Players, Player_Scores")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()