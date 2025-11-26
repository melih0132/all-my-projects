using ClientConvertisseurV2.Models;
using ClientConvertisseurV2.Services;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Microsoft.UI.Xaml.Controls;
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace ClientConvertisseurV2.ViewModels
{
    public class ConvertisseurEuroViewModel : ObservableObject
    {
        private readonly IService wsService;

        private ObservableCollection<Devise> devises;
        public ObservableCollection<Devise> Devises
        {
            get => devises;
            set => SetProperty(ref devises, value);
        }

        private string montantEuro;
        public string MontantEuro
        {
            get => montantEuro;
            set => SetProperty(ref montantEuro, value);
        }

        private string montantDevise;
        public string MontantDevise
        {
            get => montantDevise;
            set => SetProperty(ref montantDevise, value);
        }

        private Devise deviseselectionnee;
        public Devise DeviseSelectionnee
        {
            get => deviseselectionnee;
            set => SetProperty(ref deviseselectionnee, value);
        }

        public IRelayCommand BtnSetConversion { get; }

        public ConvertisseurEuroViewModel(IService service)
        {
            wsService = service;
            BtnSetConversion = new RelayCommand(ActionSetConversion);
            GetDataOnLoadAsync();
        }

        public async void GetDataOnLoadAsync()
        {
            try
            {
                var result = await wsService.GetDevisesAsync("Devises");
                if (result == null || result.Count == 0)
                {
                    MontantDevise = "Aucune devise disponible.";
                    return;
                }
                Devises = new ObservableCollection<Devise>(result);
            }
            catch (Exception ex)
            {
                MontantDevise = "Erreur lors du chargement des devises.";
                await AfficherErreur("Erreur lors du chargement des devises.");
            }
        }

        private async Task AfficherErreur(string message)
        {
            var dialog = new ContentDialog
            {
                Title = "Erreur",
                Content = message,
                CloseButtonText = "OK",
                XamlRoot = App.MainRoot.XamlRoot
            };
            await dialog.ShowAsync();
        }

        public async void ActionSetConversion()
        {
            if (string.IsNullOrWhiteSpace(MontantEuro))
            {
                await AfficherErreur("Veuillez saisir un montant.");
                return;
            }

            if (!double.TryParse(MontantEuro, out double montant) || montant < 0)
            {
                await AfficherErreur("Montant invalide.");
                return;
            }

            if (DeviseSelectionnee == null)
            {
                await AfficherErreur("Veuillez sélectionner une devise.");
                return;
            }

            double result = montant * DeviseSelectionnee.Taux;
            MontantDevise = result.ToString("F2");
        }
    }
}