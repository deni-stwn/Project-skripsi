buah_list = []

for i in range(5):
    buah = input (f"Masukan Nama Buah ke -{i+1}: ")
    buah_list.append(buah)
    
buah_tuple = tuple(buah_list)

cari = input("Masukan nama buah yang ingin di cari :")

if cari in buah_tuple :
    print("Buah {cari} ada di dalam Tuple. ")
    
else:
    print("Buah {cari} tidak ada di dalam tuple. ")
    
print("menampilkan jumlah kemunculan setiap buah :")

for i in set(buah_tuple):
    print(f"{buah}: {buah_tuple.count(buah)} kali")