using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Media.Media3D;

namespace DortanApp
{
    /// <summary>
    /// Logique d'interaction pour UCVisuReserver.xaml
    /// </summary>
    public partial class UCVisuReserver : UserControl
    {
        public UCVisuReserver()
        {
            InitializeComponent();

            dgReservations.Items.Filter = ContientMotClef;
        }

        private bool ContientMotClef(object obj)
        {
            Reservation reservation = obj as Reservation;
            if (reservation == null)
                return false;

            bool nomFiltre = string.IsNullOrEmpty(txtNom.Text) || reservation.Activite.Nom.StartsWith(txtNom.Text, StringComparison.OrdinalIgnoreCase);
            bool dateFiltre = string.IsNullOrEmpty(txtDate.Text) || reservation.DateReservation.ToString("dd/MM/yyyy").StartsWith(txtDate.Text, StringComparison.OrdinalIgnoreCase);

            return nomFiltre && dateFiltre;
        }

        private void TxtNom_TextChanged(object sender, TextChangedEventArgs e)
        {
            CollectionViewSource.GetDefaultView(dgReservations.ItemsSource).Refresh();
        }

        private void TxtDate_TextChanged(object sender, TextChangedEventArgs e)
        {
            CollectionViewSource.GetDefaultView(dgReservations.ItemsSource).Refresh();
        }

        private void DgReservations_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (dgReservations.SelectedItem != null)
            {
                int coutTotal = 0;

                Reservation reservationSelectionne = (Reservation)dgReservations.SelectedItem;
                int duree = reservationSelectionne.DureeReservation;

                int nombreMateriels = reservationSelectionne.LesMateriels.Count;
                int coutUtilisationTotal = 0;

                for (int i = 0; i < nombreMateriels; i++)
                {
                    Materiel materiel = reservationSelectionne.LesMateriels[i];
                    int cout = materiel.CoutUtilisation;
                    coutUtilisationTotal += cout;
                }

                coutTotal += coutUtilisationTotal * duree;

                string detailsReservation = $"Durée de la réservation : {duree} heure(s)\n" +
                                            $"Nombre de matériels réservés : {nombreMateriels}\n" +
                                            $"Coût total de l'utilisation des matériels : {coutUtilisationTotal} €";

                MessageBox.Show($"Le coût de la réservation est de : {coutTotal:F2} €. \nDétails : \n{detailsReservation}");
            }
        }

        private void BtSupReservation_Click(object sender, RoutedEventArgs e)
        {
            Reservation reservationSelectionne = dgReservations.SelectedItem as Reservation;

            if (reservationSelectionne == null)
            {
                MessageBox.Show("Veuillez sélectionner une réservation");
                return;
            }

            MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.SupReservation(reservationSelectionne);
        }
    }
}