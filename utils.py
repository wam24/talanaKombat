from prompt_toolkit.shortcuts.dialogs import _create_app, _return_none

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import Completer
from prompt_toolkit.filters import FilterOrBool
from prompt_toolkit.formatted_text import AnyFormattedText

from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Label,

    TextArea,
    ValidationToolbar,
    )


class MovementValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if len(text) > 5:
            raise ValidationError(message='El texto debe tener como máximo 5 caracteres.',
                                  cursor_position=len(document.text))
        elif not all(letter in {'w', 's', 'a', 'd', 'W', 'S', 'A', 'D'} for letter in text):
            raise ValidationError(message='El texto solo puede contener las letras "w", "s", "a" o "d".',
                                  cursor_position=len(document.text))


class HitValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if len(text) > 1:
            raise ValidationError(message='El texto debe tener como máximo 1 caracteres.',
                                  cursor_position=len(document.text))
        elif not all(letter in {'k', 'p', 'K', 'P'} for letter in text):
            raise ValidationError(message='El texto solo puede contener las letras "k" o "p".',
                                  cursor_position=len(document.text))


class JsonValidator(Validator):
    def validate(self, document):
        import json
        text = document.text.strip()
        json_data = json.loads(text)
        if "player1" not in json_data or "player2" not in json_data:
            raise ValidationError(message='El JSON no contiene las claves obligatorias player1 y player2.',
                                  cursor_position=len(document.text))
        # Verificar si las claves "movimientos" y "golpes" están presentes dentro de cada "player"
        for player_key in ["player1", "player2"]:
            player_data = json_data.get(player_key, {})
            if "movimientos" not in player_data or "golpes" not in player_data:
                raise ValidationError(
                    message=f"El player '{player_key}' no contiene las claves 'movimientos' y 'golpes'.",
                    cursor_position=len(document.text))


class RoundValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        print(f'NUmero de rondas {text}')

        if not all(letter in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'} for letter in text):
            raise ValidationError(message='El texto solo puede contener números positivos',
                                  cursor_position=len(document.text))
        if len(text) < 1:
            raise ValidationError(message='Debe indicar un número',
                                  cursor_position=len(document.text))

        if int(text) == 1 or int(text) < 1:
            raise ValidationError(message='Debe indicar un número mayor a 1',
                                  cursor_position=len(document.text))


def input_dialog_multiple_line(
        title: AnyFormattedText = "",
        text: AnyFormattedText = "",
        ok_text: str = "OK",
        cancel_text: str = "Cancel",
        completer: Completer | None = None,
        validator: Validator | None = None,
        password: FilterOrBool = False,
        style: BaseStyle | None = None,
        default: str = "",
        ) -> Application[str]:
    """
    Realice una modificacion al codigo original para poder ser multilinea por defecto
    """

    def accept(buf: Buffer) -> bool:
        get_app().layout.focus(ok_button)
        return True  # Keep text.

    def ok_handler() -> None:
        get_app().exit(result=textfield.text)

    ok_button = Button(text=ok_text, handler=ok_handler)
    cancel_button = Button(text=cancel_text, handler=_return_none)

    textfield = TextArea(
        text=default,
        multiline=True,
        password=password,
        completer=completer,
        validator=validator,
        accept_handler=accept,
        )

    dialog = Dialog(
        title=title,
        body=HSplit(
            [
                Label(text=text, dont_extend_height=True),
                textfield,
                ValidationToolbar(),
                ],
            padding=1,
            ),
        buttons=[ok_button, cancel_button],
        with_background=True,
        )

    return _create_app(dialog, style)
