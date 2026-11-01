import os
from typing import Dict
import fitz  # PyMuPDF
from backend.merger import PDFMerger

class PDFRotator:
    """
    Engine responsável por alterar a rotação de páginas de arquivos PDF.
    """

    def rotate_document(self, input_path: str, output_path: str, degrees: int) -> Dict[str, str]:
        """
        Rotaciona todas as páginas do PDF no sentido horário com base nos graus informados.
        Ângulos aceitos pelo padrão PDF: 90, 180, 270.
        """
        if degrees not in [90, 180, 270]:
            return {"status": "error", "message": "Ângulo de rotação inválido. Escolha entre 90, 180 ou 270 graus."}

        if not PDFMerger.validate_pdf(input_path):
            return {"status": "error", "message": "Arquivo de entrada inválido ou corrompido."}

        try:
            with fitz.open(input_path) as doc:
                for page in doc:
                    # O método set_rotation adiciona os graus de forma absoluta ou relativa dependendo do PDF.
                    # Para garantir o comportamento esperado, somamos à rotação atual e aplicamos o módulo 360.
                    current_rotation = page.rotation
                    new_rotation = (current_rotation + degrees) % 360
                    page.set_rotation(new_rotation)

                # Garante diretório de destino
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                doc.save(output_path, garbage=3, deflate=True)
                
            return {"status": "success", "message": f"PDF rotacionado com sucesso em: {output_path}"}

        except Exception as e:
            return {"status": "error", "message": f"Falha interna durante a rotação: {str(e)}"}
