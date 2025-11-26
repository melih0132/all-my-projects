//
//  TrainerDetailViewController.swift
//  Pokémon Trainer Manager
//
//  Created by Melih CETINKAYA on 9/10/25.
//

import UIKit
import QuickLook

// MARK: - TrainerDetailViewController
class TrainerDetailViewController: UIViewController {
    
    @IBOutlet weak var headerImageView: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var badgeCollection: UICollectionView!
    @IBOutlet weak var tableView: UITableView!
    
    var trainer: Trainer!
    weak var selectionDelegate: PokemonSelectionDelegate?
    
    private var previewItemURL: URL?
        
    override func viewDidLoad() {
        super.viewDidLoad()
        title = trainer.name
        
        // Image et nom
        headerImageView.image = UIImage(named: trainer.photoName) ?? UIImage(systemName: "person.crop.circle")
        nameLabel.text = trainer.name
        nameLabel.font = UIFont.systemFont(ofSize: 20, weight: .medium)
        nameLabel.textColor = .label
        
        // Collection View
        badgeCollection.dataSource = self
        badgeCollection.delegate = self
        badgeCollection.register(UICollectionViewCell.self, forCellWithReuseIdentifier: "BadgeCell")
        
        // Table View
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "PokemonCell")
        tableView.dataSource = self
        tableView.delegate = self
    }
}

// MARK: - UITableView
extension TrainerDetailViewController: UITableViewDataSource, UITableViewDelegate {

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return trainer.pokemons.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        let cell = tableView.dequeueReusableCell(withIdentifier: "PokemonCell", for: indexPath)
        let pokemon = trainer.pokemons[indexPath.row]
        
        // Texte simple
        cell.textLabel?.text = "\(pokemon.name) (Lv.\(pokemon.level)) - \(pokemon.type)"
        cell.textLabel?.font = UIFont.systemFont(ofSize: 16)
        cell.textLabel?.textColor = .label
        
        // Image simple
        cell.imageView?.image = UIImage(named: pokemon.imageName) ?? UIImage(systemName: "bolt.circle")
        cell.accessoryType = .disclosureIndicator
        
        return cell
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let selectedPokemon = trainer.pokemons[indexPath.row]
        performSegue(withIdentifier: "ShowPokemonDetailSegue", sender: selectedPokemon)
    }
}

// MARK: - Segue
extension TrainerDetailViewController {

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "ShowPokemonDetailSegue",
           let detailVC = segue.destination as? PokemonDetailViewController,
           let pokemon = sender as? Pokemon {
            detailVC.pokemon = pokemon
        }
    }
}

// MARK: - UICollectionView
extension TrainerDetailViewController: UICollectionViewDataSource, UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return trainer.badges.count
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "BadgeCell", for: indexPath)
        
        cell.contentView.subviews.forEach { $0.removeFromSuperview() }
        
        let badge = trainer.badges[indexPath.item]
        let imageView = UIImageView(image: UIImage(named: badge.imageName) ?? UIImage(systemName: "seal"))
        imageView.contentMode = .scaleAspectFit
        imageView.translatesAutoresizingMaskIntoConstraints = false
        cell.contentView.addSubview(imageView)
        
        NSLayoutConstraint.activate([
            imageView.widthAnchor.constraint(equalToConstant: 40),
            imageView.heightAnchor.constraint(equalToConstant: 40),
            imageView.centerXAnchor.constraint(equalTo: cell.contentView.centerXAnchor),
            imageView.centerYAnchor.constraint(equalTo: cell.contentView.centerYAnchor)
        ])
        
        return cell
    }
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        let badge = trainer.badges[indexPath.item]
        
        if let image = UIImage(named: badge.imageName),
           let data = image.pngData() {
            let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("\(badge.imageName).png")
            try? data.write(to: tempURL)
            previewItemURL = tempURL
            
            let previewController = QLPreviewController()
            previewController.dataSource = self
            present(previewController, animated: true, completion: nil)
        }
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: 50, height: 50)
    }
}

// MARK: - QLPreviewController
extension TrainerDetailViewController: QLPreviewControllerDataSource {
    func numberOfPreviewItems(in controller: QLPreviewController) -> Int {
        return previewItemURL == nil ? 0 : 1
    }
    
    func previewController(_ controller: QLPreviewController, previewItemAt index: Int) -> QLPreviewItem {
        return previewItemURL! as NSURL
    }
}
