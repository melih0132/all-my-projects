using BusinessLayer;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Numerics;
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
    /// Logique d'interaction pour RechercheVirement.xaml
    /// </summary>
    public partial class RechercheVirement : Window, INotifyPropertyChanged
    {
        public ObservableCollection<Compte> Comptes { get => comptes; set => comptes = value; }
        private ObservableCollection<Compte> comptes = new ObservableCollection<Compte>();
        private Compte compte;
        private DateTime selectedDate;
        private double montant;
        private ObservableCollection<Virement> virements = new ObservableCollection<Virement>();

        public event PropertyChangedEventHandler? PropertyChanged;

        public Compte Compte
        {
            get { return compte; }

            set
            {
                compte = value;
                OnPropertyChanged("Compte");

            }
        }

        public DateTime SelectedDate
        {
            get { return selectedDate; }

            set
            {
                selectedDate = value;
                OnPropertyChanged("selectedDate");

            }
        }

        public Double Montant
        { //Property Resultat
            get { return montant; }
            set
            {
                montant = value;
                OnPropertyChanged("Montant");
            }
        }
        public IServiceCompte ObjServiceCompte
        {
            get { return ServiceCompte.Instance; }
        }

        public ObservableCollection<Virement> Virements { get => virements; set => virements = value; }

        public RechercheVirement()
        {
           InitializeComponent();
            this.DataContext = this;
            List<Compte> listeComptes = ObjServiceCompte.GetAllComptes();
            List<Virement> listVirement = ObjServiceCompte.GetAllVirement();
            Comptes = new ObservableCollection<Compte>(listeComptes);
            Virements= new ObservableCollection<Virement>(listVirement);
        }
        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler? handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }

        private void BtRechercher_Click(object sender, RoutedEventArgs e)
        {
            List<Virement> listVirement =  ObjServiceCompte.GetVirements(Compte.IdCompte, SelectedDate);
            Virements = new ObservableCollection<Virement>(listVirement);
        }
    }
}
