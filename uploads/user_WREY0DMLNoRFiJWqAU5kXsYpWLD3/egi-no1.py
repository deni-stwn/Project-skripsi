buah_list = []

for i in range(5): 
    buah = input(f"masukkan nama buah ke -{i+1}: ")
    buah_list.append(buah)
    
buah_tuple = tuple(buah_list)

cari = input("masukkan nama buah yang ingin diacari: ") 

if cari in buah_tuple:
    print(f"buah {cari} ada didalam tuple.")
else:
    print(f"buah {cari} tidak ada didalam tuple.")
print("menampilkan jumlah kemunculan setiap buah:")

for buah in set(buah_tuple):
    print(f"{buah}: {buah_tuple.count(buah)} kali")