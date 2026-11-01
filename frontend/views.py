import flet as ft

def get_merge_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Módulo: Mesclar PDFs", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
            ft.Text("Selecione e ordene os arquivos que deseja unificar.", color=ft.colors.GREY_400)
        ]),
        padding=20
    )

def get_split_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Módulo: Dividir PDF", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
            ft.Text("Extraia intervalos de páginas ou desmembre o documento.", color=ft.colors.GREY_400)
        ]),
        padding=20
    )

def get_compress_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Módulo: Compactar PDF", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
            ft.Text("Otimize o tamanho dos seus arquivos de forma segura.", color=ft.colors.GREY_400)
        ]),
        padding=20
    )

def get_rotate_view():
    return ft.Container(
        content=ft.Column([
            ft.Text("Módulo: Rotacionar Páginas", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
            ft.Text("Ajuste a orientação geométrica do seu documento.", color=ft.colors.GREY_400)
        ]),
        padding=20
    )
