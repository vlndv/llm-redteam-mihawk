from model import ask_model

reply = ask_model("llama3.1:8b", "You are a helpful assistant.", "Say hello in one sentence.")
print(reply)