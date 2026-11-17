// Services/WSService.cs
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using ClientConvertisseurV2.Models;

namespace ClientConvertisseurV2.Services
{
    public class WSService : IService
    {
        private readonly HttpClient httpClient;

        public WSService(string baseUri)
        {
            httpClient = new HttpClient { BaseAddress = new Uri(baseUri) };
        }

        public async Task<List<Devise>> GetDevisesAsync(string nomControleur)
        {
            try
            {
                return await httpClient.GetFromJsonAsync<List<Devise>>(nomControleur);
            }
            catch (Exception)
            {
                return null;
            }
        }
    }
}
