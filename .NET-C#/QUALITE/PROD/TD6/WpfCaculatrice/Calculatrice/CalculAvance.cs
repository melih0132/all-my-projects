using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Calculatrice
{
    public class CalculAvance:ICalculAvance
    {
        //Singleton
        private static CalculAvance? instance;
        static readonly object instanceLock = new object();

        private CalculAvance() { }

        public static CalculAvance? Instance
        {
            get
            {
                if (instance == null) //Les locks prennent du temps, il est préférable de v�rifier d'abord la nullité de l'instance.
                {
                    lock (instanceLock)
                    {
                        if (instance == null) //on vérifie encore, au cas où l'instance aurait été créée entre temps.
                            instance = new CalculAvance();
                    }
                }
                return instance;
            }
        }

        public double Moyenne(ICalcul calcul, double nb1, double nb2)
        {
            return calcul.Division(calcul.Addition(nb1, nb2), 2);
        }
    }
}
