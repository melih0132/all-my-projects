# Guide de Révision Swift & UIKit - Niveau Avancé

---

## Sujets Clés à Maîtriser

### 1. Delegates & Protocols

#### Concepts Avancés

- **Protocol-Oriented Programming** : Préférer les protocols aux classes
- **Associated Types** : `associatedtype` dans les protocols
- **Protocol Extensions** : Implémentations par défaut
- **Protocol Inheritance** : Un protocol peut hériter d'autres protocols

#### Questions Types

```swift
// Quelle est la différence entre ces deux déclarations ?
protocol Drawable {
    func draw()
}
extension Drawable {
    func draw() { print("Drawing...") }
}
// vs
protocol Drawable {
    func draw()
}
```
**Réponse** : La première fournit une implémentation par défaut, la seconde oblige chaque type à implémenter `draw()`.

#### Delegate Pattern Avancé

```swift
// Weak vs Strong delegates
weak var delegate: MyDelegate?    // Évite retain cycles
var delegate: MyDelegate?         // Peut créer des retain cycles
```

---

### 2. Closures Avancées

#### Concepts Clés

- **Escaping vs Non-escaping** closures
- **@autoclosure** : Exécution différée automatique
- **Capturing Values** : [weak self], [unowned self]
- **Trailing Closures** et **Multiple Trailing Closures**

#### Code Critique

```swift
// Retain cycle potentiel
class ViewController: UIViewController {
    var completion: (() -> Void)?
    func setupCompletion() {
        completion = { self.view.backgroundColor = .red } // Retain cycle
        completion = { [weak self] in self?.view.backgroundColor = .red } // Pas de retain cycle
    }
}
```

#### @escaping vs non-escaping

```swift
// Non-escaping (par défaut)
func execute(closure: () -> Void) {
    closure() // Exécutée immédiatement
}

// Escaping
func executeAsync(closure: @escaping () -> Void) {
    DispatchQueue.main.async {
        closure() // Exécutée plus tard
    }
}
```

---

### 3. Auto Layout Avancé

#### Priorités de Contraintes

- **Required (1000)** : Contrainte obligatoire
- **DefaultHigh (750)** : Résistance à la compression
- **DefaultLow (250)** : Résistance à l'étirement

#### Content Hugging vs Compression Resistance

```swift
label.setContentHuggingPriority(.required, for: .horizontal)
label.setContentCompressionResistancePriority(.required, for: .horizontal)
```

#### Intrinsic Content Size

```swift
class CustomView: UIView {
    override var intrinsicContentSize: CGSize {
        return CGSize(width: 100, height: 50)
    }
}
```

#### Stack Views Avancées

- **Distribution** : fill, fillEqually, fillProportionally, equalSpacing, equalCentering
- **Alignment** : fill, leading, top, firstBaseline, center, trailing, bottom, lastBaseline

---

### 4. Navigation Avancée

#### Types de Navigation

```swift
// Navigation Controller
navigationController?.pushViewController(vc, animated: true)
navigationController?.popViewController(animated: true)

// Modal Presentation
present(vc, animated: true)
dismiss(animated: true)

// Presentation Styles (iOS 13+)
vc.modalPresentationStyle = .pageSheet
vc.modalPresentationStyle = .formSheet
vc.modalPresentationStyle = .fullScreen
```

#### Passing Data Between VCs

```swift
// Programmatique
let detailVC = DetailViewController()
detailVC.data = someData
navigationController?.pushViewController(detailVC, animated: true)

// Storyboard avec prepare(for:sender:)
override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
    if let detailVC = segue.destination as? DetailViewController {
        detailVC.data = someData
    }
}
```

---

### 5. Memory Management Avancé

#### ARC (Automatic Reference Counting)

- **Strong References** : Compteur +1
- **Weak References** : Ne comptent pas, deviennent nil
- **Unowned References** : Ne comptent pas, ne deviennent pas nil

#### Retain Cycles Classiques

```swift
// Parent-Child avec closures
class Parent {
    var child: Child?
    var completion: (() -> Void)?
    func setup() {
        child = Child()
        child?.parent = self // Strong reference cycle
        completion = { [weak self] in self?.doSomething() } // Weak capture
    }
}
class Child {
    weak var parent: Parent? // Weak reference
}
```

---

### 6. UIViewController Lifecycle Avancé

#### Ordre d'Exécution Complet

1. `loadView()` (si pas de Storyboard)
2. `viewDidLoad()`
3. `viewWillAppear(_:)`
4. `viewWillLayoutSubviews()`
5. `viewDidLayoutSubviews()`
6. `viewDidAppear(_:)`
7. `viewWillDisappear(_:)`
8. `viewDidDisappear(_:)`
9. `viewDidUnload()` (deprecated)

#### Utilisation Correcte

```swift
override func viewDidLoad() {
    super.viewDidLoad()
    // Setup one-time: outlets, delegates, observers
}
override func viewWillAppear(_ animated: Bool) {
    super.viewWillAppear(animated)
    // Setup recurring: refresh data, start timers
}
override func viewDidLayoutSubviews() {
    super.viewDidLayoutSubviews()
    // Frame-dependent calculations
}
```

---

### 7. Collection Views Avancées

#### Modern Collection Views (iOS 13+)

```swift
// Compositional Layout
func createLayout() -> UICollectionViewLayout {
    let itemSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(0.5),
        heightDimension: .fractionalHeight(1.0)
    )
    let item = NSCollectionLayoutItem(layoutSize: itemSize)
    let groupSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(1.0),
        heightDimension: .absolute(200)
    )
    let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])
    let section = NSCollectionLayoutSection(group: group)
    return UICollectionViewCompositionalLayout(section: section)
}
```

#### Diffable Data Source

```swift
typealias DataSource = UICollectionViewDiffableDataSource
typealias Snapshot = NSDiffableDataSourceSnapshot
var dataSource: DataSource!
func configureDataSource() {
    dataSource = DataSource(collectionView: collectionView) { collectionView, indexPath, item in
        // Configure cell
    }
}
```

---

### 8. Grand Central Dispatch (GCD)

#### Queues et Threading

```swift
// Main Queue (UI Updates)
DispatchQueue.main.async {
    self.label.text = "Updated"
}

// Background Queue
DispatchQueue.global(qos: .background).async {
    // Heavy work
    DispatchQueue.main.async {
        // Update UI
    }
}

// Custom Queue
let customQueue = DispatchQueue(label: "com.app.myqueue", qos: .utility)
```

#### Quality of Service

- **userInteractive** : UI, événements utilisateur
- **userInitiated** : Actions initiées par l'utilisateur
- **utility** : Tâches longues avec progress
- **background** : Tâches non visibles par l'utilisateur

---

### 9. Swift Generics Avancés

#### Generic Functions et Types

```swift
func swapTwoValues<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

struct Stack<Element> {
    private var items = [Element]()
    mutating func push(_ item: Element) { items.append(item) }
    mutating func pop() -> Element? { return items.popLast() }
}
```

#### Type Constraints

```swift
func findIndex<T: Equatable>(of valueToFind: T, in array: [T]) -> Int? {
    for (index, value) in array.enumerated() {
        if value == valueToFind { return index }
    }
    return nil
}
```

---

### 10. Error Handling Avancé

#### Types d'Error Handling

```swift
// throws/try/catch
func processFile() throws -> String {
    guard let data = loadFile() else { throw FileError.notFound }
    return process(data)
}
do {
    let result = try processFile()
} catch FileError.notFound {
    print("File not found")
} catch {
    print("Other error: \(error)")
}

// Result Type
func fetchData(completion: @escaping (Result<Data, NetworkError>) -> Void) {
    // Network call
    if success {
        completion(.success(data))
    } else {
        completion(.failure(.networkUnavailable))
    }
}
```

---

### 11. SwiftUI Integration (Important pour iOS 13+)

#### UIHostingController

```swift
import SwiftUI
// Intégrer SwiftUI dans UIKit
let swiftUIView = MySwiftUIView()
let hostingController = UIHostingController(rootView: swiftUIView)
addChild(hostingController)
view.addSubview(hostingController.view)
hostingController.didMove(toParent: self)
```

#### UIViewRepresentable

```swift
struct UIKitViewRepresentable: UIViewRepresentable {
    func makeUIView(context: Context) -> UILabel {
        let label = UILabel()
        label.text = "Hello from UIKit"
        return label
    }
    func updateUIView(_ uiView: UILabel, context: Context) {
        // Update the view
    }
}
```

---

## Questions d'Entraînement Avancées

### Question 1 - Protocols & Generics

**Que permet `associatedtype` et comment l'utilise-t-on ?**  
`associatedtype` permet de définir un type générique dans un protocol, qui sera précisé par chaque type conforme. Cela rend le protocol flexible et réutilisable pour différents types de données.

**Exemple d’utilisation :**
```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}

struct IntStack: Container {
    var items = [Int]()
    mutating func append(_ item: Int) { items.append(item) }
    var count: Int { items.count }
    subscript(i: Int) -> Int { items[i] }
}
```

---

### Question 2 - Closures & Memory

**Quel est le problème et comment le résoudre ?**  
Le problème est un risque de cycle de rétention (retain cycle) car la closure capturée par `dataTask` retient fortement `self`. Si `NetworkManager` n’est jamais libéré, cela cause une fuite mémoire.

**Solution :**  
Capturer `self` faiblement dans la closure :
```swift
URLSession.shared.dataTask(with: url) { [weak self] data, _, _ in
    self?.completion?(data)
}.resume()
```

---

### Question 3 - Auto Layout

**Pourquoi cette ligne est-elle nécessaire lors de l'utilisation d'Auto Layout par code ?**  
`view.translatesAutoresizingMaskIntoConstraints = false` désactive la génération automatique des contraintes par le système. Cela permet d’utiliser uniquement les contraintes définies par Auto Layout, sinon les deux systèmes peuvent entrer en conflit.

---

### Question 4 - Collection Views

**Quelle est la différence entre `UICollectionViewFlowLayout` et `UICollectionViewCompositionalLayout` ?**  
- `UICollectionViewFlowLayout` : Layout classique, simple, en grille ou en liste, limité en personnalisation.
- `UICollectionViewCompositionalLayout` : Layout moderne (iOS 13+), permet de créer des interfaces complexes et dynamiques avec plusieurs sections, groupes et items, très flexible.

---

### Question 5 - Threading

**Quel est le problème avec ce code ?**  
On essaie de modifier l’interface (`self.label.text`) depuis un thread secondaire, ce qui peut provoquer des bugs ou des crashs.

**Correction :**
```swift
DispatchQueue.global().async {
    let result = heavyComputation()
    DispatchQueue.main.async {
        self.label.text = result // ✅
    }
}
```

---

## Points Critiques pour le QCM

### Pièges Classiques

1. **UI Updates sur background thread**  
   Les modifications de l’interface utilisateur doivent toujours être faites sur le thread principal.  
   **Exemple :**
   ```swift
   // Incorrect : mise à jour sur un thread secondaire
   DispatchQueue.global().async {
       self.label.text = "Hello" // Incorrect
   }
   // Correct : on repasse sur le main thread
   DispatchQueue.global().async {
       let result = heavyComputation()
       DispatchQueue.main.async {
           self.label.text = result // Correct
       }
   }
   ```

2. **Retain cycles avec self dans les closures**  
   Si une closure capture `self` fortement, cela peut empêcher la libération de la mémoire (cycle de rétention).  
   **Exemple :**
   ```swift
   // Incorrect
   someAsyncMethod {
       self.doSomething() // Incorrect
   }
   // Correct
   someAsyncMethod { [weak self] in
       self?.doSomething() // Correct
   }
   ```

3. **Force unwrapping vs safe unwrapping**  
   Utiliser `!` sur un optional peut provoquer un crash si la valeur est nil.  
   **Exemple :**
   ```swift
   let name: String? = nil
   print(name!) // Crash
   // Correct
   if let safeName = name {
       print(safeName) // Correct
   }
   ```

4. **Delegate references : toujours weak**  
   Les delegates doivent être déclarés `weak` pour éviter les cycles de rétention.  
   **Exemple :**
   ```swift
   // Correct
   weak var delegate: MyDelegate? // Correct
   // Incorrect
   var delegate: MyDelegate? // Incorrect
   ```

5. **Collection View cells : dequeueReusableCell vs création nouvelle**  
   Toujours utiliser `dequeueReusableCell` pour réutiliser les cellules et optimiser la mémoire.  
   **Exemple :**
   ```swift
   // Correct
   let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath) // Correct
   // Incorrect
   let cell = UITableViewCell(style: .default, reuseIdentifier: nil) // Incorrect
   ```

---

### Sujets Hot

- **iOS 13+ features**  
  Introduction du Scene Delegate (gestion des scènes), nouveaux styles de présentation modale, prise en charge du Dark Mode.
- **Combine Framework**  
  Permet la programmation réactive avec des Publishers et Subscribers pour gérer les flux de données asynchrones.
- **SwiftUI/UIKit integration**  
  Utilisation de `UIHostingController` pour intégrer des vues SwiftUI dans UIKit.
- **Modern Collection Views**  
  Utilisation de `UICollectionViewCompositionalLayout` pour des layouts complexes et `Diffable Data Source` pour des mises à jour efficaces.
- **Swift 5+ features**  
  Ajout des Property Wrappers (`@State`, `@Published`), Function Builders (utilisés dans SwiftUI).

---

### À Réviser Absolument

1. **Protocol-Oriented Programming**  
   Utiliser les protocols pour structurer et réutiliser le code.
2. **Memory Management (ARC, weak/strong/unowned)**  
   Comprendre comment Swift gère la mémoire et éviter les cycles de rétention.
3. **Concurrency (GCD, OperationQueue)**  
   Exécuter du code en parallèle et gérer les threads.
4. **Auto Layout (Priorities, Content Hugging/Compression Resistance)**  
   Maîtriser la disposition dynamique des vues et les priorités de contraintes.
5. **Modern UIKit APIs**  
   Savoir utiliser les dernières API UIKit pour des interfaces modernes
