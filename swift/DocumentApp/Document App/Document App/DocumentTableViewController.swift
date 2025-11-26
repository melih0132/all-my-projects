//
//  DocumentTableViewController.swift
//  Document App
//
//  Created by Melih CETINKAYA on 9/10/25.
//

import UIKit

class DocumentTableViewController: UITableViewController {
    
    // MARK: - Modèle de données
    struct DocumentFile {
        let title: String
        let size: Int
        let imageName: String?
        let url: URL
        let type: String
    }
    
    // Tableau des documents trouvés dans le bundle
    var documents: [DocumentFile] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Mes Documents"
        
        // Charger les documents depuis le bundle
        documents = listFileInBundle()
    }
    
    // MARK: - Table view data source
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return documents.count
    }

    override func tableView(_ tableView: UITableView,
                            cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "DocumentCell", for: indexPath)
        
        let document = documents[indexPath.row]
        
        // Nom du fichier
        cell.textLabel?.text = document.title
        
        // Taille formatée
        cell.detailTextLabel?.text = "Taille : \(document.size.formattedSize)"
        
        cell.accessoryType = .disclosureIndicator
        return cell
    }
    
    // MARK: - Récupérer les fichiers du bundle
    func listFileInBundle() -> [DocumentFile] {
        let fm = FileManager.default
        let path = Bundle.main.resourcePath!
        let items = try! fm.contentsOfDirectory(atPath: path)
        
        var documentListBundle = [DocumentFile]()
        
        for item in items {
            if !item.hasSuffix("DS_Store") && item.hasSuffix(".jpg") {
                let currentUrl = URL(fileURLWithPath: path + "/" + item)
                let resourcesValues = try! currentUrl.resourceValues(forKeys: [.contentTypeKey, .nameKey, .fileSizeKey])
                
                documentListBundle.append(DocumentFile(
                    title: resourcesValues.name!,
                    size: resourcesValues.fileSize ?? 0,
                    imageName: item,
                    url: currentUrl,
                    type: resourcesValues.contentType!.description)
                )
            }
        }
        return documentListBundle
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Vérifier que c’est le bon Segue
        if segue.identifier == "ShowDocumentSegue" {
            // 1. Récupérer l'index de la ligne sélectionnée
            if let indexPath = tableView.indexPathForSelectedRow {
                // 2. Récupérer le document correspondant à l'index
                let selectedDocument = documents[indexPath.row]
                
                // 3. Cibler l'instance de DocumentViewController via segue.destination
                // 4. Caster le segue.destination en DocumentViewController
                if let detailVC = segue.destination as? DocumentDetailViewController {
                    // 5. Remplir la variable imageName avec le nom de l'image du document
                    detailVC.imageName = selectedDocument.imageName
                }
            }
        }
    }
}

// MARK: - Extension pour formater les tailles
extension Int {
    var formattedSize: String {
        let formatter = ByteCountFormatter()
        formatter.countStyle = .file
        return formatter.string(fromByteCount: Int64(self))
    }
}
