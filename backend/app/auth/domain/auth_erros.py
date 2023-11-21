"""
Este módulo define exceções personalizadas para lidar com erros relacionados a
tokens em um sistema de autenticação ou autorização.

Classes:
    ExpiredToken: Uma exceção para indicar que um token usado na autenticação
                    ou autorização expirou.
    InvalidToken: Uma exceção para indicar que um token usado na autenticação
                    ou autorização é inválido.
    SecretKeyNotSet: Uma exceção para indicar que a chave secreta necessária
                     para a operação de token não foi configurada.

Estas exceções são úteis para fornecer mensagens de erro mais claras e
específicas quando ocorrem problemas com a manipulação de tokens em aplicações
que utilizam sistemas de segurança baseados em tokens.

Exemplos:
    Levantar uma exceção quando um token expira:
        raise ExpiredToken

    Levantar uma exceção quando um token é inválido:
        raise InvalidToken

    Levantar uma exceção quando a chave secreta não está definida:
        raise SecretKeyNotSet
"""


class ExpiredToken(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "Expired Token error"


class InvalidToken(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "Invalid Token error"


class SecretKeyNotSet(Exception):
    """Raised for database-related errors in consolidated portfolios."""

    def __str__(self):
        return "SECRET_KEY env variable not set"
