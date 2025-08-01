import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
import atexit
import json

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloco de Notas")
        self.root.geometry("800x600")
        
        # Configuração do arquivo temporário
        self.temp_file = "/tmp/notepad_temp.txt"
        # Arquivo de configuração para histórico
        self.config_file = os.path.expanduser("~/.notepad_config")
        
        # Configuração inicial da fonte
        self.current_font = font.Font(family="Arial", size=12)
        
        # Widget de texto
        self.text_area = tk.Text(
            self.root,
            wrap="word",
            undo=True,
            font=self.current_font
        )
        self.text_area.pack(expand=True, fill="both")
        
        # Barra de rolagem
        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side="right", fill="y")
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=scrollbar.set)
        
        # Variável para o arquivo atual
        self.current_file = None
        
        # Carregar arquivo temporário se existir
        self.load_temp_file()
        
        # Carregar último arquivo aberto, se existir
        self.load_last_file()
        
        # Configurar atalhos
        self.setup_shortcuts()
        
        # Registrar função para salvar ao sair
        atexit.register(self.save_temp_on_exit)
        atexit.register(self.save_last_file_on_exit)
    
    def load_temp_file(self):
        if os.path.exists(self.temp_file):
            try:
                with open(self.temp_file, "r") as f:
                    content = f.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
            except:
                pass  # Se der erro, ignora e começa vazio
    
    def save_temp_on_exit(self):
        try:
            with open(self.temp_file, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))
        except:
            pass  # Se não conseguir salvar, não faz nada
    
    def setup_shortcuts(self):
        # Atalhos de arquivo
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_as())
        self.root.bind("<Control-p>", lambda e: self.print_file())
        
        # Atalhos de edição
        self.root.bind("<Control-z>", lambda e: self.text_area.edit_undo())
        self.root.bind("<Control-y>", lambda e: self.text_area.edit_redo())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        self.root.bind("<Control-v>", self.custom_paste)
        
        # Zoom com Ctrl + Scroll (funciona no Linux)
        self.root.bind("<Control-4>", lambda e: self.zoom_font(1))   # Scroll Up
        self.root.bind("<Control-5>", lambda e: self.zoom_font(-1))  # Scroll Down
    
    def zoom_font(self, direction):
        """Aumenta/diminui a fonte com base na direção (+1 = aumenta, -1 = diminui)."""
        current_size = self.current_font["size"]
        if direction > 0:
            new_size = current_size + 1
        else:
            new_size = max(8, current_size - 1)  # Mínimo de tamanho 8
        self.current_font.configure(size=new_size)
    
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
    
    def load_last_file(self):
        """Carrega o último arquivo aberto, se existir no config."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    last_file = config.get("last_file")
                    if last_file and os.path.exists(last_file):
                        with open(last_file, "r") as file:
                            self.text_area.delete(1.0, tk.END)
                            self.text_area.insert(1.0, file.read())
                        self.current_file = last_file
            except Exception:
                pass

    def save_last_file_on_exit(self):
        """Salva o caminho do último arquivo aberto no config."""
        try:
            with open(self.config_file, "w") as f:
                json.dump({"last_file": self.current_file}, f)
        except Exception:
            pass

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Textos", "*.txt"), ("Todos", "*.*")])
        if file_path:
            with open(file_path, "r") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, f.read())
            self.current_file = file_path
            self.save_last_file_on_exit()  # Salva imediatamente ao abrir

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))
            self.save_last_file_on_exit()  # Salva imediatamente ao salvar
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textos", "*.txt"), ("Todos", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))
            self.current_file = file_path
            self.save_last_file_on_exit()  # Salva imediatamente ao salvar como

    def print_file(self):
        messagebox.showinfo("Imprimir", "Funcionalidade de impressão simulada.")
    
    def select_all(self):
        self.text_area.tag_add("sel", "1.0", tk.END)
        return "break"  # Evita comportamento padrão

    def custom_paste(self, event=None):
        try:
            # Se houver seleção, apaga antes de colar
            if self.text_area.tag_ranges("sel"):
                self.text_area.delete("sel.first", "sel.last")
            self.text_area.insert(tk.INSERT, self.root.clipboard_get())
            return "break"  # Impede o comportamento padrão
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
