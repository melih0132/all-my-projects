final class Queue<T> {
    private var storage: [T] = []  // Stockage des éléments de la queue

    // Abonnements (closures) pour notifier des événements
    var onEnqueue: ((T) -> Void)?  // Closure appelée lors de l'ajout d'un élément
    var onDequeue: ((T) -> Void)?  // Closure appelée lors de la suppression d'un élément

    // Propriétés calculées
    var isEmpty: Bool { storage.isEmpty }  // Vérifie si la queue est vide
    var count: Int { storage.count }  // Renvoie le nombre d'éléments dans la queue
    var peek: T? { storage.first }  // Renvoie le premier élément sans le retirer

    // Ajoute un élément à la queue
    func enqueue(_ element: T) {
        storage.append(element)  // Ajoute l'élément à la fin du tableau
        onEnqueue?(element)  // Notifie via la closure, si elle est définie
    }

    // Retire et renvoie le premier élément de la queue
    @discardableResult  // Indique que le résultat peut être ignoré
    func dequeue() -> T? {
        guard !storage.isEmpty else { return nil }  // Vérifie si la queue est vide
        let first = storage.removeFirst()  // Retire le premier élément
        onDequeue?(first)  // Notifie via la closure, si elle est définie
        return first  // Renvoie l'élément retiré
    }
}

// Démo d'utilisation de la Queue
let q = Queue<Int>()  // Crée une instance de Queue pour des entiers
q.onEnqueue = { print("Enqueue:", $0) }  // Closure pour gérer l'événement d'ajout
q.onDequeue = { print("Dequeue:", $0) }  // Closure pour gérer l'événement de retrait

// Ajout d'éléments à la queue
q.enqueue(10)  // Ajoute 10 et déclenche la closure onEnqueue
q.enqueue(20)  // Ajoute 20 et déclenche la closure onEnqueue
print("peek:", q.peek ?? -1)  // Affiche le premier élément (20), ou -1 si la queue est vide
_ = q.dequeue()  // Retire le premier élément (10) et déclenche la closure onDequeue
_ = q.dequeue()  // Retire le prochain élément (20) et déclenche la closure onDequeue
print("empty:", q.isEmpty)  // Affiche si la queue est vide (true)