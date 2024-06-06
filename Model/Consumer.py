import agentpy as ap
import numpy as np

class Consumer(ap.Agent):

    def setup(self, positions):
        self.__position = positions[self.id-1, :]
        self.__leaved = False

    def leaved(self):
        return self.__leaved

    def agent_method(self, utility_values):
        if np.any(utility_values > 0):
            # chose the product with max utility
            pref_company_index = np.argmax(utility_values)
            self.__pref_company_index = pref_company_index
        else:
            self.leave_market()

    def leave_market(self):
        #todo: if consumer has negative utility he leaves the market
        pass
    
    def pref_company_id(self):
        return self.__pref_company_index
    def position(self):
        return self.__position