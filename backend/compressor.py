import os
from typing import Dict
import fitz  # PyMuPDF
from backend.merger import PDFMerger

class PDFCompressor:
    """
    Engine responsável pela otimização e redução do tamanho de arquivos PDF.
    """

    def compress(self, input_path: str, output_path: str) -> Dict[str, str]:
        """
        Abre o PDF e salva aplicando algoritmos de compressão máxima de dados 
        e reuso de objetos idênticos (imagens/fontes repetidas).
        """
        if not PDFMerger.validate_pdf(input_path):
            return {"status": "error", "message": "Arquivo de entrada inválido ou corrompido."}

        try:
            with fitz.open(input_path) as doc:
                # Garante diretório de destino
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Parâmetros de alta otimização:
                # garbage=4: Coleta de lixo agressiva, remove objetos não utilizados e duplicados
                # deflate=True: Ativa a compressão zlib nos fluxos de dados de texto/gráficos
                doc.save(
                    output_path, 
                    garbage=4, 
                    deflate=True, 
                    clean=True
                )
                
            return {"status": "success", "message": f"PDF compactado com sucesso em: {output_path}"}

        except Exception as e:
            return {"status": "error", "message": f"Falha interna durante a compressão: {str(e)}"}
