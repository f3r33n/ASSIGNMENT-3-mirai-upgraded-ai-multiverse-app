import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
# i would be using two ai model api's one gemini and another cohere
from google import genai
import cohere
# HERE WE WOULD CREATE THE MEMORY VAULT
#  session state creates a memeory for storing the previous conversations 
# "if" is imp here cuz it makes sure if session state (basically the contained which stores messages) is present - if container is present then procced with saving other messages
if "messages" not in st.session_state:
    st.session_state.messages = [] # Initialize the Memory Vault
# Before you can display or save messages, you need to create a place to store them that survives page reloads. and that's exactly thei part 
# st.session_state.messages = []
st.title("AI MULTIVERSE - UPDATED")
st.header("Talk to different AI personalities powered by Gemini and Cohere.")
st.write("Ask anything and get AI powered responses")
st.divider()
# CHAT HISTORY WOULD BE SAVED HERE
# Here we showed history  this code block ""for message in st.session_state.messages:"" does the part of showing messages 
# it basically opens the container- shows 1st message then 2nd then 3rd etc etc 
for message in st.session_state.messages:
    # this (message[role]) checks - what excatly is the role? is the user sending messages (role = user) or assistant (role =assistant)
    # so if user is sending then show user chatbubble (user emoji), if assistant is sending - show assistant emoji etc
    with st.chat_message(message["role"]):
        st.write(message["content"]) # content basically shows what the content(message is ) - wheather from assistant or user - it shows the message(content)
#creating a sidebar now
# This sidebar is for selecting modes like  - PERSONALITY and MODELS and RESPONSE LENGTH and CREATIVITY 
# i HAVE MADE THE INDEX NONE SO THAT NOTHING IS WRIITEN IN THERE AND KEPT ONE AS PLACEHOLDER FOR  A MESSAGE TO BE SHOWN IN THE BOX 
personality=st.sidebar.selectbox("who do u want to talk to",["friendly","sarcastic","professional"], index=None , placeholder="select your personality")
models=st.sidebar.selectbox("which model do u want to use",["cohere","gemini"], index=None , placeholder="select your model")
response_length = st.sidebar.selectbox("How long should the response be" ,["long","short","medium"], index=None , placeholder = "select the length")
creativity=st.sidebar.selectbox("how creative do u want the response to be",["low","medium","high"], index=None , placeholder="select your creativity level")
# ADDING A CLEAR CONVERSATION BUTTON 
if st.sidebar.button("🗑️ CLEAR CONVERSATION"):
    st.session_state.messages = []
    st.rerun()
# The old st.text_input() and st.button("SEND") combo is outdated for chat interfaces. SO I MADE st.chat_input
 # this adds an enter button to be pressed inside the chat box ( just like chatgpt)
# lets make this bot( the text box chatgpt style instead of normal)
# For this would make the use of walrus operator :=
# The walrus operator allows you to assign a value to a variable inside an expression (like an if statement) at the exact same time you are testing it.
if user_message := st.chat_input("Your message goes here"):
    if not personality:
        st.error("please select ur personality")
    if not models:
        st.error("please select ur model")
    if not creativity:
        st.error("please select ur creativity level")
    if not response_length:
        st.warning("please enter response length")
    else:
        # setting up cohere model
     # SAVING THE USERS MESSAGE THROUGH APPEND 
        st.session_state.messages.append( # append basically means too add in already created (varibale) or stuff 
            # so append here means to put all the conversation in that conatiner we had already created 
               { "role" : "user",
                 "content" : user_message
                }
                      )
        with st.chat_message("user"):
            st.write(user_message)
        # what happened before was AI ---->> response
        # now what happens is AI -->> OPEN CONTAINER ----> READ EVERYTHING ----> DRAW EVERYTHING AGAIN
        # WHAT HAPPENS IS sending another message actually erases the previous message but in this case the streamlit creates the previous conversation again
        # so it basically seems the conversation history is still there ( but it was erased but created again from scratch)    
        if models=="cohere":
            cohere_client = cohere.ClientV2(api_key =os.getenv("cohere_api_key"))
            # 1. Create a system instruction to hold your personality rules
            system_instruction = f"You are a {models} chatbot with {personality} personality, response length {response_length}, and {creativity} creativity level."
            
            # 2. Build the full conversation history for Cohere
            cohere_messages = [{"role": "system", "content": system_instruction}]
            for m in st.session_state.messages:
                cohere_messages.append({"role": m["role"], "content": m["content"]})
            
            with st.spinner("generating response through cohere hang on there for a moment..."):
                # 3. Pass the full array of messages instead of a single prompt
                response = cohere_client.chat(
                    model="command-a-plus-05-2026", 
                    messages=cohere_messages
                )
            # I created a loop here - it was throwing error otherwise
            for content in response.message.content:
                if content.type == "text":
                    # for saving responses
                    st.session_state.messages.append(
                        {
                            "role" :"assistant",
                            "content" : content.text
                        }
                    )
                    with st.chat_message("assistant"):
                        st.write(content.text)
         # setting up gemini now  
        elif models=="gemini":
            client= genai.Client(api_key = os.getenv("google_api_key"))
            # 1. Map your session history into the specific dictionary format Gemini expects
            # Gemini requires the assistant role to be named "model" instead of "assistant"
            formatted_contents = [] #What it means: We initialize an empty list. This list will become the transcript of your entire conversation history.
            for m in st.session_state.messages: #What it means: This loop opens up your "Memory Vault" (st.session_state.messages) where Streamlit has saved every single message you and the AI sent since the app started. It looks at them one by one.
                gemini_role = "user" if m["role"] == "user" else "model" #What it means: This is a translation step. this app stores the AI's role as "assistant", but the Gemini API explicitly requires the AI's role to be named "model". This line translates "assistant" to "model" so Gemini doesn't reject it.
                formatted_contents.append({
                    "role": gemini_role,
                    "parts": [{"text": m["content"]}]
                })
            
            # 2. Define your system configuration instruction
            system_instruction = f"You are a {models} chatbot with {personality} personality, response length {response_length}, and {creativity} creativity level."
            
            with st.spinner("Generating response through gemini"):
                # 3. Send the full history along with the system instruction config
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=formatted_contents,
                    config={"system_instruction": system_instruction}
                )
            # this loading_screen.empty() is necessary here - once response is generated the laoding screen disappears
                # for saving ai response after response is generated from ai we add this append state at last so the response that got generated get saved at the end 
            st.session_state.messages.append(
                    {
                        "role" : "assistant",
                        "content": response.text
                    }
                )
            with st.chat_message("assistant"):
                    st.write(response.text)

st.caption("Powered by Gemini & Cohere Made with ❤️ by faizan using Streamlit")
            