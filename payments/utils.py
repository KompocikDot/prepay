import secrets

def gen_external_id() -> str:
    return secrets.token_hex(3)

