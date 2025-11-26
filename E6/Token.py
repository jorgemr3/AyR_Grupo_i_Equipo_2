from dataclasses import dataclass
from typing import Any
from Dicc import Dicc

@dataclass

class Token:

    type: Dicc
    value: Any
    linea: int
    column: int = 1
    pos: int = 0

    def __str__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, linea={self.linea}, columna={self.columna})"

    def __eq__(self, other) -> bool:
        if not isinstance(other,Token):
            return False
        return self.type == other.type and self.value == other.value

    def is_type(self, token_type: Dicc) -> bool:
        return self.type == token_type

    def has_value(self, expected_value: Any) -> bool:
        return self.value == expected_value

    def matches(self, token_type: Dicc, value: Any = None) -> bool:
        return self.is_type(token_type) and self.has_value(value)

    def is_command(self) -> bool:
        return self.is_type(Dicc.ACCION)

    def is_numeric(self) -> bool:
        return self.is_type(Dicc.NUMERO)

    def is_porcent(self) -> bool:
        return self.is_type(Dicc.PORCENTAJE)

    def is_place(self) -> bool:
        return self.is_type(Dicc.LUGAR)

    def is_object(self) -> bool:
        return self.is_type(Dicc.OBJETO)