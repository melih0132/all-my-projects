using System.Windows;
using System.Windows.Controls;
using TD3;

namespace TD3.UserControls
{
    public partial class ConvertisseurDevise : UserControl
    {
        private List<Devise> devises;

        public ConvertisseurDevise()
        {
            InitializeComponent();

            devises = Service.ChargerDevises();
            DeviseComboBox.ItemsSource = devises;
            DeviseComboBox.DisplayMemberPath = "NomDevise";
        }

        private void Convertir_Click(object sender, RoutedEventArgs e)
        {
            if (DeviseComboBox.SelectedItem is Devise selectedDevise && double.TryParse(MontantEuroTextBox.Text, out double montantEuro))
            {
                double resultat = montantEuro * selectedDevise.Taux;
                ResultatTextBox.Text = resultat.ToString("F2");
            }
            else
            {
                MessageBox.Show("Veuillez entrer un montant valide et sélectionner une devise.");
            }
        }
    }
}
