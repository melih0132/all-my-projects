using System.Windows; 
using System.Windows.Input; 

namespace NinjaJeu
{
    public partial class ResultatScore : Window
    {
        public ResultatScore()
        {
            InitializeComponent();
        }

        public void AfficherScoreFinal(int score)
        {
            Score.Text = $"Score: {score}"; 
        }

        private void BoutonRejouer_Click(object sender, RoutedEventArgs e)
        {
            MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
            mainWindow?.Rejouer(); 
            this.Close();
        }

        private void BoutonQuitter_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Escape || e.Key == Key.Q)
                Application.Current.Shutdown(); 
        }
    }
}