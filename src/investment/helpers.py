import string
import random


def generate_code(length=10):
    # Definindo os caracteres permitidos: letras maiúsculas, minúsculas e dígitos
    characters = string.ascii_letters + string.digits
    # Gerando o código
    unique_code = ''.join(random.choices(characters, k=length))
    return unique_code
