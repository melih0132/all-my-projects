using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataLayer
{
    public interface IDataAccess
    {
        public DataTable? GetData(string getQuery);
        public int SetData(string setQuery);
        public void VirementBancaire(int idCompteDebit, int idCompteCredit, double montant);
    }
}
