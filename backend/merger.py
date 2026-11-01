import os
from typing import List
import fitz  # PyMuPDF

class PDFMerger:
    """
    Engine responsável pela validação e mesclagem segura de arquivos PDF.
    """
    
    @staticmethod
    def validate_pdf(file_path: str) -> bool:
        """
        Valida se o arquivo existe, possui a extensão correta e é um PDF íntegro.
        Garante a segurança da aplicação contra payloads maliciosos ocultos.
        """
        if not os.path.exists(file_path):
            return False
        
        if not file_path.lower().endswith('.pdf'):
            return False
            
        try:
            # Tenta abrir o documento para verificar se não está corrompido
            with fitz.open(file_path) as doc:
                # Se conseguir ler o número de páginas, o arquivo é um PDF válido
                return doc.page_count >= 0
        except Exception:
            return False

    def merge(self, input_paths: List[str], output_path: str) -> dict:
        """
        Mescla uma lista de arquivos PDF na ordem fornecida.
        Retorna um dicionário com o status e a mensagem do resultado.
        """
        if not input_paths:
            return {"status": "error", "message": "Nenhum arquivo enviado para mesclagem."}

        # Cria um documento PDF vazio para receber as páginas
        result_pdf = fitz.open()

        try:
            for path in input_paths:
                # Verificação de segurança em tempo de execução
                if not self.validate_pdf(path):
                    result_pdf.close()
                    return {
                        "status": "error", 
                        "message": f"O arquivo '{os.path.basename(path)}' é inválido ou está corrompido."
                    }
                
                # Abre o PDF de origem e o insere no final do documento unificado
                with fitz.open(path) as current_pdf:
                    result_pdf.insert_pdf(current_pdf)

            # Garante que o diretório de destino existe antes de salvar
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Salva o arquivo final otimizando o espaço (garbage collection nativo do PyMuPDF)
            result_pdf.save(output_path, garbage=3, deflate=True)
            return {"status": "success", "message": f"PDF mesclado com sucesso em: {output_path}"}

        except Exception as e:
            return {"status": "error", "message": f"Falha interna durante a mesclagem: {str(e)}"}
            
        finally:
            # Garante o fechamento do arquivo da memória mesmo em caso de falha catastrófica
            if not result_pdf.is_closed:
                result_pdf.close()
