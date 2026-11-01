import flet as ft
# Importando as visões do nosso pacote frontend
from frontend.views import get_merge_view, get_split_view, get_compress_view, get_rotate_view

def main(page: ft.Page):
    page.title = "PDF Toolbox - Modern & Secure"
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE_GREY)
    
    # Dicionário mapeando o índice do menu para a respectiva função de visualização
    views = {
        0: get_merge_view,
        1: get_split_view,
        2: get_compress_view,
        3: get_rotate_view
    }

    # Container principal à direita que receberá o conteúdo de cada tela dinamicamente
    content_area = ft.Container(
        content=views[0](), # Inicializa exibindo a tela de Mesclagem (índice 0)
        expand=True
    )

    # Evento disparado quando o usuário clica em um botão do menu lateral
    def on_navigation_change(e):
        selected_index = e.control.selected_index
        # Atualiza o conteúdo do container dinâmico com a view correspondente
        content_area.content = views[selected_index]()
        page.update()

    # Barra de Navegação Lateral Esquerda (UI Design Pattern Moderno)
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        # Definição dos destinos (Ícones + Textos)
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.CALL_MERGE, 
                selected_icon=ft.icons.CALL_MERGE, 
                label="Mesclar"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CALL_SPLIT, 
                selected_icon=ft.icons.CALL_SPLIT, 
                label="Dividir"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.COMPRESS, 
                selected_icon=ft.icons.COMPRESS, 
                label="Compactar"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOOKS_ONE, 
                selected_icon=ft.icons.ROTATE_RIGHT, 
                label="Rotacionar"
            ),
        ],
        on_change=on_navigation_change,
        bgcolor=ft.colors.SURFACE_VARIANT
    )

    # Adiciona a estrutura layout lado a lado (Menu à esquerda, Conteúdo à direita)
    page.add(
        ft.Row(
            controls=[
                nav_rail,
                ft.VerticalDivider(width=1), # Linha sutil separadora de ambiente
                content_area
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
