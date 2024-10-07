import secrets as st, random as rd, sympy
from sympy import re, im, sqrt

class Qubit:
    def __init__(self, number, complex_generation_method="attribution"):
        self.number = number
        self.state = "crée"  # crée, mesuré, superposition, intrication
        self.value = 0  # 0 ou 1
        self.probability_0 = 0  # Amplitude complexe pour l'état |0>
        self.probability_1 = 0  # Amplitude complexe pour l'état |1>
        self.proba_0 = 0  # Probabilité de mesurer 0
        self.proba_1 = 0  # Probabilité de mesurer 1
        self.complex_generation_method = complex_generation_method

    def generate_complex(self):
        if self.complex_generation_method == "generation":
            self.probability_0 = complex(round(st.randbelow(10001) / 100, 2), round(st.randbelow(10001) / 100, 2))
            self.probability_1 = complex(round(st.randbelow(10001) / 100, 2), round(st.randbelow(10001) / 100, 2))
        else:
            self.probability_0 = complex(1, 0)  # Default to |0>
            self.probability_1 = complex(1, 0)  # Default to |1>

    def normalize(self):
        norm_value = sqrt(abs(self.probability_0) ** 2 + abs(self.probability_1) ** 2)
        if norm_value != 1:
            self.probability_0 /= norm_value
            self.probability_1 /= norm_value
        self.proba_0 = abs(self.probability_0) ** 2
        self.proba_1 = abs(self.probability_1) ** 2

    def measure(self):
        if rd.random() >= self.proba_0:
            self.value = 1
        else:
            self.value = 0
        self.state = "mesuré"
        self.clear_probabilities()

    def clear_probabilities(self):
        self.probability_0 = 0
        self.probability_1 = 0
        self.proba_0 = 0
        self.proba_1 = 0

    def apply_hadamard(self):
        if self.value == 0:
            self.probability_0 = 1 / sympy.sqrt(2)
            self.probability_1 = 1 / sympy.sqrt(2)
        else:
            self.probability_0 = 1 / sympy.sqrt(2)
            self.probability_1 = -1 / sympy.sqrt(2)
        self.state = "superposition"
        self.normalize()

    def apply_pauli_x(self):
        if self.state == "superposition":
            self.proba_0, self.proba_1 = self.proba_1, self.proba_0
        else:
            self.value = 1 - self.value

class QubitRegister:
    def __init__(self, num_qubits):
        self.qubits = [Qubit(i) for i in range(num_qubits)]

    def simulate(self):
        for qubit in self.qubits:
            qubit.generate_complex()
            qubit.normalize()

    def measure_all(self):
        for qubit in self.qubits:
            qubit.measure()

    def apply_hadamard(self, qubit_index):
        self.qubits[qubit_index].apply_hadamard()

    def apply_pauli_x(self, qubit_index):
        self.qubits[qubit_index].apply_pauli_x()

# Utilisation
register = QubitRegister(num_qubits=5)

# Simulation de tous les qubits
register.simulate()

# Application de la porte de Hadamard sur le qubit 0
register.apply_hadamard(0)

# Mesure de tous les qubits
register.measure_all()

# Application de la porte de Pauli-X sur le qubit 1
register.apply_pauli_x(1)

# Affichage de l'état des qubits
for qubit in register.qubits:
    print(f"Qubit {qubit.number}: Value = {qubit.value}, State = {qubit.state}, Proba_0 = {qubit.proba_0}, Proba_1 = {qubit.proba_1}")
