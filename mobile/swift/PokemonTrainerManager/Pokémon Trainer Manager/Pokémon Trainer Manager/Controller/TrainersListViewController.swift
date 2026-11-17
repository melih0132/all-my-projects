//
//  TrainersListViewController.swift
//  Pokémon Trainer Manager
//
//  Created by Melih CETINKAYA on 9/10/25.
//

import UIKit

// MARK: - Modèles Codable
struct Badge: Codable {
    let name: String
    let imageName: String
}

struct Pokemon: Codable {
    let name: String
    let type: String
    let imageName: String
    let level: Int
}

struct Trainer: Codable {
    let id: String
    let name: String
    let photoName: String
    var badges: [Badge]
    var pokemons: [Pokemon]
}

struct TrainersResponse: Codable {
    let trainers: [Trainer]
}

// MARK: - Data Loader
enum DataLoader {
    static func loadTrainers(fromFile fileName: String = "data") -> [Trainer] {
        guard let url = Bundle.main.url(forResource: fileName, withExtension: "json") else {
            print("Fichier \(fileName).json introuvable")
            return []
        }
        
        do {
            let data = try Data(contentsOf: url)
            let response = try JSONDecoder().decode(TrainersResponse.self, from: data)
            return response.trainers
        } catch {
            print("Erreur lors du décodage JSON : \(error)")
            return []
        }
    }
}


// MARK: - Protocole de délégation
protocol PokemonSelectionDelegate: AnyObject {
    func didSelectPokemon(_ pokemon: Pokemon, from trainer: Trainer)
}

// MARK: - TrainersListViewController
class TrainersListViewController: UIViewController {

    @IBOutlet weak var tableView: UITableView!
    private var trainers: [Trainer] = []

    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Dresseurs"

        tableView.dataSource = self
        tableView.delegate = self

        // Charger les données depuis data.json
        trainers = DataLoader.loadTrainers()
        tableView.reloadData()
    }

    // MARK: - Segue vers le détail
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "ShowTrainerDetailSegue" {
            if let indexPath = tableView.indexPathForSelectedRow {
                let selectedTrainer = trainers[indexPath.row]
                if let detailVC = segue.destination as? TrainerDetailViewController {
                    detailVC.trainer = selectedTrainer
                }
            }
        }
    }
}

// MARK: - UITableViewDataSource & Delegate
extension TrainersListViewController: UITableViewDataSource, UITableViewDelegate {

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return trainers.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        let cell = tableView.dequeueReusableCell(withIdentifier: "TrainerCell", for: indexPath)
        let trainer = trainers[indexPath.row]

        cell.textLabel?.text = "\(trainer.name) (\(trainer.pokemons.count) Pokémon • \(trainer.badges.count) Badges)"
        cell.imageView?.image = UIImage(named: trainer.photoName) ?? UIImage(systemName: "person.crop.circle")
        cell.accessoryType = .disclosureIndicator

        return cell
    }
}
