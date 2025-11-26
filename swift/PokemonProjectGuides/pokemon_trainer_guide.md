# Guide Complet - Pokémon Trainer Manager (UIKit)

## 🎯 Présentation du Projet

Vous allez développer une application iOS pour le **Professeur Chen** afin de gérer les dresseurs Pokémon, leurs équipes, leurs badges et leur progression dans la Ligue Pokémon.

### Concept
Une application complète de gestion permettant de :
- Consulter la liste des dresseurs par région
- Voir les détails de chaque dresseur (équipe, badges, stats)
- Explorer les fiches détaillées des Pokémon
- Ajouter de nouveaux dresseurs
- Prévisualiser les badges et cartes en haute définition

## 📋 Fonctionnalités Requises

### ✅ Fonctionnalités Principales

1. **Liste des Dresseurs** (UITableView avec sections)
2. **Fiche Dresseur Détaillée**
3. **Fiche Pokémon Détaillée** (délégation)
4. **Chargement de données JSON** (Bundle)
5. **Ajout de nouveau dresseur** (Formulaire)
6. **Prévisualisation QLPreview** (Badges/Cartes HD)
7. **Sections par région** (Kanto, Johto, Hoenn...)

### 🌟 Fonctionnalités Bonus
- Système de score/classement
- Filtre par type de Pokémon
- Timer de combat simulé

## 🏗 Architecture de l'Application

### Structure MVC Recommandée

```
📁 Models/
   ├── Trainer.swift           // Modèle Dresseur
   ├── Pokemon.swift           // Modèle Pokémon  
   ├── Badge.swift            // Modèle Badge
   ├── Region.swift           // Modèle Région
   └── DataManager.swift      // Gestionnaire de données JSON

📁 Views/
   ├── Main.storyboard        // Interface principale
   ├── TrainerCell.swift      // Cellule dresseur personnalisée
   └── PokemonCell.swift      // Cellule Pokémon personnalisée

📁 Controllers/
   ├── TrainerListViewController.swift    // Liste des dresseurs
   ├── TrainerDetailViewController.swift  // Détails dresseur
   ├── PokemonDetailViewController.swift  // Détails Pokémon
   └── AddTrainerViewController.swift     // Ajout dresseur

📁 Resources/
   ├── trainers.json          // Données dresseurs
   ├── pokemons.json         // Données Pokémon
   └── Images/               // Images et badges
```

## 📱 Interfaces et Navigation

### 1. Écran Principal - Liste des Dresseurs

**Composants :**
- `UITableView` avec sections par région
- Cellules personnalisées affichant :
  - Photo du dresseur
  - Nom
  - Nombre de Pokémon
  - Région d'origine

**Navigation :**
- Tap sur une cellule → Fiche dresseur détaillée

### 2. Fiche Dresseur Détaillée

**Composants :**
- `UIScrollView` pour le contenu
- Photo du dresseur (grande taille)
- Informations : nom, région, score
- Collection des badges obtenus
- `UITableView` ou `UICollectionView` des Pokémon

**Navigation :**
- Tap sur un Pokémon → Fiche Pokémon détaillée
- Tap sur un badge → QLPreview

### 3. Fiche Pokémon Détaillée

**Composants :**
- Image du Pokémon
- Statistiques détaillées
- Type(s) du Pokémon
- Capacités spéciales

## 🗂 Modèles de Données

### Trainer (Dresseur)
```swift
struct Trainer: Codable {
    let id: Int
    let name: String
    let photoURL: String
    let region: String
    let pokemons: [Pokemon]
    let badges: [Badge]
    let score: Int
    
    var pokemonCount: Int {
        return pokemons.count
    }
    
    var badgeCount: Int {
        return badges.count
    }
}
```

### Pokemon
```swift
struct Pokemon: Codable {
    let id: Int
    let name: String
    let imageURL: String
    let types: [String]
    let level: Int
    let hp: Int
    let attack: Int
    let defense: Int
    let speed: Int
    
    var primaryType: String {
        return types.first ?? "Normal"
    }
}
```

### Badge
```swift
struct Badge: Codable {
    let id: Int
    let name: String
    let imageURL: String
    let region: String
    let gymLeader: String
    let type: String
}
```

### Region
```swift
enum Region: String, CaseIterable, Codable {
    case kanto = "Kanto"
    case johto = "Johto" 
    case hoenn = "Hoenn"
    case sinnoh = "Sinnoh"
    case unova = "Unova"
    case kalos = "Kalos"
    case alola = "Alola"
    case galar = "Galar"
}
```

## 📊 Gestion des Données JSON

### DataManager
```swift
class DataManager {
    static let shared = DataManager()
    private init() {}
    
    func loadTrainers() -> [Trainer] {
        guard let url = Bundle.main.url(forResource: "trainers", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let trainers = try? JSONDecoder().decode([Trainer].self, from: data) else {
            print("Erreur chargement trainers.json")
            return []
        }
        return trainers
    }
    
    func loadPokemons() -> [Pokemon] {
        guard let url = Bundle.main.url(forResource: "pokemons", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let pokemons = try? JSONDecoder().decode([Pokemon].self, from: data) else {
            print("Erreur chargement pokemons.json")
            return []
        }
        return pokemons
    }
    
    func groupTrainersByRegion(trainers: [Trainer]) -> [String: [Trainer]] {
        return Dictionary(grouping: trainers) { $0.region }
    }
}
```

### Structure JSON Exemple

**trainers.json**
```json
[
    {
        "id": 1,
        "name": "Sacha",
        "photoURL": "sacha.jpg",
        "region": "Kanto",
        "score": 8500,
        "pokemons": [
            {
                "id": 25,
                "name": "Pikachu",
                "imageURL": "pikachu.png",
                "types": ["Électrik"],
                "level": 55,
                "hp": 150,
                "attack": 120,
                "defense": 80,
                "speed": 140
            }
        ],
        "badges": [
            {
                "id": 1,
                "name": "Badge Roche",
                "imageURL": "badge_roche.png",
                "region": "Kanto",
                "gymLeader": "Pierre",
                "type": "Roche"
            }
        ]
    }
]
```

## 🎨 Interface Utilisateur Détaillée

### TrainerListViewController
```swift
class TrainerListViewController: UITableViewController {
    
    // MARK: - Properties
    private var trainers: [Trainer] = []
    private var groupedTrainers: [String: [Trainer]] = [:]
    private var regions: [String] = []
    
    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        loadData()
    }
    
    private func setupUI() {
        title = "Dresseurs Pokémon"
        navigationItem.rightBarButtonItem = UIBarButtonItem(
            barButtonSystemItem: .add,
            target: self,
            action: #selector(addTrainerTapped)
        )
        
        // Cellule personnalisée
        tableView.register(TrainerCell.self, forCellReuseIdentifier: "TrainerCell")
    }
    
    private func loadData() {
        trainers = DataManager.shared.loadTrainers()
        groupedTrainers = DataManager.shared.groupTrainersByRegion(trainers: trainers)
        regions = Array(groupedTrainers.keys).sorted()
        tableView.reloadData()
    }
    
    @objc private func addTrainerTapped() {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let addVC = storyboard.instantiateViewController(withIdentifier: "AddTrainerViewController") as! AddTrainerViewController
        let navController = UINavigationController(rootViewController: addVC)
        present(navController, animated: true)
    }
}

// MARK: - TableView DataSource
extension TrainerListViewController {
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return regions.count
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        let region = regions[section]
        return groupedTrainers[region]?.count ?? 0
    }
    
    override func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return regions[section]
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "TrainerCell", for: indexPath) as! TrainerCell
        
        let region = regions[indexPath.section]
        if let trainersInRegion = groupedTrainers[region] {
            let trainer = trainersInRegion[indexPath.row]
            cell.configure(with: trainer)
        }
        
        return cell
    }
}

// MARK: - TableView Delegate  
extension TrainerListViewController {
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        
        let region = regions[indexPath.section]
        if let trainersInRegion = groupedTrainers[region] {
            let trainer = trainersInRegion[indexPath.row]
            showTrainerDetail(trainer: trainer)
        }
    }
    
    private func showTrainerDetail(trainer: Trainer) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let detailVC = storyboard.instantiateViewController(withIdentifier: "TrainerDetailViewController") as! TrainerDetailViewController
        detailVC.trainer = trainer
        navigationController?.pushViewController(detailVC, animated: true)
    }
}
```

### TrainerCell (Cellule personnalisée)
```swift
class TrainerCell: UITableViewCell {
    
    // MARK: - UI Elements
    private let trainerImageView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.cornerRadius = 25
        imageView.translatesAutoresizingMaskIntoConstraints = false
        return imageView
    }()
    
    private let nameLabel: UILabel = {
        let label = UILabel()
        label.font = UIFont.boldSystemFont(ofSize: 16)
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()
    
    private let pokemonCountLabel: UILabel = {
        let label = UILabel()
        label.font = UIFont.systemFont(ofSize: 14)
        label.textColor = .systemGray
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()
    
    private let badgeCountLabel: UILabel = {
        let label = UILabel()
        label.font = UIFont.systemFont(ofSize: 14)
        label.textColor = .systemOrange
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()
    
    // MARK: - Initialization
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        setupUI()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    // MARK: - UI Setup
    private func setupUI() {
        contentView.addSubview(trainerImageView)
        contentView.addSubview(nameLabel)
        contentView.addSubview(pokemonCountLabel)
        contentView.addSubview(badgeCountLabel)
        
        NSLayoutConstraint.activate([
            // Image
            trainerImageView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            trainerImageView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
            trainerImageView.widthAnchor.constraint(equalToConstant: 50),
            trainerImageView.heightAnchor.constraint(equalToConstant: 50),
            
            // Name
            nameLabel.leadingAnchor.constraint(equalTo: trainerImageView.trailingAnchor, constant: 16),
            nameLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 12),
            nameLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -16),
            
            // Pokemon count
            pokemonCountLabel.leadingAnchor.constraint(equalTo: nameLabel.leadingAnchor),
            pokemonCountLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4),
            
            // Badge count
            badgeCountLabel.leadingAnchor.constraint(equalTo: pokemonCountLabel.trailingAnchor, constant: 16),
            badgeCountLabel.centerYAnchor.constraint(equalTo: pokemonCountLabel.centerYAnchor),
            badgeCountLabel.bottomAnchor.constraint(equalTo: contentView.bottomAnchor, constant: -12)
        ])
    }
    
    // MARK: - Configuration
    func configure(with trainer: Trainer) {
        nameLabel.text = trainer.name
        pokemonCountLabel.text = "⚡ \(trainer.pokemonCount) Pokémon"
        badgeCountLabel.text = "🏆 \(trainer.badgeCount) badges"
        
        // Charger l'image du dresseur
        if let image = UIImage(named: trainer.photoURL) {
            trainerImageView.image = image
        } else {
            trainerImageView.image = UIImage(systemName: "person.circle.fill")
        }
    }
}
```

## 🔄 Pattern Délégation pour Navigation

### Protocol PokemonSelectionDelegate
```swift
protocol PokemonSelectionDelegate: AnyObject {
    func didSelectPokemon(_ pokemon: Pokemon)
}
```

### Implémentation dans TrainerDetailViewController
```swift
class TrainerDetailViewController: UIViewController {
    
    var trainer: Trainer!
    
    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        displayTrainerInfo()
    }
    
    private func setupUI() {
        title = trainer.name
        view.backgroundColor = .systemBackground
    }
}

// MARK: - PokemonSelectionDelegate
extension TrainerDetailViewController: PokemonSelectionDelegate {
    
    func didSelectPokemon(_ pokemon: Pokemon) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let pokemonDetailVC = storyboard.instantiateViewController(withIdentifier: "PokemonDetailViewController") as! PokemonDetailViewController
        pokemonDetailVC.pokemon = pokemon
        navigationController?.pushViewController(pokemonDetailVC, animated: true)
    }
}
```

## 📷 QLPreview pour Badges et Cartes

### Intégration QuickLook
```swift
import QuickLook

class TrainerDetailViewController: UIViewController, QLPreviewControllerDataSource, QLPreviewControllerDelegate {
    
    private var selectedBadgeURL: URL?
    
    // MARK: - Badge Preview
    private func previewBadge(badge: Badge) {
        guard let url = Bundle.main.url(forResource: badge.imageURL, withExtension: nil) else {
            print("Badge image not found: \(badge.imageURL)")
            return
        }
        
        selectedBadgeURL = url
        
        let previewController = QLPreviewController()
        previewController.dataSource = self
        previewController.delegate = self
        present(previewController, animated: true)
    }
    
    // MARK: - QLPreviewControllerDataSource
    func numberOfPreviewItems(in controller: QLPreviewController) -> Int {
        return selectedBadgeURL != nil ? 1 : 0
    }
    
    func previewController(_ controller: QLPreviewController, previewItemAt index: Int) -> QLPreviewItem {
        return selectedBadgeURL! as QLPreviewItem
    }
}
```

## ➕ Formulaire d'Ajout de Dresseur

### AddTrainerViewController
```swift
class AddTrainerViewController: UIViewController {
    
    // MARK: - IBOutlets
    @IBOutlet weak var nameTextField: UITextField!
    @IBOutlet weak var regionPicker: UIPickerView!
    @IBOutlet weak var starterPokemonPicker: UIPickerView!
    @IBOutlet weak var photoImageView: UIImageView!
    
    // MARK: - Properties  
    private let regions = Region.allCases.map { $0.rawValue }
    private let starterPokemons: [Pokemon] = [] // Chargé depuis JSON
    
    // MARK: - Actions
    @IBAction func saveButtonTapped(_ sender: UIButton) {
        guard let name = nameTextField.text, !name.isEmpty else {
            showAlert(message: "Veuillez saisir un nom")
            return
        }
        
        let selectedRegion = regions[regionPicker.selectedRow(inComponent: 0)]
        let selectedStarter = starterPokemons[starterPokemonPicker.selectedRow(inComponent: 0)]
        
        let newTrainer = Trainer(
            id: generateNewID(),
            name: name,
            photoURL: "default_trainer.png",
            region: selectedRegion,
            pokemons: [selectedStarter],
            badges: [],
            score: 0
        )
        
        // Sauvegarder le nouveau dresseur
        saveNewTrainer(newTrainer)
        
        dismiss(animated: true)
    }
    
    @IBAction func cancelButtonTapped(_ sender: UIButton) {
        dismiss(animated: true)
    }
    
    private func showAlert(message: String) {
        let alert = UIAlertController(title: "Erreur", message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}
```

## 🏆 Fonctionnalités Bonus

### 1. Système de Score/Classement
```swift
extension TrainerListViewController {
    
    private func sortTrainersByScore() {
        trainers.sort { $0.score > $1.score }
        groupedTrainers = DataManager.shared.groupTrainersByRegion(trainers: trainers)
        tableView.reloadData()
    }
    
    private func calculateScore(for trainer: Trainer) -> Int {
        let pokemonScore = trainer.pokemons.reduce(0) { $0 + $1.level }
        let badgeScore = trainer.badges.count * 100
        return pokemonScore + badgeScore
    }
}
```

### 2. Filtre par Type de Pokémon
```swift
extension TrainerListViewController {
    
    private func filterTrainers(by pokemonType: String) {
        let filteredTrainers = trainers.filter { trainer in
            trainer.pokemons.contains { pokemon in
                pokemon.types.contains(pokemonType)
            }
        }
        groupedTrainers = DataManager.shared.groupTrainersByRegion(trainers: filteredTrainers)
        tableView.reloadData()
    }
}
```

### 3. Timer de Combat
```swift
class BattleTimerViewController: UIViewController {
    
    @IBOutlet weak var timerLabel: UILabel!
    @IBOutlet weak var startButton: UIButton!
    
    private var timer: Timer?
    private var timeRemaining: Int = 300 // 5 minutes
    
    @IBAction func startBattle(_ sender: UIButton) {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.updateTimer()
        }
        startButton.isEnabled = false
    }
    
    private func updateTimer() {
        if timeRemaining > 0 {
            timeRemaining -= 1
            timerLabel.text = formatTime(timeRemaining)
        } else {
            timer?.invalidate()
            showBattleResult()
        }
    }
    
    private func formatTime(_ seconds: Int) -> String {
        let minutes = seconds / 60
        let seconds = seconds % 60
        return String(format: "%02d:%02d", minutes, seconds)
    }
}
```

## ✅ Check-list de Développement

### Phase 1 : Configuration Projet
- [ ] Créer projet Xcode "Pokemon Trainer Manager"
- [ ] Configurer storyboards et ViewControllers
- [ ] Ajouter fichiers JSON au Bundle
- [ ] Importer images et ressources

### Phase 2 : Modèles de Données
- [ ] Créer struct Trainer, Pokemon, Badge
- [ ] Implémenter DataManager
- [ ] Tester chargement JSON

### Phase 3 : Interface Principale
- [ ] TrainerListViewController avec sections
- [ ] Cellules personnalisées
- [ ] Navigation vers détails

### Phase 4 : Fiche Dresseur
- [ ] TrainerDetailViewController
- [ ] Affichage informations dresseur
- [ ] Collection Pokémon et badges
- [ ] Délégation pour sélection Pokémon

### Phase 5 : Fiche Pokémon
- [ ] PokemonDetailViewController
- [ ] Affichage statistiques détaillées

### Phase 6 : Fonctionnalités Avancées
- [ ] QLPreview pour badges
- [ ] Formulaire ajout dresseur
- [ ] Sections par région

### Phase 7 : Bonus (Optionnel)
- [ ] Système de score
- [ ] Filtres par type
- [ ] Timer de combat

## 🚀 Conseils de Développement

### Best Practices
- Utiliser **Auto Layout** pour toutes les contraintes
- Implémenter la **gestion d'erreurs** pour le chargement JSON
- Optimiser les **performances** avec `dequeueReusableCell`
- Respecter les **conventions de nommage** Swift

### Debug et Tests
- Tester sur **différents simulateurs** (iPhone, iPad)
- Vérifier les **rotations d'écran**
- Tester avec des **données vides** ou manquantes

### Documentation
- Commenter le code complexe
- Utiliser `// MARK:` pour organiser le code
- Créer un README avec instructions

---

**Ce guide vous donne tous les éléments pour créer une application Pokémon Trainer Manager complète avec UIKit. Bon développement, futur Professeur Chen ! 🧑‍🔬⚡**