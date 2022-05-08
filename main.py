# coding: utf8
from lexical_analysis_generator import Compiler, read_file
TEST_FILE = 3

def get_main_input(motive):
    return input(f"Introduzca el nombre del archivo para {motive} o 'salir' para salir\n>>")


def main():
    compiler = Compiler()
    valid_file = False
    while True:
        # file = get_main_input('generar el analizador léxico')
        file = f'ArchivoPrueba{TEST_FILE}.atg'
        if file == 'salir':
            break
        try:
            read_file(file, compiler)
            valid_file = True
        except FileNotFoundError:
            print("Archivo no encontrado, recuerde incluir la extensión\n")
            valid_file = False

        if valid_file:
            print(f"Se ha generado el archivo {compiler.name}.py con su analizador léxico!")
            # file = get_main_input('obtener los tokens')
            file = f'ArchivoPrueba{TEST_FILE}Entrada.txt'
            if file == 'salir':
                break
            try:
                print(f"GENERANDO TOKENS DEL ARCHIVO {file}\n")
                compiler.get_lexer_tokens(file)
                print("FINAL DE LA GENERACIÓN DE TOKENS\n")
                valid_file = False
            except FileNotFoundError:
                print("Archivo no encontrado, recuerde incluir la extensión\n")
        break
    print("Gracias por haber utilizado el generador de analizadores léxicos, que tenga un feliz día :)")


if __name__ == '__main__':
    main()
