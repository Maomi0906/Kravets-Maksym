from collections import Counter

# -----------------------------
# Načtení textového souboru
# -----------------------------
soubor = "alice.txt"

with open(soubor, "r", encoding="utf-8") as f:
    text = f.read()

# rozdělíme text na jednotlivá slova podle mezer
slova = text.split()


# -------------------------------------------------
# 1) Spočítejte počet slov v přiloženém souboru
# -------------------------------------------------
pocet_slov = len(slova)
print("Počet slov:", pocet_slov)


# -------------------------------------------------
# 2) Spočítejte počty výskytů jednotlivých slov
#    a zjistěte 16. nejčastější slovo
# -------------------------------------------------
cetnost_slov = Counter(slova)

# nejčastější slovo (mělo by být 'the')
print("Nejčastější slovo:", cetnost_slov.most_common(1))

# 16. nejčastější slovo
sestnacte_slovo = cetnost_slov.most_common(16)[15]
print("16. nejčastější slovo:", sestnacte_slovo)


# -------------------------------------------------
# 3) Určete nejčastější písmeno v souboru
# -------------------------------------------------
# odstraníme mezery
text_bez_mezer = text.replace(" ", "")

# spočítáme četnost písmen
cetnost_pismen = Counter(text_bez_mezer)

# nejčastější písmeno a jeho počet
nejcastejsi_pismeno = cetnost_pismen.most_common(1)[0]
print("Nejčastější písmeno:", nejcastejsi_pismeno[0])
print("Počet výskytů:", nejcastejsi_pismeno[1])


# -------------------------------------------------
# 4) Soubor obsahuje pouze 4 různá 14písmenná slova
#    vypíšeme je pro kontrolu
# -------------------------------------------------
slova_14 = {s for s in slova if len(s) == 14}
print("14písmenná slova:", slova_14)


# -------------------------------------------------
# 5) Určete, kolik obsahuje soubor různých
#    osmipísmenných slov
# -------------------------------------------------
slova_8 = {s for s in slova if len(s) == 8}
print("Počet různých osmipísmenných slov:", len(slova_8))