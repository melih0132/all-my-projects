using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Calculatrice
{
    public interface ICalcul
    {
        //Singleton
        static Calcul? Instance;
        Double Addition(Double a, Double b);
        Double Soustraction(Double a, Double b);
        Double Multiplication(Double a, Double b);
        Double Division(Double a, Double b);
        Double Factorielle(double number);
    }
}
