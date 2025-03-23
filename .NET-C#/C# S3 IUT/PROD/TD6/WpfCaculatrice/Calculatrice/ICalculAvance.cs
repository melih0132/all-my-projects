using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Calculatrice
{
    public interface ICalculAvance
    {
        double Moyenne(ICalcul calcul, double nb1, double nb2);
    }
}
