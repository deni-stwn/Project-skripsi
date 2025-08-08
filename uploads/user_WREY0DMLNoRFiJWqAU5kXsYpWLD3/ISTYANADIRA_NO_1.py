input_buah = []
for i in range(5):
    buah = input(f"Masukkan nama buah yang ke-{i+1}: ")
    input_buah.append(buah)

buah_tuple = tuple(input_buah)
print("\nTuple buah: ", buah_tuple)

cari_buah = input("\nMasukkan nama buah yang ingin di cari: ")

if cari_buah in buah_tuple:
    print(f"{cari_buah} ada di dalam tuple")
else:
    print(f"{cari_buah} tidak ada di dalam tuple")

print("\nJumlah kemunculan setiap buah: ")
count_data = {}
for item in buah_tuple:
    count_data[item] = count_data.get(item, 0) + 1

for key, value in count_data.items():
    print(f"{key}: {value} kali")