using System;
using System.Collections.Generic;
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

namespace DortanApp
{
    /// <summary>
    /// Logique d'interaction pour UCReservation.xaml
    /// </summary>
    public partial class UCReservation : UserControl
    {
        public UCReservation()
        {
            InitializeComponent();

            dgActivites.Items.Filter = ContientMotClef;
        }

        private void BtReserver_Click(object sender, RoutedEventArgs e)
        {
            if (dgActivites.SelectedItem == null)
            {
                MessageBox.Show("Veuillez sélectionner une activité");
                return;
            }

            if (dpDate.SelectedDate == null || dpDate.SelectedDate < DateTime.Today)
            {
                MessageBox.Show("Veuillez sélectionner une date de réservation valide");
                return;
            }

            if (string.IsNullOrWhiteSpace(tbDuree.Text))
            {
                MessageBox.Show("Veuillez entrer une durée pour la réservation");
                return;
            }

            if (!int.TryParse(tbDuree.Text, out int dureeReservation) || dureeReservation <= 0)
            {
                MessageBox.Show("Veuillez entrer une durée de réservation valide");
                return;
            }

            Activite activiteSelectionnee = dgActivites.SelectedItem as Activite;
            DateTime dateReservation = dpDate.SelectedDate.Value;

            Reservation nvReservation = new Reservation(activiteSelectionnee, dateReservation, dureeReservation);

            MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.CreationReservation(nvReservation);

            dpDate.SelectedDate = null;
            dgActivites.SelectedItem = null;
            tbDuree.Text = "";

            TabControl tabControl = mainWindow.tcMain;
            TabItem tabItem = tabControl.Items[3] as TabItem;

            UCMateriel uCMateriel = tabItem.Content as UCMateriel;

            if (uCMateriel != null)
            {
                uCMateriel.ChangerVisibilte();
                tabControl.SelectedIndex = 3;
            }
        }

        private void BtSupActivite_Click(object sender, RoutedEventArgs e)
        {
            Activite activiteSelectionne = dgActivites.SelectedItem as Activite;

            if (activiteSelectionne == null)
            {
                MessageBox.Show("Veuillez sélectionner une activité");
                return;
            }

            MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;
            mainWindow.SupActivite(activiteSelectionne);
        }

        private void BtCreationActivite_Click(object sender, RoutedEventArgs e)
        {
            MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;
            TabControl tabControl = mainWindow.tcMain;
            tabControl.SelectedIndex = 2;
        }

        private bool ContientMotClef(object obj)
        {
            Activite unActivité = obj as Activite;
            if (String.IsNullOrEmpty(txtNom.Text))
                return true;
            else
                return unActivité.Nom.StartsWith(txtNom.Text, StringComparison.OrdinalIgnoreCase);
        }

        private void TxtNom_TextChanged(object sender, TextChangedEventArgs e)
        {
            CollectionViewSource.GetDefaultView(dgActivites.ItemsSource).Refresh();
        }
    }
}
