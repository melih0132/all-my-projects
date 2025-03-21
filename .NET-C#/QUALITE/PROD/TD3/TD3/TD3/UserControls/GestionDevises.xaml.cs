using System.Collections.ObjectModel;
using System.Windows;
using System.Windows.Controls;
using System.Collections.Generic; // Import nécessaire pour la conversion en List
using System.Linq;
using TD3;

namespace TD3.UserControls
{
    public partial class GestionDevises : UserControl
    {
        private ObservableCollection<Devise> devises;

        public GestionDevises()
        {
            InitializeComponent();

            // Chargement des devises depuis le service
            devises = new ObservableCollection<Devise>(Service.ChargerDevises());
            DeviseListView.ItemsSource = devises;
        }

        private void AjouterDevise_Click(object sender, RoutedEventArgs e)
        {
            if (double.TryParse(TauxTextBox.Text, out double taux) && !string.IsNullOrWhiteSpace(NomDeviseTextBox.Text))
            {
                // Vérification de l'existence de la devise avant l'ajout
                if (devises.Any(d => d.NomDevise.Equals(NomDeviseTextBox.Text, StringComparison.OrdinalIgnoreCase)))
                {
                    MessageBox.Show("Cette devise existe déjà dans la liste.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                // Ajout de la nouvelle devise à la liste
                devises.Add(new Devise { NomDevise = NomDeviseTextBox.Text, Taux = taux });
                Service.SauvegarderDevises(devises.ToList());
            }
            else
            {
                MessageBox.Show("Veuillez entrer un nom de devise valide et un taux de conversion.", "Ajout", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void SupprimerDevise_Click(object sender, RoutedEventArgs e)
        {
            if (DeviseListView.SelectedItem is Devise selectedDevise)
            {
                devises.Remove(selectedDevise);
                Service.SauvegarderDevises(devises.ToList());
            }
            else
            {
                MessageBox.Show("Veuillez sélectionner une devise à supprimer.", "Suppression", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void MettreAJourJSON_Click(object sender, RoutedEventArgs e)
        {
            if (devises.Any())
            {
                Service.SauvegarderDevises(devises.ToList());
                MessageBox.Show("Le fichier JSON a été mis à jour avec succès.", "Mise à jour", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            else
            {
                MessageBox.Show("Aucune devise à sauvegarder. Veuillez ajouter des devises avant de mettre à jour le fichier JSON.", "Information", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }
    }
}
