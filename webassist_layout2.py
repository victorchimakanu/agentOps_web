from dotenv import find_dotenv, load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.load import dumps, loads
from dash import Dash, dcc, html, callback, Output, Input, State, no_update

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Initialize LLM and tools
llm = ChatOpenAI(temperature=0)
tavily_tool = TavilySearchResults()

# Define the agent's prompt template, instructing it to only search the two URLs
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an intelligent assistant. Your responses must only come from the documentation at 'https://docs.agentops.ai/v1/introduction' and the GitHub repository at 'https://github.com/AgentOps-AI'. Do not use any other sources for information."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Create the agent and executor
agent = create_tool_calling_agent(llm, [tavily_tool], prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=[tavily_tool],
    verbose=True,
)

def process_chat(agent_executor, user_input, chat_history):
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    return response["output"]

# Dash App
app = Dash()

app.layout = html.Div(
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "height": "100vh",
        "backgroundColor": "#1E1E2E",
        "color": "white",
        "fontFamily": "Arial, sans-serif"
    },
    children=[
        html.H2(
            "Ask me anything",
            style={"marginBottom": "10px", "fontSize": "30px", "fontWeight": "bold"}
        ),
        html.H3(
            "I'm your AgentOps web assistant.",
            style={"marginBottom": "20px", "fontSize": "20px", "fontWeight": "bold"}
        ),
        dcc.Input(
            id="my-input",
            type="text",
            debounce=True,
            placeholder="Type your question here...",
            style={
                "width": "80%",
                "maxWidth": "500px",
                "padding": "12px",
                "borderRadius": "10px",
                "border": "none",
                "outline": "none",
                "fontSize": "16px",
                "backgroundColor": "#2A2A3B",
                "color": "white",
                "marginBottom": "15px",
                "textAlign": "center"
            }
        ),
        html.Button(
            "Ask AgentOps",
            id="submit-query",
            style={
                "backgroundColor": "#4A90E2",
                "color": "white",
                "border": "none",
                "padding": "10px 20px",
                "borderRadius": "8px",
                "cursor": "pointer",
                "fontSize": "16px",
                "transition": "0.3s"
            }
        ),
        dcc.Store(id="store-it", data=[]),
        html.Div(id="response-space", style={"marginTop": "20px", "fontSize": "18px"})
    ]
)

@app.callback(
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

    if user_input:
        response = process_chat(agent_executor, user_input, chat_history)
        
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        
        return html.Div(
            f"🤖 AI Response: {response}",
            style={"padding": "10px", "backgroundColor": "#2A2A3B", "borderRadius": "10px"}
        ), dumps(chat_history)
    return no_update, no_update

if __name__ == "__main__":
    app.run_server(debug=True)
