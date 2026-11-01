import flet as ft

def main(page: ft.Page):
    # Configurações de layout e design da janela principal (UX/UI Studio)
    page.title = "PDF Toolbox - Modern & Secure"
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = True
    
    # Aplicação de identidade visual: Tema Escuro Profissional (Material Design 3)
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE_GREY)
    
    # Alinhamento do conteúdo na tela
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Componente visual temporário de boas-vindas
    welcome_text = ft.Text(
        value="Bem-vindo ao PDF Toolbox 🚀", 
        size=32, 
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_200
    )
    
    subtitle_text = ft.Text(
        value="A engine do backend está integrada. Pronto para construir os módulos visuais.",
        size=16,
        color=ft.colors.GREY_400
    )

    # Adiciona os elementos à tela do usuário
    page.add(
        ft.Column(
            controls=[welcome_text, subtitle_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    # Inicializa a aplicação como uma janela desktop nativa elegante
    ft.app(target=main)
