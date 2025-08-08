buah_list = []
for i in range(10):
    buah = input(f"Masukkan nama buah ke-{i+1}: ")
    buah_list.append(buah)

buah_tuple = tuple(buah_list)

print("\nTuple buah yaang dimasukkan:")
print(buah_tuple)

cari_buah = input("\nMasukkan nama buah yang dicari: ")

if cari_buah in buah_tuple:
    print(f"{cari_buah} ada di dalam tuple.")
else:
    print(f"{cari_buah} tidak ditemukan dalam tuple.")

print("\nJumlah kemunculan setiap buah:")
for buah in set(buah_tuple):
    print(f"{buah}: {buah_tuple.count(buah)} kali")        
