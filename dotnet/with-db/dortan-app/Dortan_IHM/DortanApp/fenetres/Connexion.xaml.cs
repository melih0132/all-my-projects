using DortanApp.config;
using System.Windows;

namespace Dortan
{
    /// <summary>
    /// Logique d'interaction pour Connexion.xaml
    /// </summary>
    public partial class Connexion : Window
    {

        public Connexion()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string identifiant = txtIdentifiant.Text;
            string mdp = txtMotDePasse.Password.ToString();

            DataAccess dataAccess = DataAccess.Instance;

            dataAccess.ConnexionBD(identifiant, mdp);

            if (dataAccess.Connexion?.State == System.Data.ConnectionState.Open)
            {
                DialogResult = true;
            }
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (DialogResult != true)
            {
                Application.Current.Shutdown();
            }
        }
    }
}