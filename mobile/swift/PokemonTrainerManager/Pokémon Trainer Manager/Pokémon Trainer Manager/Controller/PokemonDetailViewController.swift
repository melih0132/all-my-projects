//
//  PokemonDetailViewController.swift
//  Pokémon Trainer Manager
//
//  Created by Melih CETINKAYA on 9/10/25.
//

import UIKit

// MARK: - PokemonDetailViewController
class PokemonDetailViewController: UIViewController {

    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var typeLabel: UILabel!

    var pokemon: Pokemon! {
        didSet {
            if isViewLoaded {
                displayPokemonInfo()
            }
        }
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        displayPokemonInfo()
    }

    private func displayPokemonInfo() {
        guard let pokemon else { return }

        title = pokemon.name

        // Nom + niveau sur une seule ligne
        nameLabel.text = "\(pokemon.name)  (Lv.\(pokemon.level))"
        nameLabel.font = UIFont.boldSystemFont(ofSize: 20)
        nameLabel.textColor = .label

        // Type en clair
        typeLabel.text = "Type : \(pokemon.type)"
        typeLabel.font = UIFont.systemFont(ofSize: 16)
        typeLabel.textColor = .secondaryLabel

        // Image simple
        imageView.image = UIImage(named: pokemon.imageName) ?? UIImage(systemName: "bolt.circle")
        imageView.contentMode = .scaleAspectFit
    }
}
