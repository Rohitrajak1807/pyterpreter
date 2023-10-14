from typing import Union

INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = 'PLUS'


class Token:
    typ: Union[str | None]
    value: Union[str | int | None]

    def __init__(self, typ, val):
        self.typ = typ
        self.value = val


class Interpreter:
    text: str
    pos: int
    current_token: Union[Token | None]
    current_char: Union[str | None]

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def err(self):
        raise Exception("error parsing input")

    def skip_wspace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        digits: str = ''
        while self.current_char is not None and self.current_char.isdigit():
            digits += self.current_char
            self.advance()
        return int(digits)

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_wspace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                tok = Token(PLUS, self.current_char)
                self.advance()
                return tok
            self.err()
        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.typ == token_type:
            self.current_token = self.next_token()
        else:
            self.err()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.current_token = self.next_token()
        result = self.term()
        while self.current_token.typ in PLUS:
            token = self.current_token
            if token.typ == PLUS:
                self.eat(PLUS)
                result = result + self.term()
        return result


def main():
    while True:
        try:
            text = input('calc>')
            if not text:
                continue
            interp = Interpreter(text)
            res = interp.expr()
            print(res)
        except EOFError as e:
            print(e)
            break
        except KeyboardInterrupt:
            print('\nexiting...')


if __name__ == '__main__':
    main()
