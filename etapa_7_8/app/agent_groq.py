import os
from openai import AsyncOpenAI

import requests
from agents import function_tool, Agent, Runner, ModelSettings, OpenAIChatCompletionsModel

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

    return (f"Intenção: {dados['intent']}. \
              Probability: {dados['probability']}")

def configurar_agent():
    client = AsyncOpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )

    model = OpenAIChatCompletionsModel(
        model="openai/gpt-oss-20b",
        openai_client=client
    )

    agent = Agent(
        name="Atendente",
        model=model,
        instructions=instructions,
        tools=[classificar_intencao],
        tool_use_behavior="stop_on_first_tool",
        model_settings=ModelSettings(tool_choice="classificar_intencao")
    )
    return agent

def classificar_groq (prompt_user):
    agent = configurar_agent()
    resposta = Runner.run_sync(agent, prompt_user)
    return resposta