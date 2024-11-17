using System;

namespace DortanApp
{
    public class Caracteristique
    {
        private int id;
        private string nom;

        public Caracteristique(string nom)
        {
            this.Nom = nom;
        }

        public Caracteristique(int id, string nom) : this(nom)
        {
            this.Id = id;
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
                return this.nom;
            }

            set
            {
                this.nom = value;
            }
        }
    }
}