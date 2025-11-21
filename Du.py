puvodni_seznam = ["Song A", "Song B", "Song C"]
hudba = puvodni_seznam.copy()
hudba.append("Song D")
hudba.pop(0)
print("Délka listu:", len(hudba))
print("Aktuální list:", hudba)
