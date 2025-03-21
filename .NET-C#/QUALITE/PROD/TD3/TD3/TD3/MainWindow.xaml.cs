using System.Windows;
using TD3.UserControls;

namespace TD3
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void ConvertCurrencyToEuro_Click(object sender, RoutedEventArgs e)
        {
            MainContentControl.Content = new ConvertisseurEuro();
        }

        private void ConvertEuroToCurrency_Click(object sender, RoutedEventArgs e)
        {
            MainContentControl.Content = new ConvertisseurDevise();
        }

        private void ManageCurrencies_Click(object sender, RoutedEventArgs e)
        {
            MainContentControl.Content = new GestionDevises();
        }
    }
}
