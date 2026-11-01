import os
from typing import List, Dict, Union
import fitz  # PyMuPDF
from backend.merger import PDFMerger  # Reaproveitando a validação de segurança

class PDFSplitter:
    """
    Engine responsável pela divisão e extração segura de páginas de arquivos PDF.
    """

    def split_by_range(self, input_path: str, output_path: str, start_page: int, end_page: int) -> Dict[str, str]:
        """
        Extrai um intervalo de páginas (base 1) e salva em um novo arquivo PDF.
        Exemplo: páginas 2 a 5.
        """
        if not PDFMerger.validate_pdf(input_path):
            return {"status": "error", "message": "Arquivo de entrada inválido ou corrompido."}

        try:
            with fitz.open(input_path) as src_pdf:
                total_pages = src_pdf.page_count

                # Validação de limites (Convertendo interface base 1 do usuário para base 0 do sistema)
                if start_page < 1 or end_page > total_pages or start_page > end_page:
                    return {
                        "status": "error", 
                        "message": f"Intervalo inválido. O documento possui apenas {total_pages} páginas."
                    }

                # Cria um novo documento vazio para o trecho extraído
                output_pdf = fitz.open()
                # O PyMuPDF seleciona intervalos usando base 0 (start-1) e o limite superior é exclusivo
                output_pdf.insert_pdf(src_pdf, from_page=start_page - 1, to_page=end_page - 1)
                
                # Garante diretório de destino
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_pdf.save(output_path, garbage=3, deflate=True)
                output_pdf.close()

                return {
                    "status": "success", 
                    "message": f"Páginas {start_page} a {end_page} extraídas com sucesso para: {output_path}"
                }

        except Exception as e:
            return {"status": "error", "message": f"Falha interna durante a divisão por intervalo: {str(e)}"}

    def split_all_pages(self, input_path: str, output_dir: str) -> Dict[str, Union[str, List[str]]]:
        """
        Divide o PDF de entrada gerando um arquivo individual para cada página.
        Salva todos na pasta de saída indicada.
        """
        if not PDFMerger.validate_pdf(input_path):
            return {"status": "error", "message": "Arquivo de entrada inválido ou corrompido."}

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        generated_files = []
        # Captura o nome do arquivo sem a extensão .pdf
        base_name = os.path.splitext(os.path.basename(input_path))[0]

        try:
            with fitz.open(input_path) as src_pdf:
                for page_num in range(src_pdf.page_count):
                    output_pdf = fitz.open()
                    # Insere apenas a página atual do laço
                    output_pdf.insert_pdf(src_pdf, from_page=page_num, to_page=page_num)
                    
                    # Nomeia o arquivo ex: "documento_pagina_1.pdf"
                    file_name = f"{base_name}_pagina_{page_num + 1}.pdf"
                    full_output_path = os.path.join(output_dir, file_name)
                    
                    output_pdf.save(full_output_path, garbage=3, deflate=True)
                    output_pdf.close()
                    generated_files.append(full_output_path)

                return {
                    "status": "success", 
                    "message": f"PDF desmembrado com sucesso em {len(generated_files)} arquivos.",
                    "files": generated_files
                }

        except Exception as e:
            return {"status": "error", "message": f"Falha interna ao desmembrar páginas: {str(e)}"}
