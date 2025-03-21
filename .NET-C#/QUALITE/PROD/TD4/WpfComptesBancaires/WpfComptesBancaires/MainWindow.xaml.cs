using System.Text;
using BusinessLayer;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Collections.ObjectModel;
using System.Numerics;
using System.Reflection.Metadata;

namespace WpfComptesBancaires
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        public ObservableCollection<string> OperationTypes { get; set; }
        public ObservableCollection<Compte> Comptes { get; set; }
        public MainWindow()
        {
            InitializeComponent();
            this.DataContext = this;
            ServiceCompte serviceCompte = new ServiceCompte();

            OperationTypes = new ObservableCollection<string> { "Retrait", "Depot", "Virement"};

            Comptes = new ObservableCollection<Compte>(serviceCompte.GetAllComptes());
            Console.WriteLine(serviceCompte.GetAllComptes().Count());
        }

        private void boutonValider_Click(object sender, RoutedEventArgs e)
        {
            string montantText = textMontant.Text;
            string operation = comboOperation.Text;
            string compte = comboComptes.Text;

            double montant;
            int idCompte;

            if (string.IsNullOrWhiteSpace(montantText) ||
                string.IsNullOrWhiteSpace(compte) ||
                string.IsNullOrWhiteSpace(operation))
            {
                MessageBox.Show("Tous les champs doivent être remplis.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (!double.TryParse(montantText, out montant))
            {
                MessageBox.Show("Veuillez entrer un montant valide.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (!int.TryParse(compte, out idCompte))
            {
                MessageBox.Show("Veuillez sélectionner un compte valide.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            ServiceCompte service = new ServiceCompte();

            try
            {
                switch (operation)
                {
                    case "Depot":
                        service.SetDebitCredit(idCompte, montant);
                        MessageBox.Show("Dépôt effectué avec succès.", "Succès", MessageBoxButton.OK, MessageBoxImage.Information);
                        break;

                    case "Retrait":
                        if (montant > 0) montant = -montant;
                        service.SetDebitCredit(idCompte, montant);
                        MessageBox.Show("Retrait effectué avec succès.", "Succès", MessageBoxButton.OK, MessageBoxImage.Information);
                        break;

                    case "Virement":
                        if (!int.TryParse(comboCompteDestinataire.Text, out int idCompteDestinataire))
                        {
                            MessageBox.Show("Veuillez sélectionner un compte destinataire valide.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                            return;
                        }

                        service.Virement(idCompte, idCompteDestinataire, montant);
                        MessageBox.Show("Virement effectué avec succès.", "Succès", MessageBoxButton.OK, MessageBoxImage.Information);
                        break;

                    default:
                        MessageBox.Show("Opération inconnue.", "Erreur", MessageBoxButton.OK, MessageBoxImage.Warning);
                        break;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Une erreur est survenue : {ex.Message}", "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }
}