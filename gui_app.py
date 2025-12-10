import tkinter as tk
from tkinter import scrolledtext, ttk, font
import threading
import sys
import queue

try:
    from main import main_assistant
except ImportError:
    print("ПОМИЛКА: Не можу знайти файл main.py або функцію main_assistant")
    print("Переконайтеся, що gui_app.py знаходиться в тій самій папці, що й main.py")
    sys.exit()


class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()


        self.log_queue = queue.Queue()


        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_header()
        self.setup_log_area()
        self.setup_status_bar()
        self.setup_buttons()


        self.check_log_queue()


        sys.stdout = self.RedirectText(self.log_queue)
        sys.stderr = self.RedirectText(self.log_queue)

    def setup_window(self):

        self.root.title("Голосовий Асистент: Том і Джері")
        self.root.geometry("700x550")
        self.root.configure(bg="#2E2E2E")


        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="white")


        style.configure("TButton", background="#4A90E2", foreground="white", font=('Arial', 10, 'bold'))
        style.map("TButton", background=[('active', '#357ABD')])


        style.configure("Stop.TButton", background="#E24A4A", foreground="white", font=('Arial', 10, 'bold'))
        style.map("Stop.TButton", background=[('active', '#C0392B')])

    def setup_header(self):

        header_font = font.Font(family="Arial", size=16, weight="bold")
        header_label = ttk.Label(self.main_frame, text="Асистент 'Том і Джері'", font=header_font)
        header_label.pack(pady=(10, 20))

    def setup_log_area(self):

        log_frame = ttk.Frame(self.main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            bg="#1C1C1C",
            fg="white",
            font=("Consolas", 10),
            insertbackground="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.configure(state='disabled')

    def setup_status_bar(self):

        self.status_var = tk.StringVar()
        self.status_var.set("Готовий до запуску...")
        status_label = ttk.Label(self.main_frame, textvariable=self.status_var, font=("Arial", 9))
        status_label.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=(5, 0))

    def setup_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(10, 10))

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.start_button = ttk.Button(
            button_frame,
            text="Запустити Асистента",
            command=self.start_assistant_thread
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.stop_button = ttk.Button(
            button_frame,
            text="Зупинити Асистента",
            command=self.stop_assistant,
            state=tk.DISABLED,
            style="Stop.TButton"
        )
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def start_assistant_thread(self):

        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.status_var.set("Асистент запускається...")


        self.assistant_thread = threading.Thread(
            target=main_assistant,
            daemon=True
        )
        self.assistant_thread.start()

    def stop_assistant(self):

        print("--- Завершення роботи на запит користувача ---")
        self.root.destroy()

    def add_log_message(self, message):

        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message)
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')


        if "🎤" in message:
            self.status_var.set("Говоріть зараз...")
        elif "🧠" in message:
            self.status_var.set("Розпізнавання...")
        elif "🔊" in message:
            self.status_var.set("Асистент говорить...")

    def check_log_queue(self):

        try:
            while True:

                message = self.log_queue.get_nowait()
                self.add_log_message(message)
        except queue.Empty:
            pass


        self.root.after(100, self.check_log_queue)

    class RedirectText:


        def __init__(self, queue):
            self.queue = queue

        def write(self, text):
            self.queue.put(text)

        def flush(self):

            pass



if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantGUI(root)

    root.protocol("WM_DELETE_WINDOW", app.stop_assistant)

    root.mainloop()