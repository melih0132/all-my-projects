using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace DortanApp
{
    /// <summary>
    /// Logique d'interaction pour UCMateriel.xaml
    /// </summary>
    public partial class UCMateriel : UserControl
    {
        private List<Materiel> materielsSelectionnes = new List<Materiel>();

        public UCMateriel()
        {
            InitializeComponent();

            clSelection.Visibility = Visibility.Hidden;

            dbMateriel.Items.Filter = ContientMotClef;
        }

        private void MaterielSelectionne(object sender, RoutedEventArgs e)
        {
            Materiel materiel = ((CheckBox)sender).DataContext as Materiel;
            if (materiel != null)
            {
                if (((CheckBox)sender).IsChecked == true)
                {
                    materielsSelectionnes.Add(materiel);
                }
                else
                {
                    materielsSelectionnes.Remove(materiel);
                }
            }
        }

        private void DbMateriel_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (dbMateriel.SelectedItem != null)
            {
                Materiel materielSelectionne = (Materiel)dbMateriel.SelectedItem;
                AfficherDetailsMateriel(materielSelectionne);
            }
        }

        private void AfficherDetailsMateriel(Materiel materiel)
        {
            DetailsMateriel details = new DetailsMateriel();
            details.AfficherDetails(materiel);
            details.ShowDialog();
        }

        private void BtValider_Click(object sender, RoutedEventArgs e)
        {
            MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;

            if (materielsSelectionnes.Count > 0)
            {
                List<Materiel> materielsCopie = new List<Materiel>(materielsSelectionnes);

                foreach (Materiel materiel in materielsCopie)
                {
                    mainWindow.AjouterMaterielReservation(materiel);

                    materielsSelectionnes.Remove(materiel);
                }

                TabControl tabControl = mainWindow.tcMain;
                tabControl.SelectedIndex = 1;
            }
            else
            {
                MessageBox.Show("Aucun matériel n'a été sélectionné");
            }
        }

        private bool ContientMotClef(object obj)
        {
            Materiel materiel = obj as Materiel;
            if (materiel == null)
                return false;

            bool typeFiltre = string.IsNullOrEmpty(txtType.Text) || materiel.TypeMateriel.Nom.StartsWith(txtType.Text, StringComparison.OrdinalIgnoreCase);
            bool categorieFiltre = string.IsNullOrEmpty(txtCategorie.Text) || materiel.NomCategorie.Nom.StartsWith(txtCategorie.Text, StringComparison.OrdinalIgnoreCase);
            bool siteFiltre = string.IsNullOrEmpty(txtSite.Text) || materiel.Site.Nom.StartsWith(txtSite.Text, StringComparison.OrdinalIgnoreCase);

            return typeFiltre && categorieFiltre && siteFiltre;
        }

        private void TxtType_TextChanged(object sender, TextChangedEventArgs e)
        {
            RafraichirVue();
        }

        private void TxtCategorie_TextChanged(object sender, TextChangedEventArgs e)
        {
            RafraichirVue();
        }

        private void TxtSite_TextChanged(object sender, TextChangedEventArgs e)
        {
            RafraichirVue();
        }

        private void RafraichirVue()
        {
            CollectionViewSource.GetDefaultView(dbMateriel.ItemsSource).Refresh();
        }

        public void ChangerVisibilte()
        {
            clSelection.Visibility = Visibility.Visible;
            
            foreach (var item in clFiltreEtBt.Children)
            {
                btValider.Visibility = Visibility.Visible;
            }
        }
    }
}