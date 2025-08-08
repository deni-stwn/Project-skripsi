buah_list = []
for i in range(5):
    nama = input(f"Masukkan nama buah ke-{i + 1}: ")
    buah_list.append(nama)

buah_tuple = tuple(buah_list)
print("Isi tuple buah:", buah_tuple)

buah_cari = input("Masukkan nama buah yang ingin dicari: ")
if buah_cari in buah_tuple:
    print(f"{buah_cari} ditemukan ada di dalam tuple. ")
else:
    print(f"{buah_cari} tidak ditemukan di dalam tuple. ")

jumlah_buah = {}
for buah in buah_tuple:
    if buah in jumlah_buah:
        jumlah_buah[buah] += 1
    else:
        jumlah_buah[buah] = 1

print("Jumlah setiap buah:")
for kunci, nilai in jumlah_buah.items():
    print(f"{kunci} : {nilai} kali")