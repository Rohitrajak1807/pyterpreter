from typing import Union

INTEGER = 'INTEGER'
EOF = 'EOF'
PLUS = 'PLUS'
MINUS = 'MINUS'
DIVIDE = 'DIVIDE'
MULTIPLY = 'MULTIPLY'


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
    current_char: Union[str | None]

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    # 2. Add a method that skips whitespace characters so that your calculator can handle inputs with whitespace
    # characters like ” 12 + 3”
    def skip_wspace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def err(self):
        raise Exception('error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self) -> int:
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
                token = Token(PLUS, self.current_char)
                self.advance()
                return token
            if self.current_char == '-':
                token = Token(MINUS, self.current_char)
                self.advance()
                return token
            if self.current_char == '*':
                token = Token(MULTIPLY, self.current_char)
                self.advance()
                return token
            if self.current_char == '/':
                token = Token(DIVIDE, self.current_char)
                self.advance()
                return token
            self.err()
        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.typ == token_type:
            self.current_token = self.next_token()
        else:
            self.err()

    def term(self) -> int:
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.current_token = self.next_token()
        result = self.term()
        while self.current_token.typ in (PLUS, MINUS, MULTIPLY, DIVIDE):
            token = self.current_token
            if token.typ == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            if token.typ == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            if token.typ == MULTIPLY:
                self.eat(MULTIPLY)
                result = result * self.term()
            if token.typ == DIVIDE:
                self.eat(DIVIDE)
                result = result / self.term()
        return result


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
