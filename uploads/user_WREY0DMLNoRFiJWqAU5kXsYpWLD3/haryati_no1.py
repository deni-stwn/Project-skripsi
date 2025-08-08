buah_lits = []

for i in range(5):
    buah = input(f"masukan nama buah ke -{1+1}: ")
    buah_lits.append(buah)

    buah_tupla = tuple(buah_lits)

    cari = input("masukan nama buah yang ingin di cari :")

    if cari in buah_tupla :
        print("buah{cari} ada dalam tuple.")

    else:
        print("buah{cari} tidak ada dalam tuple.") 

    
    print("menampilkan jumlah kemunculan setiap buah :")

    for buah in set(buah_tupla) :
        print(f"{buah}: {buah_tupla.count(buah)} kali")
    
