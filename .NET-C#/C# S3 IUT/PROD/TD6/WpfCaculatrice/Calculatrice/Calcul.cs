using System;
using System.CodeDom;

namespace Calculatrice
{
    public class Calcul:ICalcul
    {
        //Singleton
        private static Calcul? instance;
        static readonly object instanceLock = new object();

        private Calcul() { }

        public static Calcul? Instance
        {
            get
            {
                if (instance == null) //Les locks prennent du temps, il est préférable de v�rifier d'abord la nullité de l'instance.
                {
                    lock (instanceLock)
                    {
                        if (instance == null) //on vérifie encore, au cas où l'instance aurait été créée entre temps.
                            instance = new Calcul();
                    }
                }
                return instance;
            }
        }

        public Double Addition(Double a, Double b)
        {
            return a + b;
        }

        public Double Soustraction(Double a, Double b)
        {
            return a - b;
        }

        public Double Multiplication(Double a, Double b)
        {
            return a * b;
        }

        public Double Division(Double a, Double b)
        {
            if (b == 0)
                throw new DivideByZeroException("Erreur de division par zéro.");
            else
                return a / b;
        }

        public Double Factorielle(double number)
        {
            int nb=(int)number;
            if (number!=nb)
                throw new ArgumentException("Le nombre doit être un entier.");

            int factorielle=1;

            for (int counter = 1; counter <= nb; counter++)
            {
                factorielle *= counter;
            }
            return factorielle;
        }
    }
}
