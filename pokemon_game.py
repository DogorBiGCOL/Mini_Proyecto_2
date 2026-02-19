import csv
import os

class Pokemon:
    def __init__(self, name, type1, type2, hp, attack, defense, speed):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.hp = int(hp)
        self.attack = int(attack)
        self.defense = int(defense)
        self.speed = int(speed)

    def __str__(self):
        type_str = self.type1
        if self.type2:
            type_str += f"/{self.type2}"
        
        card = f"""
        +-----------------------------+
        | {self.name.center(27)} |
        +-----------------------------+
        | Type: {type_str.ljust(21)} |
        | HP:      {str(self.hp).ljust(18)} |
        | Attack:  {str(self.attack).ljust(18)} |
        | Defense: {str(self.defense).ljust(18)} |
        | Speed:   {str(self.speed).ljust(18)} |
        +-----------------------------+
        """
        return card

class Pokedex:
    def __init__(self, csv_file):
        self.pokemons = {}
        self.csv_file = csv_file
        self.load_from_csv()

    def load_from_csv(self):
        if not os.path.exists(self.csv_file):
            print(f"File {self.csv_file} not found.")
            return

        with open(self.csv_file, mode='r', encoding='utf-8-sig', errors='replace') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Handle potential missing keys or empty values safely
                    name = row.get('name', 'Unknown')
                    p = Pokemon(
                        name=name,
                        type1=row.get('type_1', ''),
                        type2=row.get('type_2', ''),
                        hp=row.get('hp', 0) or 0,
                        attack=row.get('attack', 0) or 0,
                        defense=row.get('defense', 0) or 0,
                        speed=row.get('speed', 0) or 0
                    )
                    self.pokemons[name.lower()] = p
                except ValueError as e:
                    print(f"Error loading pokemon {row.get('name')}: {e}")

    def add_pokemon(self, pokemon):
        if pokemon.name.lower() in self.pokemons:
            print(f"Pokemon {pokemon.name} already exists!")
            return False
        self.pokemons[pokemon.name.lower()] = pokemon
        print(f"Pokemon {pokemon.name} added successfully.")
        return True

    def delete_pokemon(self, name):
        if name.lower() in self.pokemons:
            del self.pokemons[name.lower()]
            print(f"Pokemon {name} deleted successfully.")
            return True
        print(f"Pokemon {name} not found.")
        return False

    def modify_pokemon(self, name, **kwargs):
        if name.lower() in self.pokemons:
            pokemon = self.pokemons[name.lower()]
            # Update attributes if provided in kwargs
            if 'name' in kwargs: 
                # If name changes, we need to update the key in dictionary too (complex, keeping simple for now)
                pass 
            if 'hp' in kwargs: pokemon.hp = int(kwargs['hp'])
            if 'attack' in kwargs: pokemon.attack = int(kwargs['attack'])
            if 'defense' in kwargs: pokemon.defense = int(kwargs['defense'])
            if 'speed' in kwargs: pokemon.speed = int(kwargs['speed'])
            print(f"Pokemon {name} updated.")
            return True
        print(f"Pokemon {name} not found.")
        return False

    def get_pokemon(self, name):
        return self.pokemons.get(name.lower())

    def list_pokemons(self):
        return list(self.pokemons.values())

class Battle:
    @staticmethod
    def simulate(pokemon1, pokemon2):
        print(f"\n--- BATTLE STARTING ---")
        print(f"{pokemon1.name} VS {pokemon2.name}")
        print(f"{pokemon1.name} Attack: {pokemon1.attack}")
        print(f"{pokemon2.name} Attack: {pokemon2.attack}")
        
        if pokemon1.attack > pokemon2.attack:
            winner = pokemon1
            print(f"\nWinner is {winner.name}!")
        elif pokemon2.attack > pokemon1.attack:
            winner = pokemon2
            print(f"\nWinner is {winner.name}!")
        else:
            print("\nIt's a Draw!")
        print("-----------------------")

def main():
    # Use absolute path relative to the script logic to ensure we find the csv
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'pokemon.csv')
    
    pokedex = Pokedex(csv_path)

    if not pokedex.pokemons:
        print("WARNING: No Pokemons loaded! Check if 'pokemon.csv' is in the same folder.")
    else:
        print(f"Successfully loaded {len(pokedex.pokemons)} Pokemons from '{csv_path}'.")

    while True:
        print("\n=== POKEMON BATTLE SYSTEM ===")
        print("1. List All Pokemons")
        print("2. Show Pokemon Card")
        print("3. Add Pokemon")
        print("4. Modify Pokemon")
        print("5. Delete Pokemon")
        print("6. Simulate Battle")
        print("7. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            count = 0
            for p in pokedex.list_pokemons():
                print(f"- {p.name}")
                count += 1
                if count >= 20: # Limit output for CLI readability
                    print("... and many more (showing first 20)")
                    break
        
        elif choice == '2':
            name = input("Enter Pokemon Name: ")
            p = pokedex.get_pokemon(name)
            if p:
                print(p)
            else:
                print("Pokemon not found.")

        elif choice == '3':
            print("Enter New Pokemon Details:")
            name = input("Name: ")
            type1 = input("Type 1: ")
            type2 = input("Type 2 (optional): ")
            try:
                hp = int(input("HP: "))
                attack = int(input("Attack: "))
                defense = int(input("Defense: "))
                speed = int(input("Speed: "))
                new_pokemon = Pokemon(name, type1, type2, hp, attack, defense, speed)
                pokedex.add_pokemon(new_pokemon)
            except ValueError:
                print("Invalid input. Stats must be numbers.")

        elif choice == '4':
            name = input("Enter Pokemon Name to modify: ")
            if pokedex.get_pokemon(name):
                print("Enter new stats (leave blank to keep current):")
                try:
                    hp_in = input("New HP: ")
                    att_in = input("New Attack: ")
                    def_in = input("New Defense: ")
                    spd_in = input("New Speed: ")
                    
                    updates = {}
                    if hp_in: updates['hp'] = int(hp_in)
                    if att_in: updates['attack'] = int(att_in)
                    if def_in: updates['defense'] = int(def_in)
                    if spd_in: updates['speed'] = int(spd_in)
                    
                    pokedex.modify_pokemon(name, **updates)
                except ValueError:
                    print("Invalid input.")
            else:
                print("Pokemon not found.")

        elif choice == '5':
            name = input("Enter Pokemon Name to delete: ")
            pokedex.delete_pokemon(name)

        elif choice == '6':
            name1 = input("Enter First Pokemon Name: ")
            p1 = pokedex.get_pokemon(name1)
            if not p1:
                print(f"{name1} not found.")
                continue
                
            name2 = input("Enter Second Pokemon Name: ")
            p2 = pokedex.get_pokemon(name2)
            if not p2:
                print(f"{name2} not found.")
                continue
                
            Battle.simulate(p1, p2)

        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
