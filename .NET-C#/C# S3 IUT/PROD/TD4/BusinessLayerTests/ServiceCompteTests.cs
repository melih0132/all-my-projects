using Microsoft.VisualStudio.TestTools.UnitTesting;
using BusinessLayer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DataLayer;
using System.Data;
using System.Numerics;

namespace BusinessLayer.Tests
{
    [TestClass()]
    public class ServiceCompteTests
    {
        public IDataAccess ObjDataAcces
        {
            get { return DataAccess.Instance; }
        }
        public IServiceCompte ObjServiceCompte
        {
            get { return ServiceCompte.Instance; }
        }
        /// <summary>
        /// Cette méthode appelle la méthode SetData sur un objet de type DataAccess pour supprimer les données de la table Compte
        /// et insérer 2 comptes bancaires : 1234567 / 1000 et 2345678 / 2000.
        /// </summary>
        [TestInitialize()]
        public void InitialisationDesTests()
        {
            ObjDataAcces.SetData($"DELETE  FROM vComptes");
            ObjDataAcces.SetData($"insert into vComptes (idCompte, solde) values (1234567, 1000);");
            ObjDataAcces.SetData($"insert into vComptes (idCompte, solde) values (2345678, 2000);");
        }
        [TestMethod()]
        public void GetAllComptesTest_Compte1()
        {
            //Arrange
            Compte compte = new Compte();

            //Act
            compte = ObjServiceCompte.GetCompte(1234567);

            //Assert
            Assert.AreEqual(new Compte(1234567, 1000), compte, "Test non ok Compte1");
        }

        [TestMethod()]
        public void GetAllComptesTest_Compte2()
        {
            //Arrange
            Compte compte = new Compte();

            //Act
            compte = ObjServiceCompte.GetCompte(2345678);

            //Assert
            Assert.AreEqual(new Compte(2345678, 2000), compte, "Test non ok Compte1");
        }

        [TestMethod()]
        public void SetDebitCreditTest_DebitOK()
        {
            //Arrange
            Compte compte = new Compte();


            //Act
            compte = ObjServiceCompte.GetCompte(2345678);
            ObjServiceCompte.SetDebitCredit(compte, -1000);

            // Assert
            Assert.AreEqual(new Compte(2345678, 1000), compte, "Test non ok  Test_Debit");

        }
        [TestMethod()]
        public void SetDebitCreditTest_CreditOK()
        {
            //Arrange
            Compte compte = new Compte();
            Compte compte2 = new Compte();

            //Act
            compte = ObjServiceCompte.GetCompte(2345678);
            ObjServiceCompte.SetDebitCredit(compte, 1000);
            compte2 = ObjServiceCompte.GetCompte(2345678);
            // Assert
            Assert.AreEqual(new Compte(2345678, 3000), compte, "Test non ok  Test_Debit");
            Assert.AreEqual(compte, compte2);

        }

        [TestMethod()]
        [ExpectedException(typeof(DataBaseException))]
        public void SetDebitCreditTest_CompteInconnuNonOK()
        {
            //Arrange
            Compte compte = new Compte();


            //Act
            compte = ObjServiceCompte.GetCompte(234578);
            ObjServiceCompte.SetDebitCredit(compte, 1000);

        }
        [TestCleanup()]
        public void NettoyageDesTests()
        {
            ObjDataAcces.SetData($"DELETE  FROM vComptes");
            ObjDataAcces.SetData($"insert into vComptes (idCompte, solde) values (1234567, 1000);");
            ObjDataAcces.SetData($"insert into vComptes (idCompte, solde) values (2345678, 2000);");
            ObjDataAcces.SetData($"insert into Compte (idCompte, solde)   values (3456789, 0)");
        }





    }
}