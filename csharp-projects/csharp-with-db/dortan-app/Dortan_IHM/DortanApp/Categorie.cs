using System;

namespace DortanApp
{
    public class Categorie
    {
        private string nom;

        public Categorie(string nom)
        {
            this.Nom = nom;
        }

        public string Nom
        {
            get
            {
                return this.nom;
            }

            set
            {
                this.nom = value;
            }
        }

        public override string? ToString()
        {
            return Nom;
        }
    }
}