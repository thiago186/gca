import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
version = 1.0

class gca():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Teste')
        self.root.geometry('1080x720')
        self.mainframe = tk.Frame(self.root)
        self.mainframe.pack(fill = 'both', expand = True)
        self.text1 = ttk.Label(self.mainframe, text = f"GCA-v{version}")
        self.text1.grid(row = 0, column = 1)

        self.movimentacoes_file_text = ttk.Label(self.mainframe, text = 'Caminho do arquivo de movimentações B3: ')
        self.movimentacoes_file_text.grid(row = 3, column =0)
        self.movimentacoes_file_dir = ttk.Label(self.mainframe, text= 'Selecione o Arquivo')
        self.movimentacoes_file_dir.grid(row= 3, column= 1)
        self.get_movimentacoes_file_button = ttk.Button(self.mainframe, text = 'Selecionar Arquivo', command=self.get_mov_file)
        self.get_movimentacoes_file_button.grid(row = 3, column =2)

        self.root.mainloop()
        return
    
    def get_files(self):
        files = filedialog.askopenfilenames(title = 'GCA - Importar Arquivos')
        return files

    def get_mov_file(self):
        file = filedialog.askopenfilename(title = 'GCA - Importar Arquivo de Movimentacoes B3')
        self.movimentacoes_file_dir.config(text = file)
        return file



if __name__ == '__main__':
    gca()