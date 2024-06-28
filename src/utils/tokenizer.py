import tiktoken

EMBEDDING_SHAPE = 1536

encoding = tiktoken.get_encoding("cl100k_base")

def encode(text: str) -> list[int]:
    return encoding.encode(text=text)

def decode(tokens: list[int]) -> str:
    return encoding.decode(tokens=tokens)

def per_byte_decoding(tokens: list[int]) -> list[str]:
    return encoding.decode_tokens_bytes(tokens=tokens) 

def broadcast(tokens: list[int], shape: int) -> list[int]:
    if shape < len(tokens): 
        raise ArithmeticError(f"Could not broadcast array to smaller dimensions. ")
    remain = shape - len(tokens)
    tokens += [encoding.eot_token] * remain # fills the missing values with <|endoftext|> token
    return tokens

def text_to_embedding(text: str) -> list[int]:
    tokens = encode(text)
    tokens = broadcast(tokens, EMBEDDING_SHAPE)
    return tokens

def embedding_to_text(tokens: list[int]) -> str:
    no_eot_tokens = list(filter(lambda t: t != encoding.eot_token, tokens))
    return decode(no_eot_tokens)