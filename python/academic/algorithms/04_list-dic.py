

uglyList = [
	("Tanguy", "2INFO3"), \
	("Robin", "2INFO1"), \
	("Berkan", "2INFO3"), \
	("Victor", "2INFO2"), \
	("Nathan", "2INFO2"), \
	("Eya", "2INFO3"), \
	("Florian", "2INFO3"), \
	("Titouan", "2INFO1"), \
	("Mohamed", "2INFO2"), \
	("Enzo", "2INFO2"), \
	("Mattéo", "2INFO3"), \
	("Mano", "2INFO2"), \
	("Quentin", "2INFO3"), \
	("Thomas", "2INFO3"), \
	("Justin", "2INFO1"), \
	("Alexis", "2INFO3"), \
	("Mattéo", "2INFO3"), \
	("Mohamed", "2INFO1"), \
	("Aina", "2INFO1"), \
	("Melih", "2INFO2"), \
	("Ethann", "2INFO1"), \
	("Tom", "2INFO2"), \
	("Baptiste", "2INFO2"), \
	("Nicolas", "2INFO3"), \
	("Quentin", "2INFO1"), \
	("Maïlys", "2INFO2"), \
	("Kenny", "2INFO1"), \
	("Esteban", "2INFO1"), \
	("Mahé", "2INFO2"), \
	("Sammy", "2INFO2"), \
	("Mehdi", "2INFO2"), \
	("Yassine", "2INFO1"), \
	("Lou", "2INFO1"), \
	("Cyril", "2INFO3"), \
	("Simon", "2INFO1"), \
	("Noa", "2INFO1"), \
	("Mathis", "2INFO3"), \
	("Axel", "2INFO2"), \
	("Lukas", "2INFO1"), \
	("Victor", "2INFO3"), \
	("Matthéo", "2INFO3"), \
	("Lucas", "2INFO1"), \
	("Anes", "2INFO1"), \
	("Clément", "2INFO2"), \
	("Jordan", "2INFO1"), \
	("Léo", "2INFO1"), \
	("Lou", "2INFO1"), \
	("Laetitia", "2INFO2"), \
	("Anthony", "2INFO3"), \
	("Nazar", "2INFO2"), \
	("Yannis", "2INFO2"), \
	("Victor", "2INFO2"), \
	("Robin", "2INFO3"), \
	("Faher", "2INFO3"), \
	("Ahmed", "2INFO3"), \
	("Kenny", "2INFO3"), \
	("Louve", "2INFO2"), \
	("Valentin", "2INFO2"), \
	("Jules", "2INFO1"), \
	("Ewan", "2INFO1"), \
	("Yanis", "2INFO2"), \
	("Armand", "2INFO2"), \
	("Elioth", "2INFO2"), \
	("Nathan", "2INFO1"), \
	("Réda", "2INFO3"), \
	("Eddy", "2INFO3"), \
	("Valentin", "2INFO1"), \
	("Rayan", "2INFO1"), \
	("Mathieu", "2INFO3"), \
	("Alexis", "2INFO3"), \
	("Sefer", "2INFO3"), \
	("Feyza", "2INFO2"), \
	("Maël", "2INFO3"), \
	("Enzo", "2INFO1"), \
]

# 2INFO1 : Enzo, Rayan...
# 2INFO2 : Rayza, Elioth...
# 2INFO3 : Maël, ...

beautifulCollection = { }

for student,group in uglyList:
	# print(student,end=" ")
	if not group in beautifulCollection:
		beautifulCollection[group] = []
	beautifulCollection[group].append(student)

print(beautifulCollection)
