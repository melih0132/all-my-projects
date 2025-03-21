using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BusinessLayer
{
    public class ServiceCompte
    {
        public List<Compte>? GetAllComptes()
        {
            try
            {
                List<Compte> comptes = new List<Compte>();
                DataTable? table = Instance.GetData("select * from vComptes");
                foreach (DataRow res in table.Rows)
                {
                    comptes.Add(new Compte(Convert.ToInt32(res["idCompte"]), Convert.ToDouble(res["solde"])));
                }

                return comptes;
            }
            catch (Exception ex)
            {
                throw ex;

            }
        }
    }
}
