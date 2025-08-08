buah = tuple(input(f"Masukkan nama buah ke-{i+1}: ") for i in range(5))

print("Tuple buah:", buah)

cari = input("Masukkan nama buah yang ingin dicari: ")
if cari in buah:
    print(f"{cari} ada di dalam tuple.")
else:
    print(f"{cari} tidak ditemukan didalam tuple.")

print("Jumlah kemunculan setiap buah:")
for item in set(buah):
    print(f"{item}: {buah.count(item)} kali")