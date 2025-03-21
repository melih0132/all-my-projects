CREATE OR REPLACE PROCEDURE sp_virement_append(pIdCompteDebit integer,
								 pIdCompteCredit integer,
								 pMontant numeric
								 )
AS $$
BEGIN
	UPDATE compte SET solde = solde-pMontant WHERE idcompte=pIdCompteDebit;
	UPDATE compte SET solde = solde+pMontant WHERE idcompte=pIdCompteCredit;
	INSERT INTO virement(idcomptedebit, idcomptecredit, datetransaction, montant)
		VALUES (pIdCompteDebit, pIdCompteCredit, current_date, pMontant);
EXCEPTION
	WHEN others THEN
		RAISE EXCEPTION 'Erreur procédure stockée sp_virement_append';
END;
$$  LANGUAGE plpgsql

-- TEST
-- SELECT * FROM virement;
-- CALL sp_virement_Append(1234567,2345678,100.00);
-- SELECT * FROM virement;