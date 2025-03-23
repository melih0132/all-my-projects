using BusinessLayer;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace WpfVirementMVVM.ViewsModels
{
    public class VirementVM: ObservableObject, INotifyPropertyChanged
    {

        private ObservableCollection<Compte> comptes = new ObservableCollection<Compte>();
        private Compte compteDebit;
        private Compte compteCredit;
        private Double resultat;
        public IRelayCommand BtnValider { get; }
        public IRelayCommand BtnAnnuler { get; }
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
            get { return compteCredit; }
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
        public VirementVM()
        {
            List<Compte> listeComptes = ObjServiceCompte.GetAllComptes();
            Comptes = new ObservableCollection<Compte>(listeComptes);
            BtnValider = new RelayCommand(ActionValider);
            BtnAnnuler = new RelayCommand(ActionAnnuler);
        }

        public void ActionValider()
        {
            if (CompteCredit == null || CompteDebit == null)
            {
                MessageBox.Show($"Vous devez selectionner les et/ou le compte bancaire", "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }
            ObjServiceCompte.Virement(CompteDebit, CompteCredit, Resultat);
            MessageBox.Show($"Virement effectué", "Compte Bancaire", MessageBoxButton.OK, MessageBoxImage.Information);

        }

        public void ActionAnnuler ()
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

