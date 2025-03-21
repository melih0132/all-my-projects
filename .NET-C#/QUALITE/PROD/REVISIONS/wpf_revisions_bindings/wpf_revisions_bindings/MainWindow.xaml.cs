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

namespace wpf_revisions_bindings
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public ViewModel ViewModel { get; set; }

        public MainWindow()
        {
            InitializeComponent();

            ViewModel = new ViewModel();
            DataContext = ViewModel;
        }

        private void LoadUsers_Click(object sender, RoutedEventArgs e)
        {
            ViewModel.LoadUsers();
        }

        private void SaveUser_Click(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(ViewModel.UserName))
            {
                ViewModel.SaveUser();
                MessageBox.Show("Utilisateur enregistré !");
            }
            else
            {
                MessageBox.Show("Veuillez entrer un nom.");
            }
        }
    }
}