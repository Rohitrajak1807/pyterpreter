from typing import Union

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


class Token:
    typ: str
    value: Union[int | None | str]

    def __init__(self, typ, value):
        self.typ = typ
        self.value = value

    def __repr__(self):
        return f'Token({self.typ}, {self.value})'

    def __str__(self):
        return self.__repr__()


class Interpreter:
    text: str
    pos: int
    current_token: Union[Token | None]

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def err(self):
        raise Exception('error parsing input')

    def next_token(self):
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)
        current_char = self.text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        self.err()

    def eat(self, token_type):
        if self.current_token.typ == token_type:
            self.current_token = self.next_token()
        else:
            self.err()

    def expr(self):
        self.current_token = self.next_token()
        left = self.current_token
        self.eat(INTEGER)
        op = self.current_token
        _ = op
        self.eat(PLUS)
        right = self.current_token
        self.eat(INTEGER)
        res = left.value + right.value
        return res


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        except KeyboardInterrupt:
            print('\nexiting...')
            exit(1)
        if not text:
            continue
        interpreter = Interpreter(text)
        res = interpreter.expr()
        print(res)


if __name__ == '__main__':
    main()
