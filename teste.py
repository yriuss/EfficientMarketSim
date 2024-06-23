import matplotlib.pyplot as plt
import numpy as np

# Configuração inicial do plot
plt.ion()  # Modo interativo
fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x, np.sin(x))

# Loop para atualizar o plot
for i in range(10):
    # Atualizar os dados da linha
    line.set_ydata(np.sin(x + i * 0.1))
    
    # Redesenhar o plot
    plt.draw()
    plt.pause(0.1)  # Pausar para que o plot seja atualizado
    
    # Limpar a figura se necessário (não obrigatório)
    # ax.cla()

plt.ioff()  # Desativar o modo interativo
plt.show()  # Mostrar a figura final