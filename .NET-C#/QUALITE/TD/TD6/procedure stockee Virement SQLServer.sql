-- DROP PROCEDURE SPVirement_Append
-- GO
CREATE PROCEDURE SPVirement_Append(
	@IDCOMPTEDEBIT        	int,
	@IDCOMPTECREDIT       	int,
	@MONTANT				float,
	@RETOUR					int OUTPUT
	)
AS
BEGIN
	BEGIN TRANSACTION;
	DECLARE @nblignes INT=0;
	
	UPDATE compte SET solde = solde-@MONTANT WHERE idcompte=@IDCOMPTEDEBIT; 
	SET @nblignes=@nblignes+@@ROWCOUNT;
	
	UPDATE compte SET solde = solde+@MONTANT WHERE idcompte=@IDCOMPTECREDIT; 
	SET @nblignes=@nblignes+@@ROWCOUNT;
	
	if @nblignes=2
	BEGIN
		INSERT INTO virement(idcomptedebit, idcomptecredit, datetransaction, montant)
		VALUES (@IDCOMPTEDEBIT, @IDCOMPTECREDIT, getdate(), @MONTANT);
		SET @nblignes=@nblignes+@@ROWCOUNT;
	END
	
	if @nblignes=3 -- 2 UPDATE + 1 INSERT
		COMMIT
	ELSE
		ROLLBACK
		
	SET @RETOUR=@nblignes
END


/*TEST DE LA PROCEDURE EN T-SQL*/

/*
DECLARE @RET int
EXEC SPVirement_Append 
	1234567, 
	2345678, 
	500,
	@RET OUTPUT
SELECT @RET
*/