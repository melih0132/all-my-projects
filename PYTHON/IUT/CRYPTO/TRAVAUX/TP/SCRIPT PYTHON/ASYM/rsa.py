import random

class CalculatriceCryptage:

    def pgcd(self, a, b):
        """Calcule le PGCD avec débogage"""
        while b != 0:
            print(f"PGCD de {a} et {b}")
            a, b = b, a % b
        print(f"Résultat final du PGCD : {a}")
        return a

    def inverse_modulaire(self, a, n):
        """Calcule l'inverse modulaire avec débogage"""
        t, new_t = 0, 1
        r, new_r = n, a
        print(f"Début du calcul de l'inverse modulaire de {a} mod {n}")
        
        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r
            print(f"Quotient = {quotient}, t = {t}, r = {r}")
        
        if r > 1:
            print(f"Aucun inverse modulaire trouvé.")
            return None
        if t < 0:
            t = t + n
        
        print(f"Inverse modulaire trouvé : {t}")
        return t

    def generer_cles_rsa(self, p, q):
        """Génère une paire de clés RSA avec débogage"""
        n = p * q
        phi = (p - 1) * (q - 1)
        print(f"Calcul de n = {n} et phi = {phi}")
        
        e = random.randrange(2, phi)
        while self.pgcd(e, phi) != 1:
            e = random.randrange(2, phi)
        print(f"Valeur de e choisie : {e}")
        
        d = self.inverse_modulaire(e, phi)
        print(f"Clé privée d = {d}")
        
        return (e, n), (d, n)

# Exemple d'utilisation
if __name__ == "__main__":
    calc_crypto = CalculatriceCryptage()
    
    # Saisie utilisateur
    try:
        p = int(input("Entrez un nombre premier p : "))
        q = int(input("Entrez un nombre premier q : "))
        
        cle_publique, cle_privee = calc_crypto.generer_cles_rsa(p, q)
        print(f"Clé publique : {cle_publique}")
        print(f"Clé privée : {cle_privee}")
    except ValueError:
        print("Veuillez entrer des valeurs entières valides.")