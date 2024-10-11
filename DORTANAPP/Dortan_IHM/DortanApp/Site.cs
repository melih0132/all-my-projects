using System;

namespace DortanApp
{
    public class Site
    {
        private int id;
        private string nom;
        private string adresseRue;
        private string nomResponsable;
        private string horaire;

        public Site(int id)
        {
            this.Id = id;
        }

        public Site(int id, string nom, string adresseRue, string nomResponsable, string horaire) : this (id)
        {
            this.Nom = nom;
            this.AdresseRue = adresseRue;
            this.NomResponsable = nomResponsable;
            this.Horaire = horaire;
        }

        public Site(int id, string nom)
        {
            this.Id = id;
            this.Nom = nom;
        }

        public int Id
        {
            get
            {
                return id;
            }

            set
            {
                id = value;
            }
        }

        public string Nom
        {
            get
            {
                return nom;
            }

            set
            {
                nom = value;
            }
        }

        public string AdresseRue
        {
            get
            {
                return adresseRue;
            }

            set
            {
                adresseRue = value;
            }
        }

        public string NomResponsable
        {
            get
            {
                return nomResponsable;
            }

            set
            {
                nomResponsable = value;
            }
        }

        public string Horaire
        {
            get
            {
                return this.horaire;
            }

            set
            {
                this.horaire = value;
            }
        }
    }
}