enum Diet: String {
    case carnivore = "🥩"
    case herbivore = "🥕"
    case omnivore = "🍔"
}

enum Animal: CaseIterable {
    case cat, dog, elephant, giraffe, panda, penguin, cheetah, dolphin, lion, turtle

    // Emoji corresponding
    var emoji: String {
        switch self {
        case .cat: return "🐱"
        case .dog: return "🐶"
        case .elephant: return "🐘"
        case .giraffe: return "🦒"
        case .panda: return "🐼"
        case .penguin: return "🐧"
        case .cheetah: return "🐆"
        case .dolphin: return "🐬"
        case .lion: return "🦁"
        case .turtle: return "🐢"
        }
    }

    // Type d’alimentation
    var diet: Diet {
        switch self {
        case .cat, .dog, .cheetah, .dolphin, .lion: return .carnivore
        case .elephant, .giraffe, .panda, .turtle: return .herbivore
        case .penguin: return .omnivore
        }
    }

    var nom: String {
        switch self {
        case .cat: return "le Chat"
        case .dog: return "le Chien"
        case .elephant: return "l'Éléphant"
        case .giraffe: return "la Girafe"
        case .panda: return "le Panda"
        case .penguin: return "le Pingouin"
        case .cheetah: return "le Guépard"
        case .dolphin: return "le Dauphin"
        case .lion: return "le Lion"
        case .turtle: return "la Tortue"
        }
    }
}

// Print the animals with their diets
Animal.allCases.forEach { animal in
    print("\(animal) aka \(animal.nom) \(animal.emoji) : \(animal.diet) \(animal.diet.rawValue)")
}