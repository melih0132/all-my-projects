IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Virement]') AND type in (N'U'))
DROP TABLE [dbo].[Virement];
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Compte]') AND type in (N'U'))
DROP TABLE [dbo].[Compte];
IF EXISTS (SELECT * FROM sys.views WHERE object_id = object_id(N'dbo.vComptes'))
DROP VIEW dbo.vComptes;

Create table Compte (
	idCompte int not null primary key,
	solde numeric(10,2) not null
)
go

Create table Virement (
	idTransaction int identity(1,1) primary key,
	idCompteDebit int not null,
	idCompteCredit int not null,
	dateTransaction datetime not null,
	Montant numeric(10,2) not null
)
go

CREATE VIEW vComptes
AS
SELECT idCompte, solde
FROM Compte
go

insert into Compte (idCompte, solde) values (1234567, 1000);
insert into Compte (idCompte, solde) values (2345678, 2000);
insert into Compte (idCompte, solde) values (3456789, 0);
