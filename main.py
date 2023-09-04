# code grovers algorithm using oop

import math

# import the necessary packages
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram


# create a class for grovers algorithm
class Grover:
    def __init__(self, n, m, oracle, backend, shots):
        self.counts = None
        self.result = None
        self.job = None
        self.n = n
        self.m = m
        self.oracle = oracle
        self.backend = backend
        self.shots = shots
        self.qr = QuantumRegister(n)
        self.cr = ClassicalRegister(n)
        self.circuit = QuantumCircuit(self.qr, self.cr)
        self.theta = 2 * math.asin(math.sqrt(m / n))
        self.num_iterations = round(math.pi / (4 * self.theta))
        self.num_iterations = 1 if self.num_iterations == 0 else self.num_iterations
        self.initialize()
        self.grover()
        self.measure()
        self.run()
        self.plot()

    def initialize(self):
        self.circuit.h(self.qr)
        self.circuit.barrier()

    def grover(self):
        for _ in range(self.num_iterations):
            self.oracle()
            self.circuit.barrier()
            self.circuit.h(self.qr)
            self.circuit.barrier()
            self.circuit.x(self.qr)
            self.circuit.barrier()
            self.circuit.h(self.qr)
            self.circuit.barrier()
            self.circuit.x(self.qr)
            self.circuit.barrier()
            self.circuit.h(self.qr)
            self.circuit.barrier()

    def measure(self):
        self.circuit.measure(self.qr, self.cr)

    def run(self):
        self.job = execute(self.circuit, backend=self.backend, shots=self.shots)
        job_monitor(self.job)
        self.result = self.job.result()
        self.counts = self.result.get_counts(self.circuit)

    def plot(self):
        plot_histogram(self.counts)
        plt.show()


# create a class for the oracle
class Oracle:
    def __init__(self, n, m, backend, shots):
        self.counts = None
        self.result = None
        self.job = None
        self.n = n
        self.m = m
        self.backend = backend
        self.shots = shots
        self.qr = QuantumRegister(n)
        self.cr = ClassicalRegister(n)
        self.circuit = QuantumCircuit(self.qr, self.cr)
        self.initialize()
        self.oracle()
        self.measure()
        self.run()
        self.plot()

    def initialize(self):
        self.circuit.x(self.qr[self.n - 1])
        self.circuit.h(self.qr)
        self.circuit.barrier()

    def oracle(self):
        self.circuit.h(self.qr[self.n - 1])
        self.circuit.mct(self.qr[0:self.n - 1], self.qr[self.n - 1], None, mode='noancilla')
        self.circuit.h(self.qr[self.n - 1])
        self.circuit.barrier()

    def measure(self):
        self.circuit.measure(self.qr, self.cr)

    def run(self):
        self.job = execute(self.circuit, backend=self.backend, shots=self.shots)
        job_monitor(self.job)
        self.result = self.job.result()
        self.counts = self.result.get_counts(self.circuit)

    def plot(self):
        plot_histogram(self.counts)
        plt.show()


# create a class for the diffusion operator
class Diffusion:
    def __init__(self, n, backend, shots):
        self.counts = None
        self.result = None
        self.job = None
        self.n = n
        self.backend = backend
        self.shots = shots
        self.qr = QuantumRegister(n)
        self.cr = ClassicalRegister(n)
        self.circuit = QuantumCircuit(self.qr, self.cr)
        self.initialize()
        self.diffusion()
        self.measure()
        self.run()
        self.plot()

    def initialize(self):
        self.circuit.h(self.qr)
        self.circuit.barrier()

    def diffusion(self):
        self.circuit.x(self.qr)
        self.circuit.h(self.qr[self.n - 1])
        self.circuit.mct(self.qr[0:self.n - 1], self.qr[self.n - 1], None, mode='noancilla')
        self.circuit.h(self.qr[self.n - 1])
        self.circuit.x(self.qr)
        self.circuit.barrier()

    def measure(self):
        self.circuit.measure(self.qr, self.cr)

    def run(self):
        self.job = execute(self.circuit, backend=self.backend, shots=self.shots)
        job_monitor(self.job)
        self.result = self.job.result()
        self.counts = self.result.get_counts(self.circuit)

    def plot(self):
        plot_histogram(self.counts)
        plt.show()


# search for a random number in a list of numbers using grovers algorithm
def search(n, m, backend, shots):
    oracle = Oracle(n, m, backend, shots)
    grover = Grover(n, m, oracle.oracle, backend, shots)
    return grover.counts


# define the main function
def main():
    # define the number of qubits
    n = 3
    # define the number of iterations
    m = 3
    # define the backend
    backend = Aer.get_backend('qasm_simulator')
    # define the number of shots
    shots = 1024
    # run the search algorithm
    counts = search(n, m, backend, shots)
    # visualize the circuit
    visualize(create_circuit())
    # print the results
    print(counts)


def visualize(circuit):
    circuit.draw(output='mpl')
    plt.show()


def create_circuit():
    # define the number of qubits
    n = 3
    # define the number of iterations
    m = 3
    # define the backend
    backend = Aer.get_backend('qasm_simulator')
    # define the number of shots
    shots = 1024
    # run the search algorithm
    counts = search(n, m, backend, shots)
    return counts


# call the main function
if __name__ == "__main__":
    main()
