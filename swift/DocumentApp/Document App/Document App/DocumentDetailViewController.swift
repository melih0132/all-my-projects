import UIKit

class DocumentDetailViewController: UIViewController {

    // Outlet lié à l’ImageView du storyboard
    @IBOutlet weak var imageView: UIImageView!

    // Variable pour stocker le nom de l'image reçue depuis la TableView
    var imageName: String?

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Vérifier que imageName n'est pas nil
        if let name = imageName {
            // Afficher l'image dans l'ImageView
            imageView.image = UIImage(named: name)
        }
    }
}
