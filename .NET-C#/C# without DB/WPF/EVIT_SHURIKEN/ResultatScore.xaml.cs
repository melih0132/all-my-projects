using System;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace NinjaJeu
{
    public partial class ResultatScore : Window
    {
        public ResultatScore()
        {
            InitializeComponent();
            KeyDown += Window_KeyDown;
        }

        public void AfficherScoreFinal(int score, int highscore)
        {
            Score.Text = $"Score: {score}";
            HighScore.Text = $"Meilleur Score: {highscore}";

            if (score > highscore)
            {
                TextBlock nouveauRecordBlock = new TextBlock
                {
                    Text = "NOUVEAU RECORD!",
                    FontSize = 28,
                    FontWeight = FontWeights.Bold,
                    Foreground = Brushes.Gold,
                    HorizontalAlignment = HorizontalAlignment.Center,
                    VerticalAlignment = VerticalAlignment.Center,
                    Margin = new Thickness(0, 170, 0, 0)
                };

                Grid grid = Content as Grid;
                grid?.Children.Add(nouveauRecordBlock);
            }
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
            else if (e.Key == Key.R || e.Key == Key.Enter)
            {
                MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
                mainWindow?.Rejouer();
                this.Close();
            }
        }
    }
}