# import os
# from typing import List, Dict

# from dotenv import load_dotenv
# import cohere
# from cohere import errors as cohere_errors
# import typer
# from rich import print
# from rich.table import Table

# #def principal(): pass

# def get_client() -> cohere.ClientV2:
#     load_dotenv()
#     api_key = os.getenv('COHERE_API_KEY')

#     if not api_key:
#         raise ValueError('No se encontró la API_KEY o no existe en tu archivo de enterno')
#     if hasattr(cohere,'ClientV2'):
#         return cohere.ClientV2(api_key=api_key)

# get_client()

# def generador_tabla() -> None:
#     print('[bold green]Cohere Chat CLI[/bold green]\n')
#     tabla = Table('Comando','Descripción')
#     tabla.add_row('exit','Salir de la aplicación')
#     tabla.add_row('new','Crear una nueva conversación')
#     print(tabla)

# def prompt_input() -> str:
#     texto = typer.prompt('¿Sobre qué quieres hablar?')
#     if texto.strip().lower() == 'exit':
#         if typer.confirm('¿Seguro que deseas salir?'):
#             print('Hasta luego.')
#             raise typer.Abort()
#         return prompt_input()
#     return texto

# prompt_input()

# def main(model:str = 'command-a03-2025'):
#     # 1. Establecer conexión con la API
#     cliente = get_client()
#     # 2. Llamar a la tabla de instrucciones
#     generador_tabla()
#     # 3. Definir roles:
#     sistema_mensajes = {
#         'role':'system',
#         'content':'Eres un asistente virtual'
#     }

#     mensajes: list[Dict[str,str]] = [sistema_mensajes]

#     while True:
#         mensaje_usuario = prompt_input().strip()

#         if mensaje_usuario.lower() == 'new':
#             print('Nueva conversación iniciada:')
#             mensajes = [sistema_mensajes]
#             continue
#         mensajes.append({
#                     'role':'user',
#                     'content':mensaje_usuario
#         })

#         try:
#             # Llamada a la API
#             resp = cliente.chat(
#                 model = model,
#                 messages = mensajes,
#                 temperature= 0.7,
#             )

#             texto_asistente = (
#                 getattr(resp, 'messages', None).content
#                 if hasattr(resp, 'messages') else None
#             )
#             if not texto_asistente:
#                 texto_asistente = getattr(resp, 'text', '')
#                 mensajes.append({
#                     'role':'user',
#                     'content':mensaje_usuario
#                     })
#                 print('[bold green]Cohere Chat CLI[/bold green]\n')

#         #Manejo de errores: casos comunes y mensaje guía
#         except cohere_errors.NotFoundError as e:
#             print("[red]Modelo no encontrado o retirado.[/red] "
#                 "Prueba con 'command-a-03-2025' o 'command-a'.")
#         except cohere_errors.CohereError as e:
#             print(f"[red]Error de Cohere:[/red] {e}")
#         except Exception as e:
#             print(f"[red]Error inesperado:[/red] {e}")


# if __name__ == "__main__":
#     typer.run(main)
        

# Paso 1. Importaciones y tipado
# - os: leer variables de entorno
# - typing: tipos para claridad (List, Dict)
# - dotenv: cargar .env con la API key
# - cohere: SDK del proveedor
# - typer: crear CLI interactivo
# - rich: mejorar la salida en consola (colores/tablas)
import os
from typing import List, Dict

from dotenv import load_dotenv
import cohere
from cohere import errors as cohere_errors
import typer
from rich import print
from rich.table import Table


# Paso 2. Crear el cliente autenticado de Cohere
# - Cargar .env
# - Leer COHERE_API_KEY
# - Validar que exista
# - Devolver instancia del cliente (SDK v2)
def get_client() -> "cohere.ClientV2":
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("No se encontró COHERE_API_KEY en el .env")
    return cohere.ClientV2(api_key)


# Paso 3. Pintar cabecera del programa (UI del CLI)
# - Mostrar título
# - Mostrar tabla de comandos disponibles (new, exit)
def render_header() -> None:
    print("[bold green]Cohere Chat CLI[/bold green]\n")
    t = Table("Comando", "Descripción")
    t.add_row("exit", "Salir de la aplicación")
    t.add_row("new", "Crear una nueva conversación")
    print(t)


# Paso 4. Función de entrada de usuario con control de salida
# - Pregunta "¿Sobre qué quieres hablar?"
# - Si escribe "exit", confirmar y abortar la app con Typer
# - Devuelve el texto a procesar
def prompt_input() -> str:
    txt = typer.prompt("\n¿Sobre qué quieres hablar?")
    if txt.strip().lower() == "exit":
        if typer.confirm("¿Seguro que quieres salir?"):
            print("Hasta luego")
            raise typer.Abort()
        # Si no confirma, volvemos a preguntar
        return prompt_input()
    return txt


# Paso 5. Función principal del chat
# - Recibe el modelo (por defecto uno vigente)
# - Crea cliente y cabecera
# - Define el mensaje de sistema (tono/rol del asistente)
# - Mantiene el historial de mensajes con roles
# - Bucle:
#     1) Leer input
#     2) Si "new": reiniciar historial
#     3) Añadir mensaje del usuario
#     4) Llamar a la API (client.chat)
#     5) Extraer texto de la respuesta
#     6) Añadir respuesta al historial
#     7) Imprimir
# - Manejo de errores orientativo
def main(model: str = "command-a-03-2025"):  # modelo vigente
    # 5.1 Cliente y cabecera
    client = get_client()
    render_header()

    # 5.2 Mensaje de sistema: guía el estilo del asistente
    system_msg = {
        "role": "system",
        "content": "Eres un asistente útil que responde en español, claro y directo."
    }
    # 5.3 Historial: arranca con el system
    messages: List[Dict[str, str]] = [system_msg]

    # 5.4 Bucle de conversación
    while True:
        # 5.4.1 Pedimos mensaje al usuario
        user_msg = prompt_input().strip()

        # 5.4.2 Comando "new": reiniciar conversación
        if user_msg.lower() == "new":
            print("[yellow]Nueva conversación creada[/yellow]")
            messages = [system_msg]
            continue

        # 5.4.3 Agregar el turno del usuario al historial
        messages.append({"role": "user", "content": user_msg})

        try:
            # 5.4.4 Llamada a la API de Cohere
            # - Se envía todo el historial en `messages`
            # - temperature controla creatividad
            resp = client.chat(
                model=model,
                messages=messages,
                temperature=0.7,
            )

            # 5.4.5 Extraer el texto de la respuesta
            # El SDK v2 puede devolver .message.content o .text
            assistant_text = (
                getattr(resp, "message", None).content
                if hasattr(resp, "message") else None
            )
            if not assistant_text:
                assistant_text = getattr(resp, "text", "")

            # 5.4.6 Agregar la respuesta del asistente al historial
            messages.append({"role": "assistant", "content": assistant_text})

            # 5.4.7 Mostrar respuesta al usuario
            print(f"[bold green]>[/bold green] {assistant_text}")

        # 5.5 Manejo de errores: casos comunes y mensaje guía
        except cohere_errors.NotFoundError as e:
            print("[red]Modelo no encontrado o retirado.[/red] "
                  "Prueba con 'command-a-03-2025' o 'command-a'.")
        except cohere_errors.CohereError as e:
            print(f"[red]Error de Cohere:[/red] {e}")
        except Exception as e:
            print(f"[red]Error inesperado:[/red] {e}")


# Paso 6. Punto de entrada del CLI
# - Typer ejecuta main() y habilita parseo de argumentos si se añaden
if __name__ == "__main__":           
    typer.run(main)
    

