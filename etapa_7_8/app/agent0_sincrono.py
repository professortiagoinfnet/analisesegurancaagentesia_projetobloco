from agents import Agent, Runner
agent = Agent(
    name="Atendente",
    instructions="Você é um atendente de suporte ao cliente."
)
prompt_user = "Olá, gostaria de cancelar meu pedido."
resposta = Runner.run_sync(agent, prompt_user)
print(resposta.final_output)