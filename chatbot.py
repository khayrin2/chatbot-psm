from openai import OpenAI
import streamlit as st
import replicate
import os
openai_api_key = your_openai_key
os.environ['REPLICATE_API_TOKEN'] = your_replicate_key

# App title
st.set_page_config(page_title="💬 Therapist Chatbot")


def clear_chat_history():
    st.session_state["messages"] = [{"role": "system", "content": "You are a compassionate, supportive, and non-judgmental mental health chatbot designed to provide emotional support, mental wellness resources, and crisis intervention. Please provide a relevant, concise and complete answer, in maximum 3 sentences, that ends with a full stop."}]
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello. I'm your Chatbot Therapist. What brings you here today?"}]


with st.sidebar:
    st.title('💬 Therapist Chatbot')
    st.write("This chatbot is a FYP by Khayrin Nabila. Your data won't be preserved during the course of testing. Thank you for your cooperation.")
    st.info('Please enter your age below', icon="ℹ️")
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a model', ['GPT-3.5', 'Llama2-13B'], key='selected_model')
    temperature = st.sidebar.slider('Creativeness', min_value=0.01, max_value=1.0, value=0.50, step=0.01)
    top_p = st.sidebar.slider('Word Choices', min_value=0.01, max_value=1.0, value=0.80, step=0.01)
    max_length = st.sidebar.slider('Length of responses', min_value=32, max_value=2048, value=256, step=8)
    
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a compassionate, supportive, and non-judgmental mental health chatbot designed to provide emotional support, mental wellness resources, and crisis intervention. Please provide relevant, concise, and complete answers in a maximum of 3 sentences that end with a full stop."}]
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello. I'm your Chatbot Therapist. What brings you here today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)


    #GPT code
    if selected_model == 'GPT-3.5':
      with st.spinner("GPT3.5 is Thinking..."):
        print("I am GPT3.5")
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(model="ft:gpt-3.5-turbo-0125:personal:test2:932ayjvE", 
                                                messages=st.session_state.messages,
                                                max_tokens=max_length,
                                                temperature=temperature,
                                                top_p=top_p)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        print(st.session_state.messages)
        st.chat_message("assistant").write(msg)

    elif selected_model == 'Llama2-13B':
    #LLAmA API
      with st.spinner("LLaMa2-13B is Thinking..."):
        string_dialogue = ""
        for dict_message in st.session_state.messages:
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
        print(string_dialogue)
        response = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt} Assistant: ",
                                  "temperature":temperature, 
                                  "top_p":top_p, 
                                  "max_length":max_length,
                                  "system_prompt": "You are to respond and act as a mental health chatbot. You respond as Assistant. You are to act compassionate, supportive, and non-judgmental mental health chatbot designed to provide emotional support, mental wellness resources, and crisis intervention. Please provide a relevant, concise and complete answer, in maximum 3 sentences.", 
                                  "repetition_penalty":1,
                                  "presence_penalty": 1})


        full_response = ''
        for item in response:
            full_response += item
        print(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.chat_message("assistant").write(full_response)
