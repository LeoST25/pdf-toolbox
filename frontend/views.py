import flet as ft
from backend.merger import PDFMerger

def get_merge_view(page: ft.Page):
    # Instancia a nossa engine do backend
    merger_engine = PDFMerger()
    
    # Estado local para armazenar a lista de arquivos selecionados
    selected_files_paths = []
    
    # Elementos Visuais (UI Components)
    files_list_view = ft.ListView(expand=True, spacing=10, padding=10)
    
    # Texto informativo de status interno
    status_text = ft.Text("Nenhum arquivo selecionado.", color=ft.colors.GREY_500, italic=True)

    def update_ui_list():
        """Atualiza a lista visual na tela com base no estado dos arquivos salvos."""
        files_list_view.controls.clear()
        if not selected_files_paths:
            status_text.value = "Nenhum arquivo selecionado."
            merge_button.disabled = True
            clear_button.disabled = True
        else:
            status_text.value = f"{len(selected_files_paths)} arquivo(s) preparado(s) para mesclagem."
            merge_button.disabled = False
            clear_button.disabled = False
            
            for index, path in enumerate(selected_files_paths):
                files_list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.PICTURE_AS_PDF, color=ft.colors.RED_ACCENT),
                            ft.Text(path, expand=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ]),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        padding=10,
                        border_radius=8
                    )
                )
        page.update()

    # Função disparada após o usuário escolher os arquivos de entrada
    def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                if file.path not in selected_files_paths:
                    selected_files_paths.append(file.path)
            update_ui_list()

    # Função disparada após o usuário escolher onde deseja salvar o arquivo final
    def on_save_location_chosen(e: ft.FilePickerResultEvent):
        if e.path:
            output_path = e.path
            # Garante que o arquivo termine com a extensão correta
            if not output_path.lower().endswith('.pdf'):
                output_path += ".pdf"
                
            # Exibe indicador de carregamento
            status_text.value = "Processando mesclagem segura..."
            page.update()
            
            # Invoca a inteligência do nosso Backend
            result = merger_engine.merge(selected_files_paths, output_path)
            
            # Exibe feedback visual ao usuário via SnackBar (Padrão de UX da empresa)
            if result["status"] == "success":
                page.snack_bar = ft.SnackBar(ft.Text(result["message"]), bgcolor=ft.colors.GREEN_700)
                selected_files_paths.clear()
                update_ui_list()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(result["message"]), bgcolor=ft.colors.RED_700)
                update_ui_list()
                
            page.snack_bar.open = True
            page.update()

    # Registra os manipuladores de arquivos (FilePickers) na página
    file_picker = ft.FilePicker(on_result=on_files_selected)
    save_picker = ft.FilePicker(on_result=on_save_location_chosen)
    page.overlay.extend([file_picker, save_picker])

    def clear_list(e):
        selected_files_paths.clear()
        update_ui_list()

    # Botões de Controle e Ações
    add_button = ft.ElevatedButton(
        text="Adicionar PDFs",
        icon=ft.icons.ADD,
        on_click=lambda _: file_picker.pick_files(allow_multiple=True, allowed_extensions=["pdf"]),
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_700)
    )
    
    clear_button = ft.IconButton(
        icon=ft.icons.DELETE_FOREVER,
        icon_color=ft.colors.RED_400,
        tooltip="Limpar Lista",
        disabled=True,
        on_click=clear_list
    )

    merge_button = ft.FilledButton(
        text="Mesclar Documentos",
        icon=ft.icons.PLAY_ARROW,
        disabled=True,
        on_click=lambda _: save_picker.save_file(file_name="pdf_mesclado.pdf", allowed_extensions=["pdf"])
    )

    # Layout estruturado da tela de Merge (UI Design Clean)
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Módulo: Mesclar PDFs", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
                    ft.Text("Selecione e unifique múltiplos arquivos em um único documento.", color=ft.colors.GREY_400),
                ], expand=True),
                ft.Row([add_button, clear_button])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            status_text,
            
            # Área de exibição dos arquivos adicionados
            ft.Container(
                content=files_list_view,
                border=ft.border.all(1, ft.colors.GREY_800),
                border_radius=10,
                expand=True,
                bgcolor=ft.colors.BLACK12
            ),
            
            ft.Row([merge_button], alignment=ft.MainAxisAlignment.END)
        ]),
        padding=20,
        expand=True
    )

# Mantemos os esqueletos temporários abaixo para as outras abas não quebrarem
def get_split_view():
    return ft.Container(content=ft.Column([ft.Text("Módulo: Dividir PDF", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400)]), padding=20)

def get_compress_view():
    return ft.Container(content=ft.Column([ft.Text("Módulo: Compactar PDF", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400)]), padding=20)

def get_rotate_view():
    return ft.Container(content=ft.Column([ft.Text("Módulo: Rotacionar Páginas", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400)]), padding=20)
