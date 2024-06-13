import agentpy as ap
import numpy as np

class Consumer(ap.Agent):

    def setup(self, positions):
        self.__position = positions[self.id - 1, :]
        self.__leaved = False
        self.information_level = np.random.uniform(0.5, 1.0)  # nível de informação do consumidor

    def leaved(self):
        return self.__leaved

    def agent_method(self, utility_values):
        if np.any(utility_values > 0):
            # produto com maior utilidade
            pref_company_index = np.argmax(utility_values)
            self.__pref_company_index = pref_company_index
        else:
            self.leave_market()

    def leave_market(self):
        self.__leaved = True

    def pref_company_id(self):
        return self.__pref_company_index
    
    def position(self):
        return self.__position
