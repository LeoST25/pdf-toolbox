import flet as ft
import os
from backend.merger import PDFMerger
from backend.splitter import PDFSplitter
from backend.compressor import PDFCompressor
from backend.rotator import PDFRotator

# --- FUNÇÃO UTILITÁRIA DE CONVERSÃO SEGURA (Blindagem de Tipos) ---
def safe_int(value: str | None, default: int = 1) -> int:
    """Converte com segurança uma string opcional para inteiro, evitando erros de tipo."""
    if not value or not value.strip().isdigit():
        return default
    return int(value)


# --- TELA DE MESCLAGEM ---
def get_merge_view(page: ft.Page):
    merger_engine = PDFMerger()
    selected_files_paths = []
    files_list_view = ft.ListView(expand=True, spacing=10, padding=10)
    status_text = ft.Text("Nenhum arquivo selecionado.", color=ft.colors.GREY_500, italic=True)

    def update_ui_list():
        files_list_view.controls.clear()
        if not selected_files_paths:
            status_text.value = "Nenhum arquivo selecionado."
            merge_button.disabled = True
            clear_button.disabled = True
        else:
            status_text.value = f"{len(selected_files_paths)} arquivo(s) preparado(s) para mesclagem."
            merge_button.disabled = False
            clear_button.disabled = False
            for path in selected_files_paths:
                files_list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.PICTURE_AS_PDF, color=ft.colors.RED_ACCENT),
                            ft.Text(path, expand=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ]),
                        bgcolor=ft.colors.SURFACE_VARIANT, padding=10, border_radius=8
                    )
                )
        page.update()

    def on_files_selected(e: ft.FilePickerResultEvent):
        if e.files:
            for file in e.files:
                if file.path not in selected_files_paths:
                    selected_files_paths.append(file.path)
            update_ui_list()

    def on_save_location_chosen(e: ft.FilePickerResultEvent):
        if e.path:
            output_path = e.path if e.path.lower().endswith('.pdf') else e.path + ".pdf"
            status_text.value = "Processando mesclagem segura..."
            page.update()
            result = merger_engine.merge(selected_files_paths, output_path)
            if result["status"] == "success":
                page.snack_bar = ft.SnackBar(ft.Text(result["message"]), bgcolor=ft.colors.GREEN_700)
                selected_files_paths.clear()
            else:
                page.snack_bar = ft.SnackBar(ft.Text(result["message"]), bgcolor=ft.colors.RED_700)
            update_ui_list()
            page.snack_bar.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=on_files_selected)
    save_picker = ft.FilePicker(on_result=on_save_location_chosen)
    page.overlay.extend([file_picker, save_picker])

    add_button = ft.ElevatedButton(
        text="Adicionar PDFs", icon=ft.icons.ADD,
        on_click=lambda _: file_picker.pick_files(allow_multiple=True, allowed_extensions=["pdf"]),
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_700)
    )
    clear_button = ft.IconButton(icon=ft.icons.DELETE_FOREVER, icon_color=ft.colors.RED_400, disabled=True, on_click=lambda _: (selected_files_paths.clear(), update_ui_list()))
    merge_button = ft.FilledButton(text="Mesclar Documentos", icon=ft.icons.PLAY_ARROW, disabled=True, on_click=lambda _: save_picker.save_file(file_name="pdf_mesclado.pdf", allowed_extensions=["pdf"]))

    return ft.Container(
        content=ft.Column([
            ft.Row([ft.Column([ft.Text("Módulo: Mesclar PDFs", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_ACCENT_400), ft.Text("Selecione e unifique múltiplos arquivos.", color=ft.colors.GREY_400)], expand=True), ft.Row([add_button, clear_button])]),
            ft.Divider(height=10, color=ft.colors.TRANSPARENT), status_text,
            ft.Container(content=files_list_view, border=ft.border.all(1, ft.colors.GREY_800), border_radius=10, expand=True, bgcolor=ft.colors.BLACK12),
            ft.Row([merge_button], alignment=ft.MainAxisAlignment.END)
        ]), padding=20, expand=True
    )


# --- TELA DE DIVISÃO ---
def get_split_view(page: ft.Page):
    splitter_engine = PDFSplitter()
    state: dict[str, str | None] = {"input_path": None}

    txt_file = ft.Text("Nenhum arquivo selecionado", italic=True, color=ft.colors.GREY_500)
    radio_mode = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="range", label="Dividir por Intervalo de Páginas"),
        ft.Radio(value="all", label="Separar todas as páginas em arquivos individuais")
    ]))
    radio_mode.value = "range"

    input_start = ft.TextField(label="Página Inicial", value="1", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    input_end = ft.TextField(label="Página Final", value="2", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    row_inputs = ft.Row([input_start, input_end], visible=True)

    def mode_changed(e):
        row_inputs.visible = (radio_mode.value == "range")
        page.update()
    radio_mode.on_change = mode_changed

    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            first_file = e.files[0]
            if first_file.path:
                # CORRIGIDO: Extração forçada e explícita para string pura, eliminando o tipo Union do Linter
                file_path: str = str(first_file.path)
                state["input_path"] = file_path
                txt_file.value = f"Selecionado: {os.path.basename(file_path)}"
                btn_action.disabled = False
                page.update()



    def on_action_clicked(e):
        current_path = state["input_path"]
        if not current_path: return
        
        if radio_mode.value == "range":
            def on_save_chosen(se: ft.FilePickerResultEvent):
                if se.path:
                    start = safe_int(input_start.value, default=1)
                    end = safe_int(input_end.value, default=2)
                    res = splitter_engine.split_by_range(current_path, se.path, start, end)
                    color = ft.colors.GREEN_700 if res["status"] == "success" else ft.colors.RED_700
                    page.snack_bar = ft.SnackBar(ft.Text(res["message"]), bgcolor=color)
                    page.snack_bar.open = True
                    page.update()
            sp = ft.FilePicker(on_result=on_save_chosen)
            page.overlay.append(sp)
            page.update()
            sp.save_file(file_name="pdf_dividido.pdf", allowed_extensions=["pdf"])
        else:
            def on_dir_chosen(de: ft.FilePickerResultEvent):
                if de.path:
                    res = splitter_engine.split_all_pages(current_path, de.path)
                    color = ft.colors.GREEN_700 if res["status"] == "success" else ft.colors.RED_700
                    
                    # CORRIGIDO: Forçando conversão explícita para string pura str()
                    message_text = str(res.get("message", "Processamento concluído"))
                    
                    page.snack_bar = ft.SnackBar(ft.Text(message_text), bgcolor=color)
                    page.snack_bar.open = True
                    page.update()
            dp = ft.FilePicker(on_result=on_dir_chosen)
            page.overlay.append(dp)
            page.update()
            dp.get_directory_path()

    fp = ft.FilePicker(on_result=on_file_selected)
    page.overlay.append(fp)
    
    btn_select = ft.ElevatedButton("Selecionar PDF", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: fp.pick_files(allowed_extensions=["pdf"]))
    btn_action = ft.FilledButton("Executar Divisão", icon=ft.icons.PLAY_ARROW, disabled=True, on_click=on_action_clicked)

    return ft.Container(content=ft.Column([
        ft.Text("Módulo: Dividir PDF", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_ACCENT_400),
        ft.Row([btn_select, txt_file]), ft.Divider(color=ft.colors.GREY_800),
        ft.Text("Configuração de Divisão:", weight=ft.FontWeight.BOLD), radio_mode, row_inputs,
        ft.Row([btn_action], alignment=ft.MainAxisAlignment.END)
    ]), padding=20, expand=True)


# --- TELA DE COMPRESSÃO ---
def get_compress_view(page: ft.Page):
    compressor_engine = PDFCompressor()
    state: dict[str, str | None] = {"input_path": None}
    txt_file = ft.Text("Nenhum arquivo selecionado", italic=True, color=ft.colors.GREY_500)

    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            first_file = e.files[0]
            if first_file.path:
                # CORRIGIDO: Extração forçada e explícita para string pura, eliminando o tipo Union do Linter
                file_path: str = str(first_file.path)
                state["input_path"] = file_path
                txt_file.value = f"Selecionado: {os.path.basename(file_path)}"
                btn_action.disabled = False
                page.update()



    def on_save_chosen(e: ft.FilePickerResultEvent):
        current_path = state["input_path"]
        if e.path and current_path:
            res = compressor_engine.compress(current_path, e.path)
            color = ft.colors.GREEN_700 if res["status"] == "success" else ft.colors.RED_700
            page.snack_bar = ft.SnackBar(ft.Text(res["message"]), bgcolor=color)
            page.snack_bar.open = True
            page.update()

    fp = ft.FilePicker(on_result=on_file_selected)
    sp = ft.FilePicker(on_result=on_save_chosen)
    page.overlay.extend([fp, sp])

    btn_select = ft.ElevatedButton("Selecionar PDF Pesado", icon=ft.icons.FILE_UPLOAD, on_click=lambda _: fp.pick_files(allowed_extensions=["pdf"]))
    btn_action = ft.FilledButton("Otimizar e Salvar", icon=ft.icons.COMPRESS, disabled=True, on_click=lambda _: sp.save_file(file_name="pdf_compactado.pdf", allowed_extensions=["pdf"]))

    return ft.Container(content=ft.Column([
        ft.Text("Módulo: Compactar PDF", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_ACCENT_400),
        ft.Text("Reduza o tamanho do arquivo removendo duplicatas e limpando streams internos de dados.", color=ft.colors.GREY_400),
        ft.Divider(color=ft.colors.GREY_800), ft.Row([btn_select, txt_file]),
        ft.Row([btn_action], alignment=ft.MainAxisAlignment.END)
    ]), padding=20, expand=True)

    # --- TELA DE ROTAÇÃO ---
def get_rotate_view(page: ft.Page):
    rotator_engine = PDFRotator()
    # Tipagem dinâmica explícita para evitar alertas de None do linter
    state: dict[str, str | None] = {"input_path": None}
    txt_file = ft.Text("Nenhum arquivo selecionado", italic=True, color=ft.colors.GREY_500)
    
    dropdown_degree = ft.Dropdown(
        label="Graus de Rotação", value="90", width=200,
        options=[
            ft.dropdown.Option("90", "90° Horário"), 
            ft.dropdown.Option("180", "180° Invertido"), 
            ft.dropdown.Option("270", "270° Anti-horário")
        ]
    )

    def on_file_selected(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            first_file = e.files[0]
            if first_file.path:
                # CORRIGIDO: Extração forçada e explícita para string pura, eliminando o tipo Union do Linter
                file_path: str = str(first_file.path)
                state["input_path"] = file_path
                txt_file.value = f"Selecionado: {os.path.basename(file_path)}"
                btn_action.disabled = False
                page.update()



    def on_save_chosen(e: ft.FilePickerResultEvent):
        current_path = state["input_path"]
        if e.path and current_path:
            # CORRIGIDO: Utilizando o conversor seguro para garantir tipo primitivo puro 'int' sem risco de None
            degrees = safe_int(dropdown_degree.value, default=90)
            
            res = rotator_engine.rotate_document(current_path, e.path, degrees)
            color = ft.colors.GREEN_700 if res["status"] == "success" else ft.colors.RED_700
            page.snack_bar = ft.SnackBar(ft.Text(res["message"]), bgcolor=color)
            page.snack_bar.open = True
            page.update()


    fp = ft.FilePicker(on_result=on_file_selected)
    sp = ft.FilePicker(on_result=on_save_chosen)
    page.overlay.extend([fp, sp])

    btn_select = ft.ElevatedButton(
        "Selecionar PDF", 
        icon=ft.icons.ROTATE_90_DEGREES_CCW, 
        on_click=lambda _: fp.pick_files(allowed_extensions=["pdf"])
    )
    btn_action = ft.FilledButton(
        "Rotacionar e Salvar", 
        icon=ft.icons.PLAY_ARROW, 
        disabled=True, 
        on_click=lambda _: sp.save_file(file_name="pdf_rotacionado.pdf", allowed_extensions=["pdf"])
    )

    return ft.Container(
        content=ft.Column([
            ft.Text("Módulo: Rotacionar Páginas", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_ACCENT_400),
            ft.Text("Ajuste a orientação geométrica de todas as folhas do documento simultaneamente.", color=ft.colors.GREY_400),
            ft.Divider(color=ft.colors.GREY_800), 
            ft.Row([btn_select, txt_file]), 
            dropdown_degree,
            ft.Row([btn_action], alignment=ft.MainAxisAlignment.END)
        ]), 
        padding=20, 
        expand=True
    )