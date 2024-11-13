import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('flash_brains.db')
cursor = conn.cursor()

# Criação da tabela de perguntas (caso não exista)
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_option INTEGER NOT NULL
)
''')
conn.commit()

# Função para inserir perguntas no banco de dados (apenas para testes iniciais)
def add_sample_questions():
    questions = [
        ("What is the capital of France?", "Berlin", "London", "Paris", "Madrid", 3),
        ("What is 2 + 2?", "3", "4", "5", "6", 2),
        ("What is the color of the sky?", "Blue", "Green", "Red", "Yellow", 1)
    ]
    cursor.executemany('''
    INSERT INTO questions (question, option1, option2, option3, option4, correct_option)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', questions)
    conn.commit()

# Descomente a linha abaixo para adicionar perguntas ao banco de dados na primeira vez que rodar o código
# add_sample_questions()

# Função para buscar uma pergunta aleatória do banco de dados
def get_random_question():
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    return cursor.fetchone()

# Lógica para verificar a resposta correta
def check_answer(selected_option):
    global current_question
    if selected_option == current_question[6]:  # Coluna da resposta correta é o índice 6
        messagebox.showinfo("Correct!", "You got it right!")
    else:
        messagebox.showerror("Incorrect", "That's not the right answer.")
    load_next_question()

# Função para carregar a próxima pergunta
def load_next_question():
    global current_question
    current_question = get_random_question()
    if current_question:
        question_label.config(text=current_question[1])
        option1_button.config(text=current_question[2], command=lambda: check_answer(1))
        option2_button.config(text=current_question[3], command=lambda: check_answer(2))
        option3_button.config(text=current_question[4], command=lambda: check_answer(3))
        option4_button.config(text=current_question[5], command=lambda: check_answer(4))
    else:
        messagebox.showinfo("End", "No more questions available!")

# Configuração da interface com Tkinter
root = tk.Tk()
root.title("Flash Brains")

# Elementos da interface
question_label = tk.Label(root, text="Question will appear here", font=("Arial", 14), wraplength=400)
question_label.pack(pady=20)

option1_button = tk.Button(root, text="Option 1", width=20)
option1_button.pack(pady=5)
option2_button = tk.Button(root, text="Option 2", width=20)
option2_button.pack(pady=5)
option3_button = tk.Button(root, text="Option 3", width=20)
option3_button.pack(pady=5)
option4_button = tk.Button(root, text="Option 4", width=20)
option4_button.pack(pady=5)

# Carrega a primeira pergunta
load_next_question()

# Inicia o loop principal da interface
root.mainloop()

# Fecha a conexão com o banco de dados ao encerrar o programa
conn.close()
