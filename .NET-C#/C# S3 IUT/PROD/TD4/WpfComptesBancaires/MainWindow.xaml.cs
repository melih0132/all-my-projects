using BusinessLayer;
using System.Collections.ObjectModel;
using System.ComponentModel;
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

namespace WpfComptesBancaires
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window, INotifyPropertyChanged
    {
        private ObservableCollection<string>? operations = new ObservableCollection<string>();
        private string operation;
        private ObservableCollection<Compte> comptes = new ObservableCollection<Compte>();
        private Compte compte;

        public IServiceCompte ObjServiceCompte
        {
            get { return ServiceCompte.Instance; }
        }

        public ObservableCollection<string>? Operations
        {
            get
            {
                return this.operations;
            }

            set
            {
                this.operations = value;
            }
        }

        public ObservableCollection<Compte> Comptes { get => comptes; set => comptes = value; }
        public Double Resultat
        { //Property Resultat
            get { return resultat; }
            set
            {
                resultat = value;
                OnPropertyChanged("Resultat");
            }
        }

        public Compte Compte {
            get { return compte; }

            set {
                compte = value;
                 OnPropertyChanged("Compte");

            }
        }

        public string Operation
        {
            get { return operation; }

            set
            {
                operation = value;
                OnPropertyChanged("Operation");
            }
        }


        // OU OnPropertyChanged(nameof(Resultat)); 


        public event PropertyChangedEventHandler? PropertyChanged;
        private Double resultat;



        public MainWindow()
        {
            InitializeComponent();
            this.DataContext = this;
            Operations.Add("Retrait");
            Operations.Add("Dépôt");
            List<Compte> listeComptes = ObjServiceCompte.GetAllComptes();
            Comptes  = new ObservableCollection<Compte>(listeComptes);



        }
        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler? handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }

        private void btValider_Click(object sender, RoutedEventArgs e)
        {
            if(Operation  == null || Compte == null)
            {
                MessageBox.Show($"Vous devez selectionner le type d'operation et/ou le compte bancaire","Erreur",MessageBoxButton.OK,MessageBoxImage.Error);
                return;
            }

            ObjServiceCompte.SetDebitCredit(Compte, Resultat);
            MessageBox.Show($"{(Operation == "Dépôt" ? "Dépôt" : "Retrait")} effectué","Compte Bancaire",MessageBoxButton.OK,MessageBoxImage.Information);


        }

        private void btAnnuler_Click(object sender, RoutedEventArgs e)
        {

            Resultat = 0;
            Compte = null;
            Operation = null;


        }
    }
}