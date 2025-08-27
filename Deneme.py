
with open("tdk_fark_zemberek.txt", 'r') as input_file:
    dosya_icerigi = input_file.read()
    dosya_icerigi = dosya_icerigi.replace('-', '')
    dosya_icerigi = dosya_icerigi.replace('Ã¢', 'a')
    dosya_icerigi = dosya_icerigi.replace('Ã®', 'i')
    dosya_icerigi = dosya_icerigi.replace('Ã»', 'u')
    dosya_icerigi = dosya_icerigi.replace('Ä±', 'ı')
    dosya_icerigi = dosya_icerigi.replace('ÄŸ', 'ğ')
    dosya_icerigi = dosya_icerigi.replace('Ã¼', 'ü')
    dosya_icerigi = dosya_icerigi.replace('ÅŸ', 'ş')
    dosya_icerigi = dosya_icerigi.replace('Ã¶', 'ö')
    dosya_icerigi = dosya_icerigi.replace('Ã§', 'ç')

kelime_listesi = dosya_icerigi.split()

bes_harfli_kelimeler = []

for i in kelime_listesi:
    if len(i) == 5:
        bes_harfli_kelimeler.append(i)

print(len(kelime_listesi), len(bes_harfli_kelimeler))

dosya = open("5 harfli_zemberek.txt", "w")
for i in bes_harfli_kelimeler:
    dosya.writelines(i + "\n")

with open("aa.txt", 'r') as file:
    dosya = file.read()

print(dosya)
