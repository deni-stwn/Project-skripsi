list_buah=[]
for i in range(5):
    buah = input(f"Masukkan Nama Buah ke -{i+1}:").strip().lower()
    list_buah.append(buah)

    tuple_buah= tuple(list_buah)

    print("\nTuple Buah :",tuple_buah)

    cari_buah= input("Masukkan Nama Buah yang Ingin Dicari : ").strip().lower()
    if cari_buah in tuple_buah:
        print(f"Buah'{cari_buah}' ada dalam tuple")
    else:
        print(f"Buah'{cari_buah}' tidak ada dalam tuple")

print("\nJumlah Kemunculan Tiap Buah:")
for buah in set(tuple_buah):
    print(f"-{buah}:{tuple_buah.count(buah)}kali")