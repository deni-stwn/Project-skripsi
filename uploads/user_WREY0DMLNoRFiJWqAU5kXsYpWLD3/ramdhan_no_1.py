buah_list = []
for i in range(5):
    nama = input(f"masukan nama buah ke-{i+1}: ")
    buah_list.append(nama)
    
buah_tuple = tuple(buah_list)
print("isi tuple buah: ", buah_tuple)

buah_cari = input("masukan nama buah yang dicari: ")
if buah_cari in buah_tuple:
    print(f"buah {buah_cari} ada di dalam tuple. ")
else:
    print(f"buah {buah_cari} tidak ada di dalam tuple. ")
    
jumlah_buah = {}
for buah in buah_tuple:
    if buah in jumlah_buah:
        jumlah_buah[buah] += 1
    else:
        jumlah_buah[buah] = 1
        
print("jumlah setiap buah: ")
for kunci, nilai in jumlah_buah.items():
    print(f"{kunci} : {nilai} kali")