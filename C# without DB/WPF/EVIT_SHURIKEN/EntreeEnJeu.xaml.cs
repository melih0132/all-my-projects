using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;

namespace NinjaJeu
{
    public partial class EntreeEnJeu : Window
    {
        public EntreeEnJeu()
        {
            InitializeComponent();
        }

        private void BoutonJouer_Click(object sender, RoutedEventArgs e)
        {
            this.DialogResult = true;
        }

        private void BoutonQuitter_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();

            this.DialogResult = false;
        }

        private void Notice_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("But du Jeu:\n\nÉviter les shurikens et les kunaïs", "But du Jeu", MessageBoxButton.OK, MessageBoxImage.Information);

            MessageBox.Show("Commandes pour jouer :\n\nUtilisez les touches fléchées pour vous déplacer.\nAppuyez sur la touche '+' pour activer, '-' pour désactiver le mode triche.\nLa touche P pour mettre sur pause.", "Commandes pour Jouer", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Escape || e.Key == Key.Q)
                Application.Current.Shutdown();
        }

        private void BoutonSon_Click(object sender, RoutedEventArgs e)
        {
            MainWindow.GererMusqiueDeFond();

            string imageUri = MainWindow.RenvoieTrueSiMusqiueDeFondDesactive() ? "mute.png" : "demute.png";
            BoutonSon.Background = new ImageBrush(new BitmapImage(new Uri($"pack://application:,,,/NinjaJeu;component/{imageUri}", UriKind.Absolute)));
        }
    }
}