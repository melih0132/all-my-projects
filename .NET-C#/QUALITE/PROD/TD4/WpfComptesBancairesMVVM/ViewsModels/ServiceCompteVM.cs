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

namespace WpfComptesBancairesMVVM.ViewsModels
{
    public class ServiceCompteVM: ObservableObject, INotifyPropertyChanged
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

        public Compte? Compte
        {
            get { return compte; }

            set
            {
                compte = value;
                OnPropertyChanged("Compte");

            }
        }

        public string? Operation
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

        public IRelayCommand BtnValider { get; }
        public IRelayCommand BtnAnnuler { get; }


        public ServiceCompteVM()
        {
            Operations.Add("Retrait");
            Operations.Add("Dépôt");
            List<Compte> listeComptes = ObjServiceCompte.GetAllComptes();
            Comptes = new ObservableCollection<Compte>(listeComptes);
            BtnValider = new RelayCommand(ActionValider);
            BtnAnnuler = new RelayCommand(ActionAnnuler);

        }

        protected void OnPropertyChanged(string name)
        {
            PropertyChangedEventHandler? handler = PropertyChanged;
            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(name));
            }
        }
        public void ActionValider()
        {
            if (Operation == null || Compte == null)
            {
                MessageBox.Show($"Vous devez selectionner le type d'operation et/ou le compte bancaire", "Erreur", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            ObjServiceCompte.SetDebitCredit(Compte, Resultat);
            MessageBox.Show($"{(Operation == "Dépôt" ? "Dépôt" : "Retrait")} effectué", "Compte Bancaire", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        public void ActionAnnuler()
        {
            Resultat = 0;
            Compte = null;
            Operation = null;

        }
    }
}
