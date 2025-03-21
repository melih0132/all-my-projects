
DROP VIEW IF EXISTS vComptes;
DROP TABLE IF EXISTS Compte CASCADE;
DROP TABLE IF EXISTS Virement CASCADE;

Create table Compte (
	idCompte integer not null primary key,
	solde numeric(10,2) not null
);

Create table Virement (
	idTransaction serial primary key,
	idCompteDebit integer not null,
	idCompteCredit integer not null,
	dateTransaction date not null default current_date,
	Montant numeric(10,2) not null
);

CREATE VIEW vComptes
AS
SELECT idCompte, solde
FROM Compte;

insert into Compte (idCompte, solde) values (1234567, 1000);
insert into Compte (idCompte, solde) values (2345678, 2000);
insert into Compte (idCompte, solde) values (3456789, 0);
