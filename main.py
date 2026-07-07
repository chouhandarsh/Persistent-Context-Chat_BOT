from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
print(r"""
 ██████╗██╗  ██╗ █████╗ ████████╗    ██████╗  ██████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██║     ███████║███████║   ██║       ██████╔╝██║   ██║   ██║
██║     ██╔══██║██╔══██║   ██║       ██╔══██╗██║   ██║   ██║
╚██████╗██║  ██║██║  ██║   ██║       ██████╔╝╚██████╔╝   ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝  ╚═════╝    ╚═╝
""")

FILE_PATH = "history.txt"
MAX_LINES=20
messages=[SystemMessage(content="You are a Human Assistant")]
def trim_history():
    with open(FILE_PATH,'r') as file:
        lines=file.readlines()
    if len(lines)>MAX_LINES:
        lines = lines[-MAX_LINES:]
        with open(FILE_PATH,'w') as file:
            file.writelines(lines)
try:
    with open(FILE_PATH,'r') as file:
        lines = file.readlines()
    for line in lines:
        line=line.strip()
        if line.startswith("User: "):
            messages.append(
                HumanMessage(content=line[6:])
            )
        else:
            messages.append(
                AIMessage(content=line[4:])
            )
except FileNotFoundError:
    pass
print("Enter your Query")
while(True):
    user_input=input("User:")
    if(user_input=='quit'):
        break
    # Add user memory in history
    messages.append(HumanMessage(content=user_input))
    # responses
    with open(FILE_PATH,'a') as file:
        file.write(f"User: {user_input}\n")
    response =  model.invoke(messages)
    print("AI: ", response.content)
    messages.append(AIMessage(content=response.content))
    with open(FILE_PATH,'a') as file:
        file.write(f"AI: {response.content}\n")
    trim_history()
    
    
    