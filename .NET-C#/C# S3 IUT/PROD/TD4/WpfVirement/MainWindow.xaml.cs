using BusinessLayer;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Numerics;
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

namespace WpfVirement
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window,INotifyPropertyChanged
    {
        private ObservableCollection<Compte> comptes = new ObservableCollection<Compte>();
        private Compte compteDebit;
        private Compte compteCredit;
        private Double resultat;
        public IServiceCompte ObjServiceCompte
        {
            get { return ServiceCompte.Instance; }
        }
        public Double Resultat
        { //Property Resultat
            get { return resultat; }
            set
            {
                resultat = value;
                OnPropertyChanged("Resultat");
            }
        }

        public ObservableCollection<Compte> Comptes { get => comptes; set => comptes = value; }
        public Compte CompteCredit
        {
            get { return compteCredit;  }
            set
            {
                compteCredit = value;
                OnPropertyChanged("CompteCredit");

            }
        }
        public Compte CompteDebit
        { 
            get { return compteDebit; }
            set
            {
                compteDebit = value;
                OnPropertyChanged("compteDebit");

            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        public MainWindow()
        {
            InitializeComponent();
            this.DataContext = this;
            List<Compte> listeComptes = ObjServiceCompte.GetAllComptes();
            Comptes = new ObservableCollection<Compte>(listeComptes);
        }

        private void btValider_Click(object sender, RoutedEventArgs e)
        {
            if (CompteCredit == null || CompteDebit == null)
            {
                MessageBox.Show($"Vous devez selectionner les et/ou le compte bancaire", "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }
            ObjServiceCompte.Virement(CompteDebit,CompteCredit,Resultat);
            MessageBox.Show($"Virement effectué", "Compte Bancaire", MessageBoxButton.OK, MessageBoxImage.Information);

        }

        private void btAnnuler_Click(object sender, RoutedEventArgs e)
        {
            Resultat = 0;
            CompteCredit = null;
            CompteDebit = null;
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