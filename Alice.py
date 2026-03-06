from collections import Counter

soubor = "alice.txt"

with open(soubor, "r", encoding="utf-8") as f:
    text = f.read()


slova = text.split()



pocet_slov = len(slova)
print("Počet slov:", pocet_slov)



cetnost_slov = Counter(slova)


print("Nejčastější slovo:", cetnost_slov.most_common(1))


sestnacte_slovo = cetnost_slov.most_common(16)[15]
print("16. nejčastější slovo:", sestnacte_slovo)



text_bez_mezer = text.replace(" ", "")


cetnost_pismen = Counter(text_bez_mezer)

nejcastejsi_pismeno = cetnost_pismen.most_common(1)[0]
print("Nejčastější písmeno:", nejcastejsi_pismeno[0])
print("Počet výskytů:", nejcastejsi_pismeno[1])



slova_14 = {s for s in slova if len(s) == 14}
print("14písmenná slova:", slova_14)



slova_8 = {s for s in slova if len(s) == 8}
print("Počet různých osmipísmenných slov:", len(slova_8))