# Meminta pengguna memasukkan 5 nama buah
buah = tuple(input(f"Masukkan nama buah ke-{i+1}: ") for i in range(5))

# Menampilkan tuple yang berisi nama buah
print("\nTuple buah yang dimasukkan:")
print(buah)

# Meminta pengguna memasukkan nama buah yang ingin dicari
buah_cari = input("\nMasukkan nama buah yang ingin dicari: ")

# Mengecek apakah buah yang dicari ada dalam tuple
if buah_cari in buah:
    print(f"{buah_cari} ada dalam tuple.")
else:
    print(f"{buah_cari} tidak ada dalam tuple.")

# Menghitung dan menampilkan jumlah kemunculan setiap buah dalam tuple
print("\nJumlah kemunculan setiap buah dalam tuple:")
for b in set(buah):  # Menggunakan set untuk memastikan nama buah tidak duplikat
    print(f"{b}: {buah.count(b)} kali")
