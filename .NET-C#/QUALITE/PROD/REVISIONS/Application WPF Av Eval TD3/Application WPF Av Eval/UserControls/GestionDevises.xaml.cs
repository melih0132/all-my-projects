using Application_WPF_Av_Eval.Models;
using Application_WPF_Av_Eval.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Application_WPF_Av_Eval.UserControls
{
    /// <summary>
    /// Logique d'interaction pour GestionDevises.xaml
    /// </summary>
    public partial class GestionDevises : UserControl
    {

        private ObservableCollection<Devise> devises;
        public GestionDevises()
        {
            InitializeComponent();
            devises = new ObservableCollection<Devise>(Service.ChargerDevises());
            DeviseListView.ItemsSource = devises;
        }

        // Méthode pour ajouter une devise
        private void AjouterDevise_Click(object sender, RoutedEventArgs e)
        {
            if (double.TryParse(TauxTextBox.Text, out double taux) && !string.IsNullOrEmpty(NomDeviseTextBox.Text))
            {
                devises.Add(new Devise { NomDevise = NomDeviseTextBox.Text, Taux = taux });
                Service.SauvegarderDevises(devises.ToList()); // Mise à jour du fichier JSON après ajout
            }
            else
            {
                MessageBox.Show("Veuillez entrer un nom de devise valide et un taux de conversion.");
            }
        }

        // Méthode pour supprimer une devise
        private void SupprimerDevise_Click(object sender, RoutedEventArgs e)
        {
            // Récupérer la devise depuis le CommandParameter
            if (sender is Button button && button.CommandParameter is Devise deviseToRemove)
            {
                devises.Remove(deviseToRemove);
                Service.SauvegarderDevises(devises.ToList()); // Mise à jour du fichier JSON après suppression
            }
            else
            {
                MessageBox.Show("Impossible de supprimer la devise.");
            }
        }

        // Méthode pour mettre à jour le fichier JSON
        private void MettreAJourJSON_Click(object sender, RoutedEventArgs e)
        {
            Service.SauvegarderDevises(devises.ToList());
            MessageBox.Show("Le fichier JSON a été mis à jour avec succès.");
        }
    }
}
