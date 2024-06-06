import agentpy as ap
import matplotlib.pyplot as plt
from Model.Consumer import Consumer
from Model.Company import Company
import numpy as np

class Market(ap.Model):
    

    def setup(self):
        """ Initiate a list of new agents. """
        self.consumers = ap.AgentList(self, self.p.n_consumer_agents, Consumer, positions=self.p.consumer_positions)
        self.companies = ap.AgentList(self, self.p.n_company_agents, Company)

        self.show_env()
    
    def show_env(self):
        #todo: dynamical plot and set each profit to its respective company
        plt.figure(figsize=(10, 8))
        companies_positions = np.empty((0, 2))
        for company in self.companies:
            companies_positions = np.vstack((companies_positions, company.position()))

        for i, (x, y) in enumerate(companies_positions):
            cor = 'green' if self.p.companies_cash[i] >= 0 else 'red'
            plt.text(x, y, f'Cash: ${self.p.companies_cash[i]:.2f}', fontsize=9, ha='center', va='center',
                     bbox=dict(facecolor=cor, alpha=0.3, boxstyle='round,pad=0.3'))

        plt.scatter(companies_positions[:, 0], companies_positions[:, 1], color='red', marker='*', s=200, label='Empresas')

        plt.scatter(self.p.consumer_positions[:,0], self.p.consumer_positions[:,1], color='blue', marker='o', s=100, label='Consumidores')

        plt.title('Initial Market Space')
        plt.xlabel('X Coordinates')
        plt.ylabel('Y Coordinates')
        plt.legend()
        plt.grid(True)

        plt.show()


    def step(self):
        """ Call a method for every agent. """
        #self.agents.agent_method()

    def update(self):
        """ Record a dynamic variable. """
        #self.agents.record('my_attribute')

    def end(self):
        """ Repord an evaluation measure. """
        self.report('my_measure', 1)