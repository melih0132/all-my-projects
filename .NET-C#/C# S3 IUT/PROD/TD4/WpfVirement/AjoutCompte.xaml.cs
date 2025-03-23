using BusinessLayer;
using System;
using System.Collections.Generic;
using System.ComponentModel;
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
using System.Windows.Shapes;

namespace WpfVirement
{
    /// <summary>
    /// Logique d'interaction pour AjoutCompte.xaml
    /// </summary>
    public partial class AjoutCompte : Window, INotifyPropertyChanged
    {
        private int numCompte;
        private Double solde;
        public int NumCompte
        { //Property Resultat
            get { return numCompte; }
            set
            {
                numCompte = value;
                OnPropertyChanged("numCompte");
            }
        }

        public double Solde
        { //Property Resultat
            get { return solde; }
            set
            {
                solde = value;
                OnPropertyChanged("solde");
            }
        }
        public IServiceCompte ObjServiceCompte
        {
            get { return ServiceCompte.Instance; }
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        public AjoutCompte()
        {
            InitializeComponent();
            this.DataContext = this; 
        }

        private void btCréer_Click(object sender, RoutedEventArgs e)
        {
            ObjServiceCompte.CreationCompte(NumCompte,Solde);
            MessageBox.Show($"Compte créer", "Virement", MessageBoxButton.OK, MessageBoxImage.Information);

        }
        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler? handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }
    }
}
