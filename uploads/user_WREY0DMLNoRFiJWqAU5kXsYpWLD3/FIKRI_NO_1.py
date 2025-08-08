buah_list = []

for i in range(5):
    buah =input(f"Masukkan Nama Buah ke -{i+1}:")
    buah_list.append(buah)

buah_tuple = tuple(buah_list)

cari = input("Masukkan nama buah yang ingin di cari:")

if cari in buah_tuple:
    print("buah {cari} Ada di dalam Tuple.")

else:
    print("Buah {cari} tidak ada di dalam tuple.")

print("menampilkan jumlah kemunculan setiap buah:")

for buah in set(buah_tuple):
    print(f"{buah}:{buah_tuple.count(buah)} kali")