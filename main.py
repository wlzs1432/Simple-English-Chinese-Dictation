import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter import ttk
import sqlite3
import random


def connect_db():
    return sqlite3.connect('words.db')


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        english TEXT NOT NULL,
        chinese TEXT NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """)
    conn.commit()
    conn.close()


def create_category():
    category_name = simpledialog.askstring("创建类别", "请输入类别名称：")
    if category_name:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO categories (name) 
        VALUES (?)""", (category_name,))
        conn.commit()
        conn.close()
        messagebox.showinfo("成功", f"类别 '{category_name}' 创建成功！")
        refresh_category_list()


def add_word_to_category(category_id):
    english = simpledialog.askstring("添加单词", "请输入英文单词：")
    chinese = simpledialog.askstring("添加单词", "请输入中文翻译：")
    if not english or not chinese:
        messagebox.showwarning("输入错误", "请填写完整的单词和翻译")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO words (english, chinese, category_id) 
    VALUES (?, ?, ?)""", (english, chinese, category_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("成功", f"已将 '{english}' 添加到类别 ID {category_id} 中")
    refresh_category_list()


def refresh_category_list():
    for row in category_treeview.get_children():
        category_treeview.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()
    for category in categories:
        category_treeview.insert('', 'end', values=(category[0], category[1]))


def view_category_words(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE category_id = ?", (category_id,))
    words = cursor.fetchall()
    conn.close()

    word_list_window = tk.Toplevel()
    word_list_window.title(f"类别 ID {category_id} 下的单词")

    word_treeview = ttk.Treeview(word_list_window, columns=("ID", "English", "Chinese"), show="headings")
    word_treeview.heading("ID", text="ID")
    word_treeview.heading("English", text="英文单词")
    word_treeview.heading("Chinese", text="中文翻译")

    for word in words:
        word_treeview.insert('', 'end', values=(word[0], word[1], word[2]))

    word_treeview.pack(padx=10, pady=10)

    def refresh_words():
        refresh_category_words(category_id, word_treeview)

    refresh_button = tk.Button(word_list_window, text="手动刷新",
                               command=refresh_words)
    refresh_button.pack(pady=10)

    add_word_button = tk.Button(word_list_window, text="添加单词",
                                command=lambda: add_word_to_category(category_id))
    add_word_button.pack(pady=10)

    generate_test_button = tk.Button(word_list_window, text="生成测试题",
                                     command=lambda: generate_test(category_id))
    generate_test_button.pack(pady=10)


def refresh_category_words(category_id, word_treeview):
    for row in word_treeview.get_children():
        word_treeview.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE category_id = ?", (category_id,))
    words = cursor.fetchall()
    conn.close()
    for word in words:
        word_treeview.insert('', 'end', values=(word[0], word[1], word[2]))


def generate_test(category_id):
    num_questions = simpledialog.askinteger("生成测试题", "请输入需要的测试题数量：", minvalue=1)
    if not num_questions:
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE category_id = ?", (category_id,))
    words = cursor.fetchall()
    conn.close()
    if len(words) < num_questions:
        messagebox.showwarning("单词不足", "该类别下的单词不足，无法生成所需数量的测试题！")
        return
    selected_words = random.sample(words, num_questions)

    question_index = [0]

    def show_next_question():
        if question_index[0] >= len(selected_words):
            messagebox.showinfo("完成", "所有问题已完成！")
            return

        word = selected_words[question_index[0]]
        question = f"{word[1]} -> ?"
        answer = word[2]

        test_window = tk.Toplevel()
        test_window.title("测试题")

        question_label = tk.Label(test_window, text=question, font=('Arial', 14))
        question_label.pack(pady=10)

        answer_entry = tk.Entry(test_window, font=('Arial', 14))
        answer_entry.pack(pady=10)

        def check_answer():
            user_answer = answer_entry.get().strip()
            if user_answer == answer:
                messagebox.showinfo("正确", "回答正确！")
            else:
                messagebox.showerror("错误", f"错误，正确答案是：{answer}")

            question_index[0] += 1
            test_window.destroy()
            show_next_question()

        submit_button = tk.Button(test_window, text="提交", font=('Arial', 14), command=check_answer)
        submit_button.pack(pady=10)

    show_next_question()


def create_main_window():
    window = tk.Tk()
    window.title("简易中英听写器")

    tk.Button(window, text="创建类别", command=create_category).pack(padx=10, pady=10)

    global category_treeview
    category_treeview = ttk.Treeview(window, columns=("ID", "Category"), show="headings")
    category_treeview.heading("ID", text="ID")
    category_treeview.heading("Category", text="类别")
    category_treeview.pack(padx=10, pady=10)

    category_treeview.bind("<Double-1>", lambda event: on_category_select(event))

    refresh_category_list()

    window.mainloop()


def on_category_select(event):
    selected_item = category_treeview.selection()
    category_id = category_treeview.item(selected_item)['values'][0]
    view_category_words(category_id)


create_table()
create_main_window()
