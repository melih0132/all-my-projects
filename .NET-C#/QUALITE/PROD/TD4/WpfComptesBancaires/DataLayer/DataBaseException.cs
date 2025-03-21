using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataLayer // A MODIFIER SI VOTRE PROJET A UN AUTRE NOM
{
    public class DataBaseException : Exception
    {
        public DataBaseException() { }

        public DataBaseException(string message)
        : base(message) { }

        public DataBaseException(string message, Exception inner)
        : base(message, inner) { }
    }
}
