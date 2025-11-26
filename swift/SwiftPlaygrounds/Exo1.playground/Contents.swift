// 1) Générer un tableau de 20 entiers aléatoires
let numbers: [Int] = (0..<20).map { _ in Int.random(in: 0...100) }

// 2) Somme des éléments
func sum(of values: [Int]) -> Int {
values.reduce(0, +)
}
let total = sum(of: numbers)

// 3) Moyenne des éléments
func average(of values: [Int]) -> Double {
guard !values.isEmpty else { return .nan }
return Double(sum(of: values)) / Double(values.count)
}
let avg = average(of: numbers)

// 4) Valeur maximale
let maxValue = numbers.max()

// 5) Filtrer les éléments pairs
let evenNumbers = numbers.filter { $0 % 2 == 0 }

// 6) Transformer en tableau de String
let asStrings = numbers.map(String.init)

// Petits affichages de contrôle
print("numbers:", numbers)
print("sum:", total, "avg:", avg, "max:", maxValue ?? -1)
print("even:", evenNumbers)
print("strings:", asStrings)