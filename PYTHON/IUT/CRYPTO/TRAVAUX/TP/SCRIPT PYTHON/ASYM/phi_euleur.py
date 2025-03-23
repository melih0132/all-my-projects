class CalculatriceCryptage:
    
    def phi_euler(self, nombre, debug=False):
        """Calcule la fonction phi d'Euler de nombre"""
        result = nombre
        facteur_premier = 2
        
        if debug:
            print(f"Calcul de phi d'Euler pour {nombre}")
        
        while facteur_premier * facteur_premier <= nombre:
            if debug:
                print(f"Vérification du facteur premier : {facteur_premier}")
                
            if nombre % facteur_premier == 0:
                if debug:
                    print(f"{nombre} est divisible par {facteur_premier}")
                    
                while nombre % facteur_premier == 0:
                    nombre //= facteur_premier
                
                result -= result // facteur_premier
                
                if debug:
                    print(f"Mise à jour du résultat : {result} après avoir soustrait {result // facteur_premier}")
                    
            facteur_premier += 1
        
        if nombre > 1:
            result -= result // nombre
            
            if debug:
                print(f"{nombre} est un facteur premier, mise à jour du résultat : {result} après avoir soustrait {result // nombre}")
        
        if debug:
            print(f"Résultat final de phi d'Euler : {result}")
        
        return result

# Exemple d'utilisation
if __name__ == "__main__":
    calc_crypto = CalculatriceCryptage()
    
    # Saisie utilisateur
    try:
        n = int(input("Entrez la valeur de n : "))
        phi_result = calc_crypto.phi_euler(n, debug=True)
        print(f"Phi d'Euler de {n} : {phi_result}")
    except ValueError:
        print("Veuillez entrer une valeur entière valide.")