import tiktoken

# print(f"dir(tiktoken): {dir(tiktoken)}")

encoding = tiktoken.encoding_for_model("gpt-4.1-mini")

# print(f"dir(encoding): {dir(encoding)}")

tokens = encoding.encode("Hi! My name is Ed and I like Banoffee pie")

# print(f"dir(tokens): {dir(tokens)}")

print(f"Tokens: {tokens}")

for token_id in tokens:
    token = encoding.decode([token_id])
    print(f"{token_id} -> {token}")

# print(f"{100000} -> {encoding.decode([100000])}")
