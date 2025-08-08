buah = input("Masukan 5 nama buah dan pisah dengan tanda koma ',': ")
tup_buah = tuple(buah.split(","))
print(tup_buah)
cari_buah = input("Masukan nama buah yang ingin kamu cari: ")
if cari_buah in tup_buah:
    print("Buah %s ada pada tuple diatas"%(cari_buah))
else:"Buah %s yang kamu cari tidak ada dalam tuple"

#lupa mengerjakan bagian ini lalu baru ditambahkan saat selesai record codingan ini menyontek dari blackbox ai
count_data = {}
for item in tup_buah:
    count_data[item] = count_data.get(item,0) + 1

for key,value in count_data.items():
    print(f'{key}: {value} kali')