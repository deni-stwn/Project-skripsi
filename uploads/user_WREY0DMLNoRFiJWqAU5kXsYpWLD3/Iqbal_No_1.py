buah_tuple = tuple (input("masukan nama buah ke-{i+1}:") for i in range(5))
print("tuple buah :", buah_tuple)

cari = input("masukan buah yang ingin dicari:")
if cari in buah_tuple: 
    print(f"{cari} di temukan dalam tuple.")
else: 
    print(f"{buah} :tidak diteukan dalam tuple")

print("\njumlah kemunculan setiap buah ")
for buah in set(buah_tuple):
    print(f"{buah} :{buah_tuple.count(buah)}")