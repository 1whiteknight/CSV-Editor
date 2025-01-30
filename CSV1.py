import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import csv
import os


class CSVEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        self.root.geometry("800x600")

        # Scrollbars
        self.canvas = tk.Canvas(self.root)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.columns = []  # Spaltennamen
        self.data = []  # Datenzeilen
        self.filepath = ""  # Dateipfad

        self.create_menu()
        self.ask_for_file()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Neues CSV erstellen", command=self.create_new_csv)
        file_menu.add_command(label="CSV laden", command=self.load_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.exit_program)

    def ask_for_file(self):
        choice = messagebox.askquestion("CSV Datei",
                                        "Möchten Sie eine neue CSV Datei erstellen oder eine bestehende laden?",
                                        icon='question')
        if choice == 'yes':
            self.create_new_csv()
        else:
            self.load_csv()

    def create_new_csv(self):
        file_name = simpledialog.askstring("Dateiname", "Wie soll die Datei heißen?", parent=self.root)
        if not file_name:
            return

        # Dateipfad speichern
        self.filepath = os.path.join(os.getcwd(), f"{file_name}.csv")

        # Anzahl der Eingabefelder
        num_fields = simpledialog.askinteger("Anzahl der Felder", "Wie viele Felder soll die Datei haben?",
                                             parent=self.root)
        if not num_fields:
            return

        self.columns = []
        for i in range(num_fields):
            col_name = simpledialog.askstring(f"Spalte {i + 1}",
                                              f"Geben Sie den Namen der Spalte {i + 1} ein (oder lassen Sie es leer):",
                                              parent=self.root)
            self.columns.append(col_name if col_name else f"Spalte {i + 1}")

        self.create_column_entries()

    def create_column_entries(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.entries = []
        for idx, col_name in enumerate(self.columns):
            label = tk.Label(self.frame, text=col_name)
            label.grid(row=0, column=idx, padx=5, pady=5)
            entry = tk.Entry(self.frame)
            entry.grid(row=1, column=idx, padx=5, pady=5)
            self.entries.append(entry)

        save_button = tk.Button(self.frame, text="Speichern", command=self.save_csv)
        save_button.grid(row=2, columnspan=len(self.columns), pady=10)

    def save_csv(self):
        data = []
        for entry in self.entries:
            data.append(entry.get())

        if os.path.exists(self.filepath):
            with open(self.filepath, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        else:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.columns)  # Header
                writer.writerow(data)

        messagebox.showinfo("Erfolg", "CSV-Datei wurde gespeichert.")
        self.load_csv()

    def load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV-Dateien", "*.csv")])
        if not filepath:
            return

        self.filepath = filepath
        self.columns = []
        self.data = []

        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.columns = next(reader)
            self.data = list(reader)

        self.create_table()

    def create_table(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Tabelle mit Header und Daten
        self.entries = []
        for idx, col_name in enumerate(self.columns):
            label = tk.Label(self.frame, text=col_name)
            label.grid(row=0, column=idx, padx=5, pady=5)

        for row_idx, row_data in enumerate(self.data, start=1):
            for col_idx, col_data in enumerate(row_data):
                entry = tk.Entry(self.frame)
                entry.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                entry.insert(tk.END, col_data)
                self.entries.append(entry)

        add_row_button = tk.Button(self.frame, text="Neue Zeile hinzufügen", command=self.add_row)
        add_row_button.grid(row=len(self.data) + 1, columnspan=len(self.columns), pady=10)

        save_button = tk.Button(self.frame, text="Speichern", command=self.save_csv)
        save_button.grid(row=len(self.data) + 2, columnspan=len(self.columns), pady=10)

    def add_row(self):
        row_idx = len(self.data) + 1
        self.data.append([""] * len(self.columns))

        for col_idx in range(len(self.columns)):
            entry = tk.Entry(self.frame)
            entry.grid(row=row_idx, column=col_idx, padx=5, pady=5)
            self.entries.append(entry)

    def exit_program(self):
        if messagebox.askyesno("Beenden", "Möchten Sie die Datei vor dem Beenden speichern?", parent=self.root):
            self.save_csv()
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditorApp(root)
    root.mainloop()
