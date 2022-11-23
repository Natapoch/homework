postcards = {
    "Maria": "London",
    "Lorenzo": "Milan",
    "Oleg": "Canberra",
    "Hans": "Calgary",
    "Mark": "Milan",
    "Alex": "Krakow",
    "Julia": "Murmansk"
}


postcards["Petra"] = "Paris"
postcards["Ivan"] = "Moscow"
print(postcards) #после добавления 2-х открыток.
postcards["Oleg"] = "Sydney"
print(postcards) # после замены Канберры на Сидней
cities = set(postcards.values())
print(*cities, sep=", ")
print(len(cities))
