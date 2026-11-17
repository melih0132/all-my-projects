using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using FilmRatingsApp.Models;
using FilmRatingsApp.Services;
using Microsoft.UI.Xaml.Controls;
using System.Threading.Tasks;
using System.Windows.Input;

namespace FilmRatingsApp.ViewModels;

public partial class UtilisateurViewModel : ObservableRecipient
{
    private readonly WSService _service;
    private string _searchMail;
    private Utilisateur _utilisateurSearch;

    [ObservableProperty]
    private string searchMail;

    [ObservableProperty]
    private Utilisateur utilisateurSearch;

    public ICommand BtnSearchUtilisateurCommand
    {
        get;
    }
    public ICommand BtnModifyUtilisateurCommand
    {
        get;
    }
    public ICommand BtnClearUtilisateurCommand
    {
        get;
    }
    public ICommand BtnAddUtilisateurCommand
    {
        get;
    }

    public UtilisateurViewModel(WSService service) // Injection du service concret
    {
        _service = service;
        InitializeUtilisateur();

        // Utilisation de AsyncRelayCommand pour les méthodes asynchrones
        BtnSearchUtilisateurCommand = new AsyncRelayCommand(ExecuteSearchUtilisateurAsync);
        BtnModifyUtilisateurCommand = new AsyncRelayCommand(ExecuteModifyUtilisateurAsync);
        BtnClearUtilisateurCommand = new RelayCommand(ExecuteClearUtilisateur);
        BtnAddUtilisateurCommand = new AsyncRelayCommand(ExecuteAddUtilisateurAsync);
    }

    private void InitializeUtilisateur()
    {
        UtilisateurSearch = new Utilisateur
        {
            // Initialisation des propriétés requises
            Mail = string.Empty,
            Pwd = string.Empty,
            Nom = string.Empty,
            Prenom = string.Empty
        };
    }

    private async Task ExecuteSearchUtilisateurAsync()
    {
        if (string.IsNullOrWhiteSpace(SearchMail))
        {
            await ShowDialogAsync("Erreur", "Veuillez saisir une adresse email valide.");
            return;
        }

        var utilisateur = await _service.GetUtilisateurByEmailAsync(SearchMail.Trim());

        if (utilisateur != null)
        {
            UtilisateurSearch = utilisateur;
        }
        else
        {
            await ShowDialogAsync("Information", "Aucun utilisateur trouvé.");
            InitializeUtilisateur();
        }
    }

    private async Task ExecuteModifyUtilisateurAsync()
    {
        if (UtilisateurSearch?.Id == 0) // Utilisation de UtilisateurId au lieu de Id
        {
            await ShowDialogAsync("Erreur", "Veuillez d'abord rechercher un utilisateur.");
            return;
        }

        if (await ValidateUtilisateurAsync())
        {
            var success = await _service.UpdateUtilisateurAsync(UtilisateurSearch);
            await ShowDialogAsync(success ? "Succès" : "Erreur",
                success ? "Modification réussie" : "Échec de la modification");
        }
    }

    private void ExecuteClearUtilisateur()
    {
        SearchMail = string.Empty;
        InitializeUtilisateur();
    }

    private async Task ExecuteAddUtilisateurAsync()
    {
        if (await ValidateUtilisateurAsync())
        {
            var success = await _service.AddUtilisateurAsync(UtilisateurSearch);
            if (success) InitializeUtilisateur();
            await ShowDialogAsync(success ? "Succès" : "Erreur",
                success ? "Ajout réussi" : "Échec de l'ajout");
        }
    }

    private async Task<bool> ValidateUtilisateurAsync()
    {
        if (UtilisateurSearch == null)
        {
            await ShowDialogAsync("Erreur", "Utilisateur invalide");
            return false;
        }

        var missingFields = new List<string>();
        if (string.IsNullOrWhiteSpace(UtilisateurSearch.Nom)) missingFields.Add("Nom");
        if (string.IsNullOrWhiteSpace(UtilisateurSearch.Prenom)) missingFields.Add("Prénom");
        if (string.IsNullOrWhiteSpace(UtilisateurSearch.Mail)) missingFields.Add("Email");
        if (string.IsNullOrWhiteSpace(UtilisateurSearch.Pwd)) missingFields.Add("Mot de passe");

        if (missingFields.Count > 0)
        {
            await ShowDialogAsync("Erreur", $"Champs obligatoires manquants :\n{string.Join("\n", missingFields)}");
            return false;
        }

        return true;
    }

    private static async Task ShowDialogAsync(string title, string content)
    {
        var dialog = new ContentDialog
        {
            Title = title,
            Content = content,
            CloseButtonText = "OK",
            XamlRoot = App.MainRoot?.XamlRoot // Gestion null-safe
        };

        await dialog.ShowAsync();
    }
}