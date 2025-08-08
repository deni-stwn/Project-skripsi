# Meminta pengguna memasukkan 5 nama buah
buah = tuple(input(f"Masukkan nama buah ke-{i+1}: ") for i in range(5))

# Menampilkan tuple
print("\nTuple buah:", buah)

# Mencari buah
cari = input("\nMasukkan nama buah yang ingin dicari: ")
if cari in buah:
    print(f"Buah '{cari}' ada dalam tuple.")
else:
    print(f"Buah '{cari}' tidak ditemukan.")

# Menghitung dan menampilkan jumlah kemunculan setiap buah
print("\nJumlah kemunculan setiap buah:")
for item in set(buah):
    print(f"{item}: {buah.count(item)} kali")
