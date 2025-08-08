list_buah = []
for i in range(5):
    buah = input(f"masukan nama buah ke -{i+1}:").strip().lower()
    list_buah.append(buah)
    
    tuple_buah = tuple(list_buah)
    
    print("\nTuple buah :",tuple_buah)
    
    cari_buah = input("masukan nama buah yang ingin di cari :").strip().lower()
    if cari_buah in tuple_buah:
        print(f"Buah '{cari_buah}'ada dalam tuple.")
    else:
        print(f"Buah'{cari_buah}'tidak ada dalam taple.")
        
print("\nJumlah Kemunculan Tiap Buah :")
for buah in set(tuple_buah):
    print(f"-{buah}:{tuple_buah.count(buah)}kali")



