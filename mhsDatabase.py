import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class MhsDatabase:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x400')
        self.root.title('Mahasiswa Database')

        # Button widgets instead of a menu
        self.input_btn = tk.Button(root, text="Input Data", command=self.input_window)
        self.input_btn.pack(pady=5, ipadx=3, ipady=3)

        self.delete_btn = tk.Button(root, text="Delete Data", command=self.delete_data)
        self.delete_btn.pack(pady=5, ipadx=3, ipady=3)

        self.placeholder_text = "Search data here"

        self.txt_search = tk.Entry(root, width=25)
        self.txt_search.insert(0, self.placeholder_text)   
        self.txt_search.config(fg="grey")  # Set initial text color to grey
        self.txt_search.bind("<FocusIn>", self.on_entry_click)
        self.txt_search.bind("<FocusOut>", self.on_focus_out)
        self.txt_search.bind("<Return>", lambda event: self.search_data())
        self.txt_search.pack(padx=25, ipadx=1, ipady=1, anchor='se')

        self.tree = ttk.Treeview(self.root, columns=('nim', 'nama', 'tanggal lahir', 'ipk'), show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        self.tree.column('nim', anchor='w', width=90, minwidth=85)
        self.tree.column('nama', anchor='w', width=110, minwidth=95)
        self.tree.column('tanggal lahir', anchor='w', width=90, minwidth=85)
        self.tree.column('ipk', anchor='w', width=50, minwidth=40)

        self.sort_order = {'nim': False, 'nama': False, 'tanggal lahir': False, 'ipk': False}

        self.tree.heading('nim', text='NIM', command=lambda: self.on_heading_click('nim'))
        self.tree.heading('nama', text='Nama', command=lambda: self.on_heading_click('nama'))
        self.tree.heading('tanggal lahir', text='Tanggal Lahir', command=lambda: self.on_heading_click('tanggal lahir'))
        self.tree.heading('ipk', text='IPK', command=lambda: self.on_heading_click('ipk'))

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        # Configure the Treeview to use the scrollbar
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_btn = tk.Button(root, text="Refresh", command=self.refresh_db)
        self.refresh_btn.pack(padx=10, pady=5, anchor="sw")

    def fetch_data(self):
        if not self.tree.get_children():
            self.fd = False
        if self.fd == False:
            self.input_wd.destroy()
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='mahasiswa'
                )

                cursor = conn.cursor()
                cursor.execute("SELECT * FROM data_mhs")
                self.rows = cursor.fetchall()

                for row in self.rows:
                    # Convert the date to a datetime object and format it
                    formatted_date = str(row[2]).split()[0]
                    # Replace the original date in the row with the formatted date
                    row = row[:2] + (formatted_date,) + row[3:]
                    self.tree.insert('', 'end', values=row)

                conn.close()
            except mysql.connector.Error as e:
                print(f"Error connecting to MySQL: {e}")
            self.fd = True
        else:
            messagebox.showwarning("Warning", "Data from the database has already inputted!")
    
    def refresh_db(self):
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "Database is empty!")
        else:
            self.tree.delete(*self.tree.get_children())
            self.fetch_data()
        pass

    def on_heading_click(self, column):
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "Database is empty!")
        else:
            self.all_items = self.tree.get_children()
            self.data_to_sort = [self.tree.item(item)['values'] for item in self.all_items]
            current_order = self.sort_order[column]
            # Sort data based on the column clicked
            self.tree.delete(*self.tree.get_children())
            if not current_order:
                self.sort_data(column, reverse=False)
                self.sort_order[column] = True
            else:
                self.sort_data(column, reverse=True)
                self.sort_order[column] = False

            for row in self.data_to_sort:
                self.tree.insert("", "end", values=row)

    def get_column_index(self, column_name):
        # Get the index of the column in the data
        column_index = {'nim': 0, 'nama': 1, 'tanggal lahir': 2, 'ipk': 3}
        return column_index[column_name]

    def on_entry_click(self, event):
        if self.txt_search.get() == self.placeholder_text:
            self.txt_search.delete(0, "end")
            self.txt_search.config(fg="black")  # Change text color to black

    def on_focus_out(self, event):
        if self.txt_search.get() == "":
            self.txt_search.insert(0, self.placeholder_text)
            self.txt_search.config(fg="grey")

    def input_window(self):
        self.input_wd = tk.Toplevel(self.root)
        self.input_wd.geometry('150x100')
        self.input_wd.title("Input Data")

        self.input_btn = tk.Button(self.input_wd, text="Input Database", command=self.fetch_data)
        self.input_btn.pack(pady=5, ipadx=3, ipady=3)

        self.input_btn2 = tk.Button(self.input_wd, text="Input Data Manually", command=self.input_manually_window)
        self.input_btn2.pack(pady=5, ipadx=3, ipady=3)

    def input_manually_window(self):
        self.input_wd.destroy()

        self.input_manual = tk.Toplevel(self.root)
        self.input_manual.geometry('240x400')
        self.input_manual.title("Input Data Manually")

        #title label
        self.title_lbl = tk.Label(self.input_manual, text="INPUT DATA MANUALLY", font=("Family", 10, "bold"))
        self.title_lbl.pack(pady=10)

        #nim
        self.nim_lbl = tk.Label(self.input_manual, text="NIM")
        self.nim_lbl.pack()

        self.nim_txt = tk.Entry(self.input_manual, width=25, justify="center")
        self.nim_txt.pack(pady=5)

        self.nim_lbl = tk.Label(self.input_manual)
        self.nim_lbl.pack()

        #nama
        self.nama_lbl = tk.Label(self.input_manual, text="Nama")
        self.nama_lbl.pack()

        self.nama_txt = tk.Entry(self.input_manual, width=25, justify="center")
        self.nama_txt.pack(pady=5)

        self.nama_lbl = tk.Label(self.input_manual)
        self.nama_lbl.pack()
        
        #tanggal lahir
        self.placeholder_tgl = "YYYY-MM-DD"

        self.tgl_lbl = tk.Label(self.input_manual, text="Tanggal Lahir")
        self.tgl_lbl.pack()

        self.tgl_txt = tk.Entry(self.input_manual, width=25, justify="center")
        self.tgl_txt.pack(pady=5)

        self.tgl_lbl = tk.Label(self.input_manual)
        self.tgl_lbl.pack()

        self.tgl_txt.insert(0, self.placeholder_tgl)
        self.tgl_txt.config(fg="grey")  # Set initial text color to grey
        self.tgl_txt.bind("<FocusIn>", self.on_entry_click_tgl)
        self.tgl_txt.bind("<FocusOut>", self.on_focus_out_tgl)

        #ipk
        self.ipk_lbl = tk.Label(self.input_manual, text="IPK")
        self.ipk_lbl.pack()

        self.ipk_txt = tk.Entry(self.input_manual, width=25, justify="center")
        self.ipk_txt.pack(pady=5)

        self.ipk_lbl = tk.Label(self.input_manual)
        self.ipk_lbl.pack()

        #input button
        self.input_dat_btn = tk.Button(self.input_manual, text="Input Data", command=self.input_data)
        self.input_dat_btn.pack(ipadx=3, ipady=3)

    def on_entry_click_tgl(self, event):
        if self.tgl_txt.get() == self.placeholder_tgl:
            self.tgl_txt.delete(0, "end")
            self.tgl_txt.config(fg="black")  # Change text color to black

    def on_focus_out_tgl(self, event):
        if self.tgl_txt.get() == "":
            self.tgl_txt.insert(0, self.placeholder_tgl)
            self.tgl_txt.config(fg="grey")

    def input_data(self):
        nim = self.nim_txt.get()
        nama = self.nama_txt.get()
        tgl = self.tgl_txt.get()
        ipk = self.ipk_txt.get()
        data = (nim, nama, tgl, ipk)
        if len(nim) != 11:
            messagebox.showwarning("Warning", "NIM must be 11 digits!")
        else:
            self.tree.insert('', 'end', values=data)
            messagebox.showwarning("Status", "Data input was successful!")

    def binary_search(self, tree, value, column):
        self.all_items = self.tree.get_children()
        self.data_to_sort = [self.tree.item(item)['values'] for item in self.all_items]
        
        index = self.get_column_index(column)
        current_order = self.sort_order[column]

        self.tree.delete(*self.tree.get_children())

        if not current_order:
            self.sort_data(column, reverse=False)
        else:
            self.sort_data(column, reverse=False)

        for row in self.data_to_sort:
            self.tree.insert("", "end", values=row)

        items = tree.get_children()
        low, high = 0, len(items) - 1

        if self.tree.get_children():
            while low <= high:
                mid = (low + high) // 2
                mid_val = tree.item(items[mid], 'values')[index]
                if index == 1:
                    mid_val = mid_val.lower()
                
                if mid_val == value:
                    return items[mid]
                elif mid_val < value:
                    low = mid + 1
                else:
                    high = mid - 1
            return None
        else:
            return None

    def search_data(self):
        if not self.tree.get_children():
            messagebox.showwarning("Warning", "Database is empty!")
        elif self.txt_search.get() == "":
            messagebox.showwarning("Warning", "Please search the data using these formats:\nnim=12345678901\nnama=john baker\ntgl=yyyy-mm-dd\nipk=3.25")
        else:
            self.search_txt = self.txt_search.get()
            self.nim_opt = self.search_txt[0:4]
            self.nama_opt = self.search_txt[0:5]
            self.tgl_opt = self.search_txt[0:4]
            self.ipk_opt = self.search_txt[0:4]
            if self.nim_opt == "nim=":
                self.column = "nim"
                value = self.search_txt[4:]
                result = self.binary_search(self.tree, value, self.column)
                self.display_search_result(result)
            elif self.nama_opt == "nama=":
                self.column = "nama"
                value = self.search_txt[5:]
                result = self.binary_search(self.tree, value.lower(), self.column)
                self.display_search_result(result)
            elif self.tgl_opt == "tgl=":
                self.column = "tanggal lahir"
                value = self.search_txt[4:]
                result = self.binary_search(self.tree, value, self.column)
                self.display_search_result(result)
            elif self.ipk_opt == "ipk=":
                self.column = "ipk"
                value = self.search_txt[4:]
                result = self.binary_search(self.tree, value, self.column)
                self.display_search_result(result)
            else:
                messagebox.showwarning("Warning", "Incorrect format")
            
    def display_search_result(self, result):
        if result:
            # Display only the searched item
            values = self.tree.item(result, 'values')
            self.tree.delete(*self.tree.get_children())
            self.tree.insert('', 'end', values=values)
        else:
            messagebox.showwarning("Warning", "Data not found!")

    def delete_data(self):
        self.selected_items = self.tree.selection()
        for item in self.selected_items:
            self.tree.delete(item)

    def sort_data(self, column, reverse=False): #using selection sort
        index = self.get_column_index(column)
        n = len(self.data_to_sort)

        for i in range(n - 1):
            min_index = i
            for j in range(i + 1, n):
                if reverse:
                    if self.data_to_sort[j][index] > self.data_to_sort[min_index][index]:
                        min_index = j
                else:
                    if self.data_to_sort[j][index] < self.data_to_sort[min_index][index]:
                        min_index = j
            self.data_to_sort[i], self.data_to_sort[min_index] = self.data_to_sort[min_index], self.data_to_sort[i]

def main():
    root = tk.Tk()
    app = MhsDatabase(root)
    root.mainloop()

if __name__ == "__main__":
    main()
