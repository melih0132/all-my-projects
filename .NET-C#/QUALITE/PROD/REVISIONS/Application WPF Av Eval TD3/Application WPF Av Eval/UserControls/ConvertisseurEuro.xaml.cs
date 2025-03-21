using Application_WPF_Av_Eval.Models;
using Application_WPF_Av_Eval.Services;
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

namespace Application_WPF_Av_Eval.UserControls
{
    /// <summary>
    /// Logique d'interaction pour ConvertisseurEuro.xaml
    /// </summary>
    public partial class ConvertisseurEuro : UserControl
    {
        private List<Devise> devises;

        public ConvertisseurEuro()
        {
            InitializeComponent();
            devises = Service.ChargerDevises();
            DeviseComboBox.ItemsSource = devises;
            DeviseComboBox.DisplayMemberPath = "NomDevise";
        }

        private void Convertir_Click(object sender, RoutedEventArgs e)
        {
            if (DeviseComboBox.SelectedItem is Devise selectedDevise && double.TryParse(MontantDeviseTextBox.Text, out double montantDevise))
            {
                double resultat = montantDevise / selectedDevise.Taux;
                ResultatTextBox.Text = resultat.ToString("F2");
            }
            else
            {
                MessageBox.Show("Veuillez entrer un montant valide et sélectionner une devise.");
            }
        }
    }
}
