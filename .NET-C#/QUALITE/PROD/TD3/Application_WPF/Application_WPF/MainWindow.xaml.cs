using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Application_WPF
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void ConvertisseurDevise_Button_Click(object sender, RoutedEventArgs e)
        {
            ConvertisseurDevise convertisseurDevise = new ConvertisseurDevise();
            this.MyContentControl.Content = convertisseurDevise;
        }

        private void ConvertisseurEuro_Click(object sender, RoutedEventArgs e)
        {
            ConvertisseurEuro convertisseurEuro = new ConvertisseurEuro();
            this.MyContentControl.Content = convertisseurEuro;
        }


        private void GEstionDevises_Click(object sender, RoutedEventArgs e)
        {
            GEstionDevises devise = new GEstionDevises();
            this.MyContentControl.Content = devise;
        }
    }
}