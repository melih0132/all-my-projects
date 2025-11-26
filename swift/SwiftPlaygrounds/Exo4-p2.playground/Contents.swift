class Button {
    var onClickClosure: (() -> Void)?

    func onClick() {
        onClickClosure?()
    }
}

class MyInterface {
    var someButton: Button

    init(button: Button) {
        someButton = button

        // On définit ici la closure de réponse au clic
        someButton.onClickClosure = {
            print("A button has been clicked !")
        }
    }
}

let myButton = Button()
let interface = MyInterface(button: myButton)

myButton.onClick()
