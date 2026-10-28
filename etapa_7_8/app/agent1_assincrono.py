import asyncio
from agents import Agent, Runner

async def main(agent, prompt_user):
    result = await Runner.run(agent, prompt_user)
    print(result.final_output)

agent = Agent(
    name="Atendente",
    instructions="Você é um atendente de suporte ao cliente."
)
prompt_user = "Olá, gostaria de cancelar meu pedido."

asyncio.run(main(agent, prompt_user))