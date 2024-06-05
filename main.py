import agentpy as ap
import matplotlib.pyplot as plt

class FishingAgent(ap.Agent):
    def setup(self):
        self.fish_caught = 0
        self.role = "Pescador"
        self.max_fish = 20

    def send_message(self, recipient, performative, content):
        message = {'performative': performative, 'content': content}
        recipient.receive_message(message)

    def receive_message(self, message):
        if message['performative'] == 'inform' and message['content'] == 'reduce_fishing':
            self.reaction_to_alert()

    def reaction_to_alert(self):
        self.max_fish = max(5, self.max_fish - 5)

    def decide_fishing(self):
        if self.model.fish_count > 0 and self.role == "Pescador":
            fish_to_catch = min(self.max_fish, self.model.fish_count)
            self.model.fish_count -= fish_to_catch
            self.fish_caught += fish_to_catch

class FisheryModel(ap.Model):
    def setup(self):
        self.fish_count = 1000
        self.agents = ap.AgentList(self, 10, FishingAgent)
        self.fish_counts = []
        self.pesquisador = ap.AgentList(self)  # Cria uma nova lista de agentes para o grupo 1
        self.pescador = ap.AgentList(self)  # Cria uma nova lista de agentes para o grupo 2
        self.create_groups()

    def create_groups(self):
        # Divide os agentes em dois grupos baseados em índice par ou ímpar
        for i, agent in enumerate(self.agents):
            if i % 2 == 0:
                self.pesquisador.append(agent)
            else:
                self.pescador.append(agent)

    def update(self):
        self.fish_count += int(self.fish_count * 0.05)
        if self.fish_count > 1000:
            self.fish_count = 1000
        self.fish_counts.append(self.fish_count)

    def step(self):
        self.agents.decide_fishing()

        if self.fish_count < 300:
            for agent in self.pesquisador:
                for other in self.pescador:
                    agent.send_message(other, 'inform', 'reduce_fishing')

    def end(self):
        total_fish_caught = sum(agent.fish_caught for agent in self.agents)
        print(f"Total de peixes pescados: {total_fish_caught}")
        print(f"Peixes restantes no lago: {self.fish_count}")

parameters = {'steps': 100}
model = FisheryModel(parameters)
model.run()

plt.plot(model.fish_counts)
plt.title('Quantidade de Peixes no Lago ao Longo do Tempo')
plt.xlabel('Passo')
plt.ylabel('Quantidade de Peixes')
plt.show()