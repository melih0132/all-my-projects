class Button {
    let id: Int
    var onClickClosure: ((Int) -> Void)?  // Closure qui prend un entier (id) en paramètre

    init(id: Int) {
        self.id = id
    }

    func onClick() {
        onClickClosure?(id)
    }
}

class MyInterface {
    var buttons: [Button] = []

    init(buttonCount: Int) {
        for i in 1...buttonCount {
            let button = Button(id: i)

            // On définit la closure qui sera appelée lors d'un clic sur le bouton
            // On utilise [weak self] pour éviter une référence forte à l'instance de MyInterface
            button.onClickClosure = { [weak self] buttonID in
                // self? permet d'accéder à 'self' en toute sécurité
                // Si 'self' est nil (c'est-à-dire si l'instance a été désallouée), la closure ne sera pas exécutée
                self?.handleButtonClick(buttonID: buttonID)
            }

            buttons.append(button)
        }
    }

    func handleButtonClick(buttonID: Int) {
        print("Le bouton \(buttonID) a été cliqué.")
    }
}

let interface = MyInterface(buttonCount: 3)

// Simuler des clics
interface.buttons[0].onClick()
interface.buttons[1].onClick()
interface.buttons[2].onClick()