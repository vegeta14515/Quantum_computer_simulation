import secrets as st, sympy

"""

registre de taille n = n qubits
nombre de registre = N
=> registre N_1,N_2,etc
=> position du qubit dans ce registre : q_1,q_2,etc

étapes : 
-fonction de mesure et réduction du paquet d"onde
-portes quantiques de bases : Pauli-X, Hadamard, CNOT

amplitudes : list, # [a_0,a_1]
probabilities : list, # [p_0,p_1]    
                 
"""

class Qubits:
    def __init__(
                 self,
                 register_qubits_number : int, # 0-N
                 register_qubits_position : int, # 0-n
                 state : str, # [created,measured,superposed,entangled]
                 value : int, # |0> or |1>
                 generation_method : str, # generation,attribution
                 ):
        
        self.attributes = {
            "register_qubits_number": register_qubits_number,
            "position_qubits": register_qubits_position,
            "state": state,
            "value": value,
            "amplitudes": [0 + 0j, 0 + 0j],
            "probabilities": [0, 0],
            "generation_method": generation_method
        }
        
    def amplitudes_def(self):
        self.attributes["amplitudes"][0] = complex(round(st.randbelow(10001) / 100, 2),round(st.randbelow(10001) / 100, 2))
        self.attributes["amplitudes"][1] = complex(round(st.randbelow(10001) / 100, 2),round(st.randbelow(10001) / 100, 2))
        return self.attributes["amplitudes"]
    
    def normalization(self):
        module : int = abs(self.attributes["amplitudes"][0])**2 + abs(self.attributes["amplitudes"][1])**2
        module_sqrt : int = sympy.sqrt(module)
        if module!=1 : 
            self.attributes["amplitudes"][0] /= module_sqrt
            self.attributes["amplitudes"][1] /= module_sqrt
        return self.attributes["amplitudes"]
    
    def probability_def(self):
        self.attributes["probabilities"][0]=abs(self.attributes["amplitudes"][0])**2
        self.attributes["probabilities"][1]=abs(self.attributes["amplitudes"][1])**2
        return self.attributes["probabilities"]
    
    def initialize_qubit(self):
        self.amplitudes_def()
        self.normalization()
        self.probability_def()
    
    def __getitem__(self, key):
    # Accès aux attributs comme s'ils faisaient partie d'un dictionnaire
        return self.attributes.get(key, f"Clé '{key}' inexistante.")

    def __setitem__(self, key, value):
        # Modification des attributs comme s'ils faisaient partie d'un dictionnaire
        if key in self.attributes:
            self.attributes[key] = value
        else:
            raise KeyError(f"Clé '{key}' inexistante.")

    def __repr__(self):
        # Représentation lisible de l'objet Qubits
        return f"Qubits({self.attributes})"


    
class Register_qubits:
    def __init__(self,register_qubits_number : int):
        self.register_number = register_qubits_number # number of registers
        r : int = register_qubits_number
        q_0 = Qubits(r,0,"created",0,"generation")
        q_1 = Qubits(r,1,"created",0,"generation")
        q_2 = Qubits(r,2,"created",0,"generation")
        q_3 = Qubits(r,3,"created",0,"generation")
        q_4 = Qubits(r,4,"created",0,"generation")
        q_5 = Qubits(r,5,"created",0,"generation")
        q_6 = Qubits(r,6,"created",0,"generation")
        q_7 = Qubits(r,7,"created",0,"generation")
    
#    def __str__(self):
#       return f"Register Number: {self.register_number}"

class Bits:
    
    # self.attributes à mettre dans le commentaire suivant
    
    """
    def __init__(
                self,
                register_bits_number : int, # 0-N
                postion_bits : int, # 0-n
                value : int, # 0 or 1
                ):
        self.register_bits_number = register_bits_number
        self.position_bits = postion_bits
        self.value = value
    """
    
    
    
    def __repr__(self):
        # Représentation lisible des attributs de l"objet Bits
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
        # Permet d"accéder aux bits
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
        
        
        
qubit_0 = Qubits(1,0,"created",0,"generation")
print(qubit_0)
qubit_0.initialize_qubit()
print(qubit_0)
        
        
        
        
        

"""
class Gate:
    def __init__(self,entree,sortie,type): # type : register, qubit, n-qubit
        pass
"""


"""

ce qu"il reste à faire : 
-implémenter le mode génération et attribution pour les probas
-
-

"""
