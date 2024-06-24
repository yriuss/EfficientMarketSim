import agentpy as ap
import matplotlib.pyplot as plt
from Model.Consumer import Consumer
from Model.Company import Company
from Model.Coordinator import Coordinator
import numpy as np
import csv

def save_dict_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])

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
        if(self.p.plot):
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
        if(self.p.plot):
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
        
        self.coordinator[0].record('number_companies', self.coordinator[0].number_companies())
        self.coordinator[0].record('number_consumers', self.coordinator[0].number_consumers())
        
    def end(self):
        """ Registra uma medida de avaliação. """
        self.coordinator.end()
        self.report('my_measure', 1)
    
    def show_results(self):
        """ Mostra os resultados da simulação. """
        fig, axs = plt.subplots(2, 2, figsize=(10, 12))  # Cria uma figura com 2 subplots (1 coluna, 2 linhas)

        companies_strategy1 = 0
        companies_strategy2 = 0
        companies_strategy3 = 0

        begin_companies_strategy1 = 0
        begin_companies_strategy2 = 0
        begin_companies_strategy3 = 0

        for i, company in enumerate(self.companies):
            axs[0, 0].plot(company.recorded('cash'), label=f'Empresa {company.id} - Caixa')
            axs[0, 1].plot(company.recorded('price'), label=f'Empresa {company.id} - Preço')

            if company.strategy() == 1:
                companies_strategy1 += 1
            elif company.strategy() == 2:
                companies_strategy2 += 1
            elif company.strategy() == 3:
                companies_strategy3 += 1
            
            if self.p.strategies[i] == 1:
                begin_companies_strategy1 += 1
            elif self.p.strategies[i] == 2:
                begin_companies_strategy2 += 1
            elif self.p.strategies[i] == 3:
                begin_companies_strategy3 += 1
        
        axs[1, 0].plot(self.coordinator[0].recorded('number_companies'))
        axs[1, 1].plot(self.coordinator[0].recorded('number_consumers'))

        # Configuração do primeiro subplot (Caixa)
        axs[0, 0].set_title('Caixa das Empresas')
        axs[0, 0].set_xlabel('Passos')
        axs[0, 0].set_ylabel('Caixa')
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        # Configuração do segundo subplot (Preço)
        axs[0, 1].set_title('Preço das Empresas')
        axs[0, 1].set_xlabel('Passos')
        axs[0, 1].set_ylabel('Preço')
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        axs[1, 0].set_title('Número de Empresas')
        axs[1, 0].set_xlabel('N')
        axs[1, 0].set_ylabel('Passos')
        axs[1, 0].grid(True)

        axs[1, 1].set_title('Número de Consumidores')
        axs[1, 1].set_xlabel('N')
        axs[1, 1].set_ylabel('Passos')
        axs[1, 1].grid(True)

        plt.tight_layout()  # Ajusta a disposição dos subplots para evitar sobreposição
        plt.show()

        

        data = {
            'Número de empresas utilizando a estratégia 1 (final)':companies_strategy1,
            'Número de empresas utilizando a estratégia 2 (final)':companies_strategy2,
            'Número de empresas utilizando a estratégia 3 (final)':companies_strategy3,
            'Número de empresas utilizando a estratégia 1 (começo)':begin_companies_strategy1,
            'Número de empresas utilizando a estratégia 2 (começo)':begin_companies_strategy2,
            'Número de empresas utilizando a estratégia 3 (começo)':begin_companies_strategy3,
            'Número de empresas (final)': self.coordinator[0].recorded('number_companies')[-1],
            'Número de consumidores (final)': self.coordinator[0].recorded('number_consumers')[-1]

        }

        headers = list(data.keys())
        values = np.array(list(data.values()))
        save_dict_to_csv("results_file.csv", data)


