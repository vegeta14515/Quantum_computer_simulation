import secrets as st, sympy, math, random

print("")

class Qubits:
    def __init__(
                 self,
                 position_register_qubits : int, # 0-N
                 qubits_position : int, # 0-n
                 # state : dict,  [created,measured,superposed,entangled]
                 value : int, # |0> or |1>
                 generation_method : str, # generation,attribution
                 *args
                 ):
        
        self.attributes = {
            "position_register_qubits": position_register_qubits,
            "position_qubits": qubits_position,
            "state" : {
                "created" :  0,
                "measured" : 0,
                "superposed" : 0,
                "entangled" : 0
                },
            "value": value,
            "amplitudes": [0 + 0j, 0 + 0j],
            "probabilities": [0.00, 0.00],
            "generation_method": generation_method
        }
                
        self.initialize_qubit(generation_method,*args)
        
    def amplitudes_def(self):
        self.attributes["amplitudes"][0] = complex(round(st.randbelow(10001) / 100, 2),round(st.randbelow(10001) / 100, 2))
        self.attributes["amplitudes"][1] = complex(round(st.randbelow(10001) / 100, 2),round(st.randbelow(10001) / 100, 2))
        return self.attributes["amplitudes"]
    
    def normalization(self):
        module : int = abs(self.attributes["amplitudes"][0])**2 + abs(self.attributes["amplitudes"][1])**2
        module_sqrt : int = math.sqrt(module)
        if module!=1 : 
            self.attributes["amplitudes"][0] = self.attributes["amplitudes"][0]/module_sqrt
            self.attributes["amplitudes"][0] = complex(round(complex(self.attributes["amplitudes"][0]).real, 2), round(complex(self.attributes["amplitudes"][0]).imag, 2))
            self.attributes["amplitudes"][1] = self.attributes["amplitudes"][1]/module_sqrt
            self.attributes["amplitudes"][1] = complex(round(complex(self.attributes["amplitudes"][1]).real, 2), round(complex(self.attributes["amplitudes"][1]).imag, 2))
        return self.attributes["amplitudes"]
    
    def probability_def(self):
        self.attributes["probabilities"][0] = round(abs(self.attributes["amplitudes"][0])**2,2)
        self.attributes["probabilities"][1] = round(abs(self.attributes["amplitudes"][1])**2,2)
        return self.attributes["probabilities"]
    
    def initialize_qubit(
                        self, 
                         generation_method: str,
                         *args
                         ):
        
        if generation_method == "generation":
            self.amplitudes_def()
            self.normalization()
            self.probability_def()

        elif generation_method == "attribution":
            if len(args) != 2:
                raise ValueError(f'Le mode "attribution" nécessite deux arguments mais {len(args)} argument(s) ont été fournis.')
            else : 
                new_amplitudes_0, new_amplitudes_1 = args
                self.attributes["amplitudes"] = [new_amplitudes_0, new_amplitudes_1]
                self.normalization()
                self.probability_def()
                
        else:
            raise ValueError("Méthode de génération non reconnue. Utilisez 'generation' ou 'attribution'.")
        
        self.attributes["state"]["created"] = 1
    
    """
    def __getitem__(self, key):
        return self.attributes.get(key, f"Clé '{key}' inexistante.")

    def __setitem__(self, key, value):
        if key in self.attributes:
            self.attributes[key] = value
        else:
            raise KeyError(f"Clé '{key}' inexistante.")

    def __repr__(self):
        return str(self.attributes)
    """
    
    def Measure_chained(
                self,
                nb_measure : int
               ):
        results = []
        count_0, count_1 = 0, 0
        for i in range(0,nb_measure):
            result = random.choices([0, 1], weights=self.attributes["probabilities"])[0]
            results.append(result)
            if result == 0 : 
                count_0 += 1
            elif result == 1:
                count_1 += 1
            else : 
                raise ValueError(f"Une erreur est survenue lors de la mesure")
        print(f"Nombre de |0> mesurés : {count_0/100000}, Nombre de |1> mesurés : {count_1/100000}")
        return count_0, count_1
                    
    
    def Measure_normal(self):  
        result = random.choices([0, 1], weights=self.attributes["probabilities"])[0]
        if result == 0:
            self.attributes["amplitudes"] = [1 + 0j, 0 + 0j]
            
        else:
            self.attributes["amplitudes"] = [0 + 0j, 1 + 0j]
        
        self.attributes["probabilities"] = [1.0 if result == 0 else 0.0, 1.0 if result == 1 else 0.0]
        self.attributes["state"]["measured"] = 1
        self.attributes["value"] = result
        return result

def modify_qubit(qubit, value : str, after):
    qubit.attributes[value] = after

class Register_qubits:
    def __init__(self, 
                 position_register_qubits: int,
                 size: int,
                 generation_method: str,
                 *args
                 ):
        
        self.attributes = {
            "position_register_qubits": position_register_qubits,
            "size": size,
            "generation_method": generation_method
        }
        
        self.qubits = []
        
        if generation_method == "generation":
            for n in range(size):
                qubit = Qubits(position_register_qubits, n, 0, generation_method)
                self.qubits.append(qubit)
        
        elif generation_method == "attribution":
            if len(args) != 2:
                raise ValueError(f'Le mode "attribution" nécessite deux arguments pour les amplitudes, mais {len(args)} argument(s) ont été fourni(s).')
            new_amplitudes_0, new_amplitudes_1 = args
            for n in range(size):
                qubit = Qubits(position_register_qubits, n, 0, generation_method, new_amplitudes_0, new_amplitudes_1)
                self.qubits.append(qubit)
            self.attributes["amplitudes"] = qubit.attributes["amplitudes"]
            self.attributes["probabilties"] = qubit.attributes["probabilities"]
        else:
            raise ValueError("Méthode de génération non reconnue. Utilisez 'generation' ou 'attribution'.")

    def get_qubit(self, index: int):
        # Accéder à un qubit spécifique par son index
        if 0 <= index < len(self.qubits):
            return self.qubits[index]
        else:
            raise IndexError("Index de qubit invalide.")
    
    def __repr__(self):
        qubits_info = ', '.join([str(qubit.attributes) for qubit in self.qubits])
        return f"Register_qubits({self.attributes}, Qubits: [{qubits_info}])"



# Exemple d'utilisation
r_0 = Register_qubits(0,2,"generation")

# Accéder au premier qubit
first_qubit = r_0.get_qubit(0)

print(r_0)

print("")

# Utiliser la méthode de mesure de Qubits
# first_qubit.Measure_chained(100000)


















#    def __str__(self):
#       return f"Register Number: {self.register_number}"

class Bits:

    def __init__(
                self,
                register_bits_number : int, # 0-N
                postion_bits : int, # 0-n
                value : int, # 0 or 1
                ):
        
        self.attributes = {
            "register_bits_number" : register_bits_number,
            "position_bits" : postion_bits,
            "value" : value
        }
        
    def __repr__(self):
        return f"Bits(register={self.register_bits_number}, position={self.position_bits}, value={self.value})"
    
class Register_bits:
    def __init__(self,register_bits_number : int):
        self.bits = []
        r : int = register_bits_number
        b_0 = Bits(r,0,0)
        b_1 = Bits(r,1,0)
        b_2 = Bits(r,2,0)
        b_3 = Bits(r,3,0)
        b_4 = Bits(r,4,0)
        b_5 = Bits(r,5,0)
        b_6 = Bits(r,6,0)
        b_7 = Bits(r,7,0)
        
        for i in range(8):
            self.bits.append(Bits(register_bits_number, i, 0))
            
    def __getitem__(self, key):
        # Permet d'accéder aux bits
        return self.bits[key]

    def __setitem__(self, key, value):
        # Permet de modifier les bits
        if key in self.bits:
            self.bits[key].value = value
        else:
            raise KeyError(f"Le bit à la position {key} n'existe pas dans ce registre.")

#r_q_0 = Register_qubits(0)
#r_b_0 = Register_bits(0)
#print(r_b_0[7])
        
        
        

        
        
        
        

"""
class Gate:
    def __init__(self,entree,sortie,type): # type : register, qubit, n-qubit
        pass
"""


"""

ce qu"il reste à faire : 
-implémenter la personalisation de la création des qubits d'un registre
-

"""
