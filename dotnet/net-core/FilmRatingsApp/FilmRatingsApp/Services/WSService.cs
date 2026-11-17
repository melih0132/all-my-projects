using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using FilmRatingsApp.Models;
using Windows.ApplicationModel.Resources;

namespace FilmRatingsApp.Services;
public class WSService : IService
{
    private HttpClient client;
    private string baseUri;

    public WSService()
    {
        client = new HttpClient();
        var loader = new ResourceLoader();
        baseUri = loader.GetString("https://localhost:7131/api/Utilisateurs");
    }

    // Méthodes pour Utilisateur
    public async Task<Utilisateur> GetUtilisateurByEmailAsync(string email)
    {
        try
        {
            string requestUri = string.Concat($"{baseUri}/GetByEmail/{Uri.EscapeDataString(email)}");
            HttpResponseMessage response = await client.GetAsync(requestUri);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<Utilisateur>();
            }
            return null;
        }
        catch (Exception)
        {
            return null;
        }
    }

    public async Task<List<Utilisateur>> GetUtilisateursAsync()
    {
        try
        {
            string requestUri = string.Concat(baseUri);
            HttpResponseMessage response = await client.GetAsync(requestUri);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<List<Utilisateur>>();
            }
            return new List<Utilisateur>();
        }
        catch (Exception)
        {
            return new List<Utilisateur>();
        }
    }

    public async Task<bool> AddUtilisateurAsync(Utilisateur utilisateur)
    {
        try
        {
            string requestUri = string.Concat(baseUri, utilisateur);
            var content = new StringContent(
                JsonSerializer.Serialize(utilisateur),
                Encoding.UTF8,
                "application/json");

            HttpResponseMessage response = await client.PostAsync(requestUri, content);
            return response.IsSuccessStatusCode;
        }
        catch (Exception)
        {
            return false;
        }
    }

    public async Task<bool> UpdateUtilisateurAsync(Utilisateur utilisateur)
    {
        try
        {
            string requestUri = string.Concat($"{baseUri}/{utilisateur.Id}");
            var content = new StringContent(
                JsonSerializer.Serialize(utilisateur),
                Encoding.UTF8,
                "application/json");

            HttpResponseMessage response = await client.PutAsync(requestUri, content);
            return response.IsSuccessStatusCode;
        }
        catch (Exception)
        {
            return false;
        }
    }

    public async Task<bool> DeleteUtilisateurAsync(int id)
    {
        try
        {
            string requestUri = string.Concat($"{baseUri}/{id}");
            HttpResponseMessage response = await client.DeleteAsync(requestUri);
            return response.IsSuccessStatusCode;
        }
        catch (Exception)
        {
            return false;
        }
    }

    // Méthodes pour Film (à développer dans la suite du TP)
    public async Task<List<Film>> GetFilmsAsync()
    {
        try
        {
            string requestUri = string.Concat(baseUri, "/films");
            HttpResponseMessage response = await client.GetAsync(requestUri);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<List<Film>>();
            }
            return new List<Film>();
        }
        catch (Exception)
        {
            return new List<Film>();
        }
    }

    public async Task<Film> GetFilmByIdAsync(int id)
    {
        try
        {
            string requestUri = string.Concat(baseUri, "/films/", id);
            HttpResponseMessage response = await client.GetAsync(requestUri);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<Film>();
            }
            return null;
        }
        catch (Exception)
        {
            return null;
        }
    }

    // Méthodes pour Notation (à développer dans la suite du TP)
    public async Task<List<Notation>> GetNotationsByUtilisateurAsync(int utilisateurId)
    {
        try
        {
            string requestUri = string.Concat(baseUri, "/notations/utilisateur/", utilisateurId);
            HttpResponseMessage response = await client.GetAsync(requestUri);

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<List<Notation>>();
            }
            return new List<Notation>();
        }
        catch (Exception)
        {
            return new List<Notation>();
        }
    }
}
