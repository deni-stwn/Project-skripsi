list_buah = []
for i in range(5):
    buah = input(f"Masukan nama buah ke -{i+1}:").strip().lower()
    list_buah.append(buah)
    
    tuple_buah = tuple(list_buah)
    
    print("\nTuple buah :",tuple_buah)
    
    cari_buah = input("\nMasukan nama buah yang ingin dicari :").strip().lower()
    
    if cari_buah in tuple_buah:
        print(f"Buah `{cari_buah}` ada dalam tuple. ")
    else:
        print(f"Buah `{cari_buah}` tidak ada dalam tuple.")
        
print("\nJumlah kemunculan tiap buah : ")
for buah in set(tuple_buah):
    print(f"- {buah}: {tuple_buah.count(buah)} kali")