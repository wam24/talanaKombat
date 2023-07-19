from prompt_toolkit import prompt


def menu(intro=True):
    # Use a breakpoint in the code line below to debug your script.
    from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog
    from battle import Game
    if intro:
        message_dialog(
            title='Juego interactivo',
            text='Bienvenido a Talana Kombat.',
            ok_text='Continuar').run()
    options = [
        ("start", "Iniciar juego"),
        ("instructions", "Instrucciones"),
        ("control", "Controles"),
        ("exit", "Salir")
        ]
    result = radiolist_dialog(
        title="Menú",
        text="Seleccione una opción presionando Enter y luego presiones TAB y Enter",
        values=options
        ).run()
    if result == "start":
        Game().battle()
    elif result == "instructions":
        message_dialog(
            title='Introducción',
            text='Talana Kombat es un juego de pelea de 2 jugadores. La pelea dura las rondas que indiquen antes de '
                 'empezar, debe ser mayor a 3 o hasta que un jugador haya '
                 'derrotado al contrincante.\nCada jugador debera ingresar todos los movimientos que usara en cada turno.\n'
                 'Empezará el jugador número 1 y luego el jugador número 2.\nEl jugador se encuentra del lado derecho y el '
                 'jugador 2 se encuentra del lado izquierdo',
            ok_text='Continuar').run()
        menu(False)
    elif result == "control":
        message_dialog(
            title='Controles',
            text='Los botones son los siguientes: (W)Arriba, (S)Abajo, (A)Izquierda, (D)Derecha, (P)Puño, (K)Patada.'
                 '\nLa cantidad maxima de movimientos es 5.\nPrimero indicamos el movimiento y luego el ataque.',
            ok_text='Continuar').run()
        menu(False)
    elif result == "exit":
        exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menu()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
