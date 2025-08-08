buah_list = []
for i in range(10) :
    nama = input(f" Masukkan nama buah ke-{i+1}:")
    buah_list.append(nama)

buah_tuple = tuple(buah_list)
print("isi dari tuple buah :", buah_tuple)

buah_cari = input("Masukkan nama buah yang akan dicari: ")
if buah_cari in buah_tuple:
    print(f"{buah_cari} ada dan ditemukan didalam tuple")
else :
    print(f"{buah_cari} tidak ditemukan dan tidak ada didalam tuple")

jumlah_buah ={}
for buah in buah_tuple:
    if buah in jumlah_buah :
        jumlah_buah[buah] += 1
    else :
        jumlah_buah[buah] =1

print("jumlah per buah :")
for kunci, nilai in jumlah_buah.items() :
    print(f"{kunci} : {nilai} kali")