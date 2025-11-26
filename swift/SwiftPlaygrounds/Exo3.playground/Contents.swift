struct Person {
var name: String
var age: Int?
var city: String?
}

let people: [Person] = [
Person(name: "Alice", age: 14, city: "Paris-sur-Mer"),
Person(name: "Bob", age: nil, city: nil),
Person(name: "Charlie", age: 30, city: "Baguette-ville"),
Person(name: "David", age: nil, city: "Escargot-terre"),
Person(name: "Eva", age: 22, city: nil),
Person(name: "Frank", age: 40, city: "Tour-Eiffel-land"),
Person(name: "Grace", age: 18, city: nil)
]

// 1) Age == nil
let ageNil = people.filter { $0.age == nil }

// 2) Ville == nil
let cityNil = people.filter { $0.city == nil }

// 3) Age == nil ET Ville == nil
let bothNil = people.filter { $0.age == nil && $0.city == nil }

// 4) “Majeur” / “Mineur” / “Age inconnu”
func status(for person: Person) -> String {
guard let age = person.age else { return "Age inconnu" }
return age >= 18 ? "Majeur" : "Mineur"
}

// Affichages de contrôle
print("Sans Age:", ageNil.map(\.name))
print("Sans Ville:", cityNil.map(\.name))
print("Sans Age ni Ville:", bothNil.map(\.name))
print("-------------------------------------------------")
people.forEach { print("\($0.name): \(status(for: $0))") }