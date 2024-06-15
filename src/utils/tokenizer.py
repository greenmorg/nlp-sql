import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

def encode(text: str) -> list[int]:
    return encoding.encode(text=text)

def decode(tokens: list[int]) -> str:
    return encoding.decode(tokens=tokens)

def per_byte_decoding(tokens: list[int]) -> list[str]:
    return encoding.decode_tokens_bytes(tokens=tokens) 