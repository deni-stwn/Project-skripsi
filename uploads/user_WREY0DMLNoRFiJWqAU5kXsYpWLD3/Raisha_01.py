# 1. operasi pada tuple

list_buah = ("mangga", "anggur", "apel"," jeruk", "durian")
tuple_buah = tuple(list_buah)
print(tuple_buah)

cari = input("Masukkan buah yang ingin dicari: ")
if cari in tuple_buah:
    print(f"Buah ada didalam tuple")
else:
    print(f"Buah tidak ditemukan !!")
    
print(f"Jumlah kemunculan setiap buah dalam tuple: ")
for buah in set(tuple_buah):
    print(buah, ":", tuple_buah.count(buah))