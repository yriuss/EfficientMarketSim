import agentpy as ap
import matplotlib.pyplot as plt
from Model.Consumer import Consumer
from Model.Company import Company
from Model.Coordinator import Coordinator
import numpy as np

class Market(ap.Model):

    def setup(self):
        """ Inicializa uma lista de novos agentes. """
        self.consumers = ap.AgentList(self, self.p.n_consumer_agents, Consumer)
        self.companies = ap.AgentList(self, self.p.n_company_agents, Company)
        self.coordinator = ap.AgentList(self, 1, Coordinator)

        for consumer in self.consumers:
            self.coordinator.register_consumer(consumer)
    
        for company in self.companies:
            self.coordinator.register_company(company)

        self.coordinator.start_process()
        self.fig, self.ax = plt.subplots(figsize=(10, 8))  # Inicializa a figura e os eixos
        self.show_env()
        
    def show_env(self):
        self.ax.clear()  # Limpa os eixos

        companies_positions = np.empty((0, 2))
        consumer_positions = np.empty((0, 2))
        
        for company in self.companies:
            companies_positions = np.vstack((companies_positions, company.position()))

        for consumer in self.coordinator.consumers()[0]:
            consumer_positions = np.vstack((consumer_positions, consumer.position()))

        for i, (x, y) in enumerate(companies_positions):
            cor = 'green' if self.companies[i].cash() >= 0 else 'red'
            self.ax.text(x, y, f'Cash: ${self.companies[i].cash():.2f}', fontsize=9, ha='center', va='center',
                         bbox=dict(facecolor=cor, alpha=0.3, boxstyle='round,pad=0.3'))

        self.ax.scatter(companies_positions[:, 0], companies_positions[:, 1], color='red', marker='*', s=200, label='Empresas')
        self.ax.scatter(consumer_positions[:, 0], consumer_positions[:, 1], color='blue', marker='o', s=100, label='Consumidores')

        self.ax.set_title('Initial Market Space')
        self.ax.set_xlabel('X Coordinates')
        self.ax.set_ylabel('Y Coordinates')
        self.ax.legend()
        self.ax.grid(True)
        
        plt.draw()  # Atualiza o gráfico
        plt.pause(0.1)  # Pausa para que o gráfico seja atualizado

    def step(self):
        self.coordinator.process()
        self.show_env()
    
    def update_env(self):

        plt.figure(figsize=(10, 8))
        companies_positions = np.empty((0, 2))
        consumer_positions = np.empty((0, 2))
        for company in self.companies:
            companies_positions = np.vstack((companies_positions, company.position()))

        for consumer in self.consumers:
            consumer_positions = np.vstack((consumer_positions, consumer.position()))

        for i, (x, y) in enumerate(companies_positions):
            cor = 'green' if self.p.companies_cash[i] >= 0 else 'red'
            plt.text(x, y, f'Cash: ${self.p.companies_cash[i]:.2f}', fontsize=9, ha='center', va='center',
                     bbox=dict(facecolor=cor, alpha=0.3, boxstyle='round,pad=0.3'))
        
        plt.scatter(companies_positions[:, 0], companies_positions[:, 1], color='red', marker='*', s=200, label='Empresas')
        plt.scatter(consumer_positions[:, 0], consumer_positions[:, 1], color='blue', marker='o', s=100, label='Consumidores')

        plt.draw()
        plt.pause(0.1)


        




    def update(self):
        """ Atualiza variáveis dinâmicas. """
        for company in self.companies:
            company.record('cash', company.cash())
            company.record('price', company.price())
        
    def end(self):
        """ Registra uma medida de avaliação. """
        self.coordinator.end()
        self.report('my_measure', 1)
    
    def show_results(self):
        """ Mostra os resultados da simulação. """
        plt.figure(figsize=(10, 8))
        for company in self.companies:
            plt.plot(company.recorded('cash'), label=f'Empresa {company.id} - Caixa')
            plt.plot(company.recorded('price'), label=f'Empresa {company.id} - Preço')
        plt.title('Resultados da Simulação de Mercado')
        plt.xlabel('Passos')
        plt.ylabel('Valores')
        plt.legend()
        plt.grid(True)
        plt.show()
