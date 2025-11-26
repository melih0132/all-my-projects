protocol ButtonListener {
    func clicked()
}

class Button {
    var listener: ButtonListener?

    func onClick() {
        listener?.clicked()
    }
}

class MyInterface: ButtonListener {
    var someButton: Button

    init(button: Button) {
        someButton = button
    }

    func clicked() {
        print("A button has been clicked !")
    }
}

let myButton = Button()
let interface = MyInterface(button: myButton)

// Ligne à ajouter :
myButton.listener = interface

myButton.onClick()
