import requests
from agents import function_tool, Agent, Runner, ModelSettings

instructions = """
Você é um agente de atendimento ao cliente.

1. Sempre classifique a intenção do usuário utilizando a ferramenta disponível.
2. Utilize a classificação com a mensagem do usuário para retornar a intenção daquela mensagem.
3. Responda de maneira educada e objetiva.
4. Não invente informações.
""" 

@function_tool
def classificar_intencao(texto: str) -> str:
    """Classifica a intenção de uma mensagem de atendimento ao cliente."""

    response = requests.post(
        "http://127.0.0.1:8000/classify_padrao",
        json={"message": texto},
        timeout=5
    )

    response.raise_for_status()
    dados = response.json()

    resposta_final = f"Intenção: {dados['intent']}. \
              Probability: {dados['probability']}"
    print(resposta_final)

    return (resposta_final)

def configurar_agent():
    agent = Agent(
        name="Atendente",
        instructions=instructions,
        tools=[classificar_intencao],
        tool_use_behavior="stop_on_first_tool",
        model_settings=ModelSettings(tool_choice="classificar_intencao")
    )
    return agent

def classificar (prompt_user):
    agent = configurar_agent()
    resposta = Runner.run_sync(agent, prompt_user)
    return resposta