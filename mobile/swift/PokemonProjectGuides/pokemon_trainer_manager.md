# 🎯 Sujet UIKit — “Pokémon Trainer Manager”

**Pitch**
Vous êtes le professeur Chen. Développez une application UIKit pour gérer les dresseurs Pokémon, suivre leurs Pokémon, leurs badges et leur progression dans la Ligue.

---

## Contenu du fichier
Ce fichier contient :
- Une brève **explication d'architecture** et de la délégation.
- Des **modèles Swift** (`Trainer`, `Pokemon`, `Badge`).
- Un exemple complet d'implémentation **UIKit programmatique** (sans storyboard) :
  - `TrainersListViewController` (liste des dresseurs, `UITableView`).
  - `TrainerDetailViewController` (fiche d'un dresseur : nom, photo, badges, table des Pokémon).
  - `PokemonDetailViewController` (fiche détaillée d'un Pokémon).
  - Cellules personnalisées (`TrainerCell`, `PokemonCell`).
  - Un protocole de délégation `PokemonSelectionDelegate` pour ouvrir la fiche Pokémon depuis la fiche dresseur.
- **Exemples de données** pour tester l'app.

> Remarque : le code est volontairement simple et didactique — prêt à être copié dans un projet Xcode. Remplacez les `UIImage(named:)` par vos assets réels ou par des SF Symbols.

---

## Architecture (résumé)
- `UINavigationController` racine.
- `TrainersListViewController` → liste (UITableView) des dresseurs.
- Sur sélection d'un dresseur : push `TrainerDetailViewController`.
- `TrainerDetailViewController` affiche badges et une `UITableView` des Pokémon du dresseur.
- La sélection d'un Pokémon dans la fiche dresseur déclenche la **délégation** pour ouvrir `PokemonDetailViewController`.

### Délégation
On définit un protocole `PokemonSelectionDelegate` :
```swift
protocol PokemonSelectionDelegate: AnyObject {
    func didSelectPokemon(_ pokemon: Pokemon, from trainer: Trainer)
}
```
`TrainerDetailViewController` possède une propriété `weak var delegate: PokemonSelectionDelegate?` que l'on mettra au `UINavigationController` (ou au `TrainersListViewController`) avant de pusher, ou plus simplement on laisse le `TrainerDetailViewController` pusher directement une nouvelle `PokemonDetailViewController` (ici on montre une variante avec délégation pour illustrer le pattern).

---

## Code complet (Swift, UIKit)

```swift
import UIKit

// MARK: - Modèles
struct Badge {
    let name: String
    let imageName: String // nom d'asset
}

struct Pokemon {
    let name: String
    let type: String
    let imageName: String
    let level: Int
}

struct Trainer {
    let id: UUID = UUID()
    let name: String
    let photoName: String
    var badges: [Badge]
    var pokemons: [Pokemon]
}

// MARK: - Protocole de délégation
protocol PokemonSelectionDelegate: AnyObject {
    func didSelectPokemon(_ pokemon: Pokemon, from trainer: Trainer)
}

// MARK: - TrainerCell (UITableViewCell)
class TrainerCell: UITableViewCell {
    static let reuseId = "TrainerCell"

    private let avatarImageView: UIImageView = {
        let iv = UIImageView()
        iv.contentMode = .scaleAspectFill
        iv.layer.cornerRadius = 30
        iv.clipsToBounds = true
        iv.translatesAutoresizingMaskIntoConstraints = false
        return iv
    }()

    private let nameLabel = UILabel()
    private let countLabel = UILabel()

    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        accessoryType = .disclosureIndicator
        setupLayout()
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    private func setupLayout() {
        nameLabel.font = UIFont.boldSystemFont(ofSize: 17)
        countLabel.font = UIFont.systemFont(ofSize: 13)
        countLabel.textColor = .secondaryLabel

        contentView.addSubview(avatarImageView)
        contentView.addSubview(nameLabel)
        contentView.addSubview(countLabel)

        NSLayoutConstraint.activate([
            avatarImageView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            avatarImageView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
            avatarImageView.widthAnchor.constraint(equalToConstant: 60),
            avatarImageView.heightAnchor.constraint(equalToConstant: 60),

            nameLabel.leadingAnchor.constraint(equalTo: avatarImageView.trailingAnchor, constant: 12),
            nameLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 18),
            nameLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -36),

            countLabel.leadingAnchor.constraint(equalTo: nameLabel.leadingAnchor),
            countLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4)
        ])
    }

    func configure(with trainer: Trainer) {
        nameLabel.text = trainer.name
        countLabel.text = "Pokémon: \(trainer.pokemons.count) • Badges: \(trainer.badges.count)"
        avatarImageView.image = UIImage(named: trainer.photoName) ?? UIImage(systemName: "person.crop.circle")
    }
}

// MARK: - PokemonCell
class PokemonCell: UITableViewCell {
    static let reuseId = "PokemonCell"

    private let iconImageView: UIImageView = {
        let iv = UIImageView()
        iv.contentMode = .scaleAspectFit
        iv.translatesAutoresizingMaskIntoConstraints = false
        iv.layer.cornerRadius = 8
        iv.clipsToBounds = true
        return iv
    }()

    private let nameLabel = UILabel()
    private let typeLabel = UILabel()

    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        accessoryType = .disclosureIndicator
        setupLayout()
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    private func setupLayout() {
        nameLabel.font = UIFont.systemFont(ofSize: 16, weight: .medium)
        typeLabel.font = UIFont.systemFont(ofSize: 13)
        typeLabel.textColor = .secondaryLabel

        contentView.addSubview(iconImageView)
        contentView.addSubview(nameLabel)
        contentView.addSubview(typeLabel)

        NSLayoutConstraint.activate([
            iconImageView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            iconImageView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
            iconImageView.widthAnchor.constraint(equalToConstant: 56),
            iconImageView.heightAnchor.constraint(equalToConstant: 56),

            nameLabel.leadingAnchor.constraint(equalTo: iconImageView.trailingAnchor, constant: 12),
            nameLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: 16),
            nameLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -36),

            typeLabel.leadingAnchor.constraint(equalTo: nameLabel.leadingAnchor),
            typeLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 4)
        ])
    }

    func configure(with pokemon: Pokemon) {
        nameLabel.text = pokemon.name + " Lv.\(pokemon.level)"
        typeLabel.text = pokemon.type
        iconImageView.image = UIImage(named: pokemon.imageName) ?? UIImage(systemName: "bolt.circle")
    }
}

// MARK: - Trainers List
class TrainersListViewController: UIViewController {
    private var trainers: [Trainer] = SampleData.makeTrainers()

    private lazy var tableView: UITableView = {
        let tv = UITableView(frame: .zero, style: .plain)
        tv.register(TrainerCell.self, forCellReuseIdentifier: TrainerCell.reuseId)
        tv.translatesAutoresizingMaskIntoConstraints = false
        tv.rowHeight = 84
        tv.dataSource = self
        tv.delegate = self
        return tv
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Dresseurs"
        view.backgroundColor = .systemBackground
        setupLayout()
    }

    private func setupLayout() {
        view.addSubview(tableView)
        NSLayoutConstraint.activate([
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
}

extension TrainersListViewController: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int { trainers.count }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: TrainerCell.reuseId, for: indexPath) as? TrainerCell else { return UITableViewCell() }
        let t = trainers[indexPath.row]
        cell.configure(with: t)
        return cell
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let trainer = trainers[indexPath.row]
        let detail = TrainerDetailViewController(trainer: trainer)
        // Set delegate if you want selection to be handled elsewhere
        detail.selectionDelegate = self
        navigationController?.pushViewController(detail, animated: true)
    }
}

// MARK: - Trainer Detail
class TrainerDetailViewController: UIViewController {
    private(set) var trainer: Trainer
    weak var selectionDelegate: PokemonSelectionDelegate?

    private let headerImageView = UIImageView()
    private let nameLabel = UILabel()
    private let badgesStack = UIStackView()

    private lazy var tableView: UITableView = {
        let tv = UITableView(frame: .zero, style: .plain)
        tv.register(PokemonCell.self, forCellReuseIdentifier: PokemonCell.reuseId)
        tv.translatesAutoresizingMaskIntoConstraints = false
        tv.dataSource = self
        tv.delegate = self
        return tv
    }()

    init(trainer: Trainer) {
        self.trainer = trainer
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        title = trainer.name
        setupHeader()
        setupTableView()
    }

    private func setupHeader() {
        headerImageView.translatesAutoresizingMaskIntoConstraints = false
        headerImageView.contentMode = .scaleAspectFill
        headerImageView.layer.cornerRadius = 44
        headerImageView.clipsToBounds = true
        headerImageView.image = UIImage(named: trainer.photoName) ?? UIImage(systemName: "person.crop.circle")

        nameLabel.font = UIFont.systemFont(ofSize: 22, weight: .bold)
        nameLabel.text = trainer.name
        nameLabel.translatesAutoresizingMaskIntoConstraints = false

        badgesStack.axis = .horizontal
        badgesStack.spacing = 8
        badgesStack.translatesAutoresizingMaskIntoConstraints = false

        for badge in trainer.badges {
            let iv = UIImageView()
            iv.widthAnchor.constraint(equalToConstant: 40).isActive = true
            iv.heightAnchor.constraint(equalToConstant: 40).isActive = true
            iv.contentMode = .scaleAspectFit
            iv.image = UIImage(named: badge.imageName) ?? UIImage(systemName: "seal")
            iv.layer.cornerRadius = 6
            iv.clipsToBounds = true
            badgesStack.addArrangedSubview(iv)
        }

        view.addSubview(headerImageView)
        view.addSubview(nameLabel)
        view.addSubview(badgesStack)

        NSLayoutConstraint.activate([
            headerImageView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
            headerImageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 16),
            headerImageView.widthAnchor.constraint(equalToConstant: 88),
            headerImageView.heightAnchor.constraint(equalToConstant: 88),

            nameLabel.leadingAnchor.constraint(equalTo: headerImageView.trailingAnchor, constant: 12),
            nameLabel.centerYAnchor.constraint(equalTo: headerImageView.centerYAnchor, constant: -12),
            nameLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),

            badgesStack.leadingAnchor.constraint(equalTo: headerImageView.trailingAnchor, constant: 12),
            badgesStack.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 8)
        ])
    }

    private func setupTableView() {
        view.addSubview(tableView)
        NSLayoutConstraint.activate([
            tableView.topAnchor.constraint(equalTo: headerImageView.bottomAnchor, constant: 18),
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
}

extension TrainerDetailViewController: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int { trainer.pokemons.count }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: PokemonCell.reuseId, for: indexPath) as? PokemonCell else { return UITableViewCell() }
        cell.configure(with: trainer.pokemons[indexPath.row])
        return cell
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let pokemon = trainer.pokemons[indexPath.row]
        // Option 1: Délégation
        selectionDelegate?.didSelectPokemon(pokemon, from: trainer)

        // Option 2: Navigation directe (si pas de delegate) :
        if selectionDelegate == nil {
            let pdvc = PokemonDetailViewController(pokemon: pokemon)
            navigationController?.pushViewController(pdvc, animated: true)
        }
    }
}

// MARK: - Pokemon Detail
class PokemonDetailViewController: UIViewController {
    private let pokemon: Pokemon

    private let imageView = UIImageView()
    private let nameLabel = UILabel()
    private let typeLabel = UILabel()

    init(pokemon: Pokemon) {
        self.pokemon = pokemon
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        title = pokemon.name
        setupLayout()
    }

    private func setupLayout() {
        imageView.translatesAutoresizingMaskIntoConstraints = false
        imageView.contentMode = .scaleAspectFit
        imageView.image = UIImage(named: pokemon.imageName) ?? UIImage(systemName: "bolt.circle")

        nameLabel.font = UIFont.systemFont(ofSize: 28, weight: .bold)
        nameLabel.text = pokemon.name
        nameLabel.translatesAutoresizingMaskIntoConstraints = false

        typeLabel.font = UIFont.systemFont(ofSize: 18)
        typeLabel.textColor = .secondaryLabel
        typeLabel.text = "Type: \(pokemon.type) — Niv: \(pokemon.level)"
        typeLabel.translatesAutoresizingMaskIntoConstraints = false

        view.addSubview(imageView)
        view.addSubview(nameLabel)
        view.addSubview(typeLabel)

        NSLayoutConstraint.activate([
            imageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 24),
            imageView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            imageView.widthAnchor.constraint(equalToConstant: 160),
            imageView.heightAnchor.constraint(equalToConstant: 160),

            nameLabel.topAnchor.constraint(equalTo: imageView.bottomAnchor, constant: 20),
            nameLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor),

            typeLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 12),
            typeLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor)
        ])
    }
}

// MARK: - Sample Data
enum SampleData {
    static func makeTrainers() -> [Trainer] {
        let badgesAsh = [
            Badge(name: "Cascade Badge", imageName: "badge_cascade"),
            Badge(name: "Boulder Badge", imageName: "badge_boulder"),
            Badge(name: "Thunder Badge", imageName: "badge_thunder")
        ]

        let ashPokemons = [
            Pokemon(name: "Pikachu", type: "Électrik", imageName: "pikachu", level: 50),
            Pokemon(name: "Charizard", type: "Feu/Vol", imageName: "charizard", level: 63),
            Pokemon(name: "Bulbasaur", type: "Plante/Poison", imageName: "bulbasaur", level: 20)
        ]

        let misty = Trainer(name: "Ondine", photoName: "misty", badges: [Badge(name: "Cascade Badge", imageName: "badge_cascade")], pokemons: [
            Pokemon(name: "Stari", type: "Eau/Psy", imageName: "staryu", level: 28),
            Pokemon(name: "Starmie", type: "Eau/Psy", imageName: "starmie", level: 34)
        ])

        let brock = Trainer(name: "Pierre", photoName: "brock", badges: [Badge(name: "Boulder Badge", imageName: "badge_boulder")], pokemons: [
            Pokemon(name: "Onix", type: "Roche/Sol", imageName: "onix", level: 40)
        ])

        let ash = Trainer(name: "Sacha", photoName: "ash", badges: badgesAsh, pokemons: ashPokemons)

        return [ash, misty, brock]
    }
}

// MARK: - App Launch (SceneDelegate example)
// Dans un projet Xcode sans storyboard, utilisez ce code dans SceneDelegate.swift / AppDelegate.swift

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = (scene as? UIWindowScene) else { return }
        window = UIWindow(windowScene: windowScene)
        let root = TrainersListViewController()
        let nav = UINavigationController(rootViewController: root)
        window?.rootViewController = nav
        window?.makeKeyAndVisible()
    }
}
```

---

## Explication pas-à-pas (comment ça marche)
1. **Modèles** : `Trainer` contient `badges` et `pokemons`. Les `imageName` servent à récupérer des assets (ou SF Symbols de secours).
2. **Liste des dresseurs** : `TrainersListViewController` affiche un `UITableView` avec `TrainerCell`. Taper sur une cellule pousse `TrainerDetailViewController`.
3. **Fiche dresseur** : affiche image, nom, badges (stack horizontal) et une `UITableView` des Pokémon. La `tableView` des Pokémon utilise `PokemonCell`.
4. **Sélection d’un Pokémon** : quand l'utilisateur tape un Pokémon dans la fiche dresseur, on appelle `selectionDelegate?.didSelectPokemon(...)`. Si aucun délégué n'est fourni, on navigue directement vers `PokemonDetailViewController`.
5. **Délégation** : utile si vous voulez centraliser la logique de navigation ailleurs (par ex. un coordinator). Le code montre les deux modes (délégation ou navigation directe).

---

## Notes & améliorations possibles
- **Images** : ajoutez vos assets (pikachu, charizard, badge_cascade, etc.) dans l'Asset Catalog. Le code contient des `UIImage(systemName:)` de secours.
- **Badges** : on affiche ici des `UIImageView` dans un `UIStackView`. Pour beaucoup de badges, utiliser `UICollectionView` sera plus adapté.
- **State & persistance** : vous pouvez stocker les `Trainer` dans CoreData, Realm ou JSON local.
- **Architecture** : le pattern Coordinator ou MVVM rendra la navigation/données plus testables.
- **Accessibilité** : ajouter `accessibilityLabel` et tailles dynamiques.

---

## Comment utiliser
1. Créez un nouveau projet Xcode (App iOS) sans storyboard.
2. Collez les modèles et ViewControllers dans des fichiers Swift.
3. Remplacez `SceneDelegate`/`AppDelegate` comme indiqué ou adaptez selon votre template.
4. Ajoutez des images dans `Assets.xcassets` pour `pikachu`, `charizard`, etc.
5. Lancez l'app sur simulateur.

---

Bonne construction — si vous voulez, je peux :
- transformer ce code en version SwiftUI.
- ajouter persistance (CoreData) et sauvegarde des progrès.
- ajouter animations et transitions pour la navigation.

Fin du fichier.

