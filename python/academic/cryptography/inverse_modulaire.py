class CalculatriceCryptage:
    
    def inverse_modulaire(self, a, n):
        """Calcule l'inverse modulaire de a mod n, si possible"""
        t, new_t = 0, 1
        r, new_r = n, a
        
        print(f"Initialisation : r = {r}, new_r = {new_r}, t = {t}, new_t = {new_t}")

        while new_r != 0:
            quotient = r // new_r
            print(f"Calcul du quotient : quotient = {quotient}")

            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r
            
            print(f"Étapes intermédiaires : r = {r}, new_r = {new_r}, t = {t}, new_t = {new_t}")

        if r > 1:
            print(f"{a} n'a pas d'inverse modulaire mod {n}")
            return None  # a n'a pas d'inverse modulaire
        if t < 0:
            t = t + n
        
        print(f"Inverse modulaire trouvé : {t}")
        return t

# Exemple d'utilisation
if __name__ == "__main__":
    calc_crypto = CalculatriceCryptage()
    
    # Saisie utilisateur
    try:
        a = int(input("Entrez la valeur de a : "))
        n = int(input("Entrez la valeur de n : "))
        
        inverse = calc_crypto.inverse_modulaire(a, n)
        if inverse is not None:
            print(f"L'inverse modulaire de {a} mod {n} est : {inverse}")
    except ValueError:
        print("Veuillez entrer des valeurs entières valides.")