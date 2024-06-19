import numpy as np

def utility_function(company, consumer, information_level) -> float:
    distance = np.linalg.norm(company.position() - consumer.position())
    perceived_price = company.price()
    
    if information_level < 1.0:
        # preços com ruído (informação imperfeita)
        perceived_price += np.random.normal(0, (1 - information_level) * perceived_price)
    
    return -perceived_price - distance  # utilidade diminui com maior preço e distância