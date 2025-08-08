buah_list = []

for i in range(5):
    buah = input('Masukkan Nama Buah: ')
    buah_list.append(buah)
    
buah_tuple = tuple(buah_list)

print('Daftar Buah:', buah_tuple)

cari_buah = input('Masukkan Nama Buah yang dicari: ')
if cari_buah in buah_tuple:
    print(f'{cari_buah} ada di dalam tuple')
else:
    print(f'{cari_buah} tidak ada di dalam tuple')
    
print('jumlah kemunculan setiap buah:')
for buah in set(buah_tuple):
    print(f'{buah}: {buah_tuple.count(buah)} kali')