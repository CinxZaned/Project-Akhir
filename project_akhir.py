class Mhs_info:
    def __init__(self, nim, nama, tgl_lahir, ipk):
        self.nim = nim
        self.nama = nama
        self.tgl_lahir = tgl_lahir
        self.ipk = ipk

class Mhs_database:
    def __init__(self):
        self.data_mhs_all = []

    def insert_data(self, nim, nama, tgl_lahir, ipk):
        mhs = Mhs_info(nim, nama, tgl_lahir, ipk)
        self.data_mhs_all.append([mhs.nim, mhs.nama, mhs.tgl_lahir, mhs.ipk])

    def get_mhs_info(self, index):
        if 0 <= index < len(self.data_mhs_all):
            return self.data_mhs_all[index]
        else:
            print("Index out of range.")
            return None

    def get_nim(self, index):
        if 0 <= index < len(self.data_mhs_all):
            return self.data_mhs_all[index]
        else:
            print("Index out of range.")
            return None

    def display_data(self):
        print("NIM ------> Nama ------> Tanggal Lahir ------> IPK")
        for i, mhs in enumerate(self.data_mhs_all):
            nim, nama, tgl_lahir, ipk = mhs
            print(f"Student {i + 1}: NIM - {nim}, Name - {nama}, Birth Date - {tgl_lahir}, IPK - {ipk}")

mhs1 = Mhs_database()

def display_menu():
    print("Pilih Menu di bawah ini")
    print("1. Memasukkan data")
    print("2. Mencari data")
    print("3. Menghapus data")
    print("4. Exit")

while True:
    display_menu()
    menu = int



nim = int(input("Masukkan NIM: "))
nama = str(input("Masukkan Nama: "))
tgl_lahir = str(input("Masukkan Tanggal lahir (dd-mm-yyyy): "))
ipk = float(input("Masukkan IPK: "))

mhs1.insert_data(nim, nama, tgl_lahir, ipk)

mhs1.display_data()