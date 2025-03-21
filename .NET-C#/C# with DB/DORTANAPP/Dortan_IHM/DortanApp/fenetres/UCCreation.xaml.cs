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

namespace DortanApp
{
    /// <summary>
    /// Logique d'interaction pour UCCreation.xaml
    /// </summary>
    public partial class UCCreation : UserControl
    {
        public UCCreation()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string nomActivite = txtNomActivite.Text;

            if (nomActivite.Length >= 10)
            {
                if (nomActivite.Length > 100)
                    MessageBox.Show("Réduissez la taille du nom de l'activité");
                else
                {
                    MainWindow mainWindow = (MainWindow)Application.Current.MainWindow;
                    mainWindow.CreationActivite(nomActivite);

                    txtNomActivite.Text = "";
                }
            }
            else if (nomActivite.Length < 10)
                MessageBox.Show("Ajoutez plus de détails");
        }
    }
}
