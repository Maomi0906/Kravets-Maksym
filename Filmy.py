import matplotlib.pyplot as plt
import statistics

filmy = [
    ("The Shawshank Redemption", 1994, 9.3),
    ("The Godfather", 1972, 9.2),
    ("The Dark Knight", 2008, 9.0),
    ("Pulp Fiction", 1994, 8.9),
    ("Forrest Gump", 1994, 8.8),
    ("Inception", 2010, 8.8),
    ("Fight Club", 1999, 8.8),
    ("Interstellar", 2014, 8.6),
    ("Parasite", 2019, 8.6),
    ("Whiplash", 2014, 8.5)
]

top = [f for f in filmy if f[2] >= 9]
nove = [f for f in filmy if f[1] > 2000]

print("Top filmy (>=9):", top)
print("Nové filmy (>2000):", nove)

print("Podle roku:", sorted(filmy, key=lambda x: x[1]))
print("Podle hodnocení:", sorted(filmy, key=lambda x: x[2], reverse=True))

hodnoceni = [f[2] for f in filmy]
print("Průměr:", statistics.mean(hodnoceni))
print("Medián:", statistics.median(hodnoceni))

plt.hist(hodnoceni, bins=5, color="skyblue", edgecolor="black")
plt.title("Histogram hodnocení")
plt.xlabel("Hodnocení")
plt.ylabel("Počet filmů")
plt.show()
