class CalculatriceCryptage:

    def exponentiation_modulaire(self, base, exp, mod):
        """Calcule (base^exp) % mod avec débogage"""
        result = 1
        base = base % mod
        print(f"Base initiale = {base}, Exposant = {exp}, Modulo = {mod}")
        
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
                print(f"Exposant impair, nouveau résultat = {result}")
            exp = exp // 2
            base = (base * base) % mod
            print(f"Base mise à jour = {base}, Exposant divisé par 2 = {exp}")
        
        print(f"Résultat final = {result}")
        return result

# Exemple d'utilisation
if __name__ == "__main__":
    calc_crypto = CalculatriceCryptage()
    
    # Saisie utilisateur
    try:
        base = int(input("Entrez la valeur de la base : "))
        exp = int(input("Entrez la valeur de l'exposant : "))
        mod = int(input("Entrez la valeur du modulo : "))
        
        calc_crypto.exponentiation_modulaire(base, exp, mod)
    except ValueError:
        print("Veuillez entrer des valeurs entières valides.")