# Standard library imports
import os

# Third-party imports
# Environment management
from dotenv import find_dotenv, load_dotenv

# AgentOps
import agentops

# Dash framework
from dash import Dash, dcc, html, callback, Output, Input, State, no_update

# LangChain imports
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.load import dumps, loads
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Initialize AgentOps
agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), auto_start_session=False)

# Define LLM and Tools
llm = ChatOpenAI(temperature=0)
tavily_tool = TavilySearchResults()
tools = [tavily_tool]

# Define Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant. Use the tavily_search_results_json tool for information."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

# Define function to process chat
def process_chat(agent_executor, user_input, chat_history):
    session = agentops.start_session(tags=["chat-interaction"])  # Start session
    try:
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        session.end_session("Success")  # End session successfully
        return response["output"]
    except Exception as e:
        session.end_session("Fail", end_state_reason=str(e))  # End session on failure
        return "Error processing request."

# Create Dash App
app = Dash()
app.layout = html.Div([
    html.H2("Ask me anything. I'm your Agency personal assistant that can search the web"),
    dcc.Input(id="my-input", type="text", debounce=True, style={"width": "500px", "height": "30px"}),
    html.Br(),
    html.Button("Submit", id="submit-query", style={"backgroundColor": "blue", "color": "white"}),
    dcc.Store(id="store-it", data=[]),
    html.P(),
    html.Div(id="response-space")
])

# Define callback function
@callback(
    Output("response-space", "children"),
    Output("store-it", "data"),
    Input("submit-query", "n_clicks"),
    State("my-input", "value"),
    State("store-it", "data"),
    prevent_initial_call=True
)
def interact_with_agent(n, user_input, chat_history):
    if len(chat_history) > 0:
        chat_history = loads(chat_history)

    response = process_chat(agent_executor, user_input, chat_history)
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))

    history = dumps(chat_history)

    return f"Assistant: {response}", history

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
