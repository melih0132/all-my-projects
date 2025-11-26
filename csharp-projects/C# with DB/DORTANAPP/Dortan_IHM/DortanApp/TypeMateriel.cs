using System;

namespace DortanApp
{
    public class TypeMateriel
    {
        private int id;
        private string nom;

        public TypeMateriel(int id)
        {
            this.Id = id;
        }

        public TypeMateriel(int id, string nom) : this (id)
        {
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
                return this.nom;
            }

            set
            {
                this.nom = value;
            }
        }
    }
}