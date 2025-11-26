using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Globalization;
using ClientConvertisseurV1.Models;
using ClientConvertisseurV1.Services;
using System.Collections.ObjectModel;

namespace ClientConvertisseurV1.Views
{
    public sealed partial class ConvertisseurEuroPage : Page
    {
        private readonly WSService wsService;
        private List<Devise> result;
        private ObservableCollection<Devise> devises;

        public ConvertisseurEuroPage()
        {
            this.InitializeComponent();
            this.DataContext = this;

            wsService = new WSService("https://localhost:7078/api/");

            LoadDevisesAsync();
        }

        private async void LoadDevisesAsync()
        {
            try
            {
                result = await wsService.GetDevisesAsync("devises");

                if (result != null && result.Count > 0)
                {
                    devises = new ObservableCollection<Devise>(result);
                    cbDevises.ItemsSource = devises;
                }
                else
                {
                    await ShowErrorDialog("Aucune devise disponible.");
                }
            }
            catch (Exception ex)
            {
                await ShowErrorDialog($"Erreur de connexion : {ex.Message}");
            }
        }

        private async void Convertir_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(txtMontantEuro.Text))
            {
                await ShowErrorDialog("Veuillez saisir un montant en Euro.");
                return;
            }
            if (cbDevises.SelectedItem == null)
            {
                await ShowErrorDialog("Veuillez sélectionner une devise.");
                return;
            }

            if (double.TryParse(txtMontantEuro.Text, NumberStyles.Any, CultureInfo.InvariantCulture, out double montantEuro))
            {
                Devise selectedDevise = (Devise)cbDevises.SelectedItem;
                double montantConverti = montantEuro * selectedDevise.Taux;
                txtMontantDevise.Text = montantConverti.ToString("F2", CultureInfo.InvariantCulture);
            }
            else
            {
                await ShowErrorDialog("Montant invalide.");
            }
        }

        private async Task ShowErrorDialog(string message)
        {
            ContentDialog dialog = new ContentDialog()
            {
                Title = "Erreur",
                Content = message,
                CloseButtonText = "OK"
            };

            if (this.Content != null)
            {
                dialog.XamlRoot = this.Content.XamlRoot;
                await dialog.ShowAsync();
            }
        }
    }
}
