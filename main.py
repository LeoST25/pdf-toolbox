import flet as ft
from frontend.views import get_merge_view, get_split_view, get_compress_view, get_rotate_view

def main(page: ft.Page):
    page.title = "PDF Toolbox - Modern & Secure"
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE_GREY)
    
    # Dicionário de rotas injetando a dependência da 'page' onde necessário
    views = {
        0: lambda: get_merge_view(page),
        1: get_split_view,
        2: get_compress_view,
        3: get_rotate_view
    }

    content_area = ft.Container(
        content=views[0](), 
        expand=True
    )

    def on_navigation_change(e):
        selected_index = e.control.selected_index
        content_area.content = views[selected_index]()
        page.update()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.CALL_MERGE, label="Mesclar"),
            ft.NavigationRailDestination(icon=ft.icons.CALL_SPLIT, label="Dividir"),
            ft.NavigationRailDestination(icon=ft.icons.COMPRESS, label="Compactar"),
            ft.NavigationRailDestination(icon=ft.icons.ROTATE_RIGHT, label="Rotacionar"),
        ],
        on_change=on_navigation_change,
        bgcolor=ft.colors.SURFACE_VARIANT
    )

    page.add(
        ft.Row(
            controls=[
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
