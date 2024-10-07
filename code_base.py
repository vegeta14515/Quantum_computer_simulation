import secrets as st, builtins as bt, random as rd, math, sympy
from sympy import re, im, sqrt

settings_computer = {
    "qubits_number": 5, # nombre de qubit de l'ordinateur quantique
    "bits_number": 5, # nombre de bits de l'ordinateur quantique
    "complex-generation-method": "attribution" # generation, attribution
}

qubit = {
    "number": "", # position du qubit
    "state": "crée", # crée, mesuré, superposition, intrication
    "value" : 0, # 0, 1
    "n_qubit" : "1_qubit", # qubits simples
    "probability_0": "", # amplitude de probabilité de 0
    "probability_1": "", # amplitude de probabilité de 1
    "proba_0": "", # probabilité de mesurer 0
    "proba_1": "" # probabilité de mesurer 1
}

bit = {
    "number" : "",
    "value" : ""
}

# création des variables
registre_total, registre_1, bits, real_0, real_1, imaginary_0, imaginary_1, probm_0, probm_1 = [], [], [], [], [], [], [], [], []
a, b, c, d = 1, 0, 1, 0
registre_total = [registre_1]

# raccourcis
sc = settings_computer
qn = int(sc["qubits_number"])
bn = int(sc["bits_number"])
cgm = sc["complex-generation-method"]
pb_0 = "probability_0"
pb_1 = "probability_1"

# initialisation des listes
for i in range(0,qn):
    registre_1.append(dict(qubit))
    registre_1[i]["number"] = i
    bits.append(dict(bit))
    bits[i]["number"] = i
    real_0.append(0)
    real_1.append(0)
    imaginary_0.append(0)
    imaginary_1.append(0)
    probm_0.append(0)
    probm_1.append(0)

# création des fonctions de simulation
def generation_complex_0(qubit):
    real_0[qubit] = round(st.randbelow(10001) / 100, 2)
    imaginary_0[qubit] = round(st.randbelow(10001) / 100, 2)
    registre_1[qubit][pb_0] = complex(real_0[qubit], imaginary_0[qubit])

def generation_complex_1(qubit):
    real_1[qubit] = round(st.randbelow(10001) / 100, 2)
    imaginary_1[qubit] = round(st.randbelow(10001) / 100, 2)
    registre_1[qubit][pb_1] = complex(real_1[qubit], imaginary_1[qubit])

def attribution(qubit):
    registre_1[qubit][pb_0] = complex(a, b)
    registre_1[qubit][pb_1] = complex(c, d)

def norm(qubit):
    if round(abs(registre_1[qubit][pb_0])**2 + abs(registre_1[qubit][pb_1])**2) == 1:
        return 1
    else:
        return abs(registre_1[qubit][pb_0])**2 + abs(registre_1[qubit][pb_1])**2

def normalisation(qubit):
    norm_value = sqrt(abs(registre_1[qubit][pb_0])**2 + abs(registre_1[qubit][pb_1])**2)
    if norm_value != 1:
        registre_1[qubit][pb_0] /= norm_value
        registre_1[qubit][pb_1] /= norm_value
    registre_1[qubit]["proba_0"] = abs(registre_1[qubit][pb_0])**2
    registre_1[qubit]["proba_1"] = abs(registre_1[qubit][pb_1])**2

def calculs_proba(qubit):
    probm_0[qubit] = re(registre_1[qubit][pb_0])**2 + im(registre_1[qubit][pb_0])**2
    probm_1[qubit] = re(registre_1[qubit][pb_1])**2 + im(registre_1[qubit][pb_1])**2
    registre_1[qubit]["proba_0"] = probm_0[qubit]
    registre_1[qubit]["proba_1"] = probm_1[qubit]

# reproduction d'un qubit 
def simulation(qubit):
    if cgm == "generation":
        generation_complex_0(qubit)
        generation_complex_1(qubit)
    else:
        attribution(qubit)
    calculs_proba(qubit)
    normalisation(qubit)

for qubit in range(qn):
    simulation(qubit)

# fonction de réduction du paquet d'onde
def reduction(qubit):
    registre_1[qubit]["probability_0"] = ""
    registre_1[qubit]["probability_1"] = ""
    registre_1[qubit]["proba_0"] = ""
    registre_1[qubit]["proba_1"] = ""
    registre_1[qubit]["state"] = "mesuré"

# mesure d'un qubit
def mesure(qubit):
    if registre_1[qubit]["proba_0"] == 1 or registre_1[qubit]["proba_1"] == 1:
        if registre_1[qubit]["proba_0"] == 1:
            registre_1[qubit]["value"] = 0
            reduction(qubit)
            bits[qubit]["value"] = 0
            return 0
        else:
            registre_1[qubit]["value"] = 1
            reduction(qubit)
            bits[qubit]["value"] = 1
            return 1
    else:
        rand = rd.random()
        if rand >= registre_1[qubit]["proba_0"]:
            registre_1[qubit]["value"] = 1
            reduction(qubit)
            bits[qubit]["value"] = 1
            return 1
        else:
            registre_1[qubit]["value"] = 0
            reduction(qubit)
            bits[qubit]["value"] = 0
            return 0

# porte de hadamard
def porte_h(qubit):
    if registre_1[qubit]["value"] == 0 or registre_1[qubit]["value"] == 1:
        if registre_1[qubit]["value"] ==0 :
            registre_1[qubit]["state"] = "superposition"
            registre_1[qubit][pb_0] = 1/sympy.sqrt(2)
            registre_1[qubit][pb_1] = 1/sympy.sqrt(2)
        else:
            registre_1[qubit]["state"] = "superposition"
            registre_1[qubit][pb_0] = 1/sympy.sqrt(2)
            registre_1[qubit][pb_1] = -(1/sympy.sqrt(2))
    else:
        registre_1[qubit]["state"] = "superposition"
        inter_0 = registre_1[qubit][pb_0]
        registre_1[qubit][pb_0] = (registre_1[qubit][pb_0] + registre_1[qubit][pb_1])/sympy.sqrt(2)
        registre_1[qubit][pb_1] = (inter_0 - registre_1[qubit][pb_1])/sympy.sqrt(2)
    calculs_proba(qubit)

# porte de pauli-x (=not)
def porte_pauli_x(qubit):
    if registre_1[qubit]["state"] == "superposition":
        inter_0 = registre_1[qubit]["proba_0"]
        registre_1[qubit]["proba_0"] = registre_1[qubit]["proba_1"]
        registre_1[qubit]["proba_1"] = inter_0
        calculs_proba(qubit)
    else:
        registre_1[qubit]["value"] = 1 - registre_1[qubit]["value"]

porte_pauli_x(1)
print(registre_1)