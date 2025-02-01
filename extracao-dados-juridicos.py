import os
import PyPDF2
import pandas as pd
import re


def limpar_texto(texto: str) -> str:
    """
    Remove caracteres indesejados (\n, \t, etc.) de um texto.
    """
    return texto.replace('\n', ' ').replace('\t', ' ').strip()


def segmentar_texto(texto: str) -> list[str]:
    """
    Divide o texto em duas partes principais: antes e depois de 'RELATÓRIO E VOTO'.
    """
    return texto.split("RELATÓRIO E VOTO", 1)


def get_num_processo(texto: str) -> str:
    """
    Extrai o número do processo usando regex
    """
    match = re.search(r"Processo\s*:\s*(\S+)", texto, re.IGNORECASE)
    return match.group(1) if match else "Número de processo não encontrado"


def get_interessado(texto: str) -> str:
    """
    Extrai o interessado e seu CPF usando regex
    """
    match = re.search(r"Interessado/CPF\s*:\s*(.+?)(?=Relator|$)", texto, re.IGNORECASE)
    return match.group(1).strip() if match else "Interessado/CPF não encontrado"


def get_cargo(texto: str) -> str:
    """
    Extrai o cargo do interessado usando regex
    """
    match = re.search(r"no cargo\s+(.+?);", texto, re.IGNORECASE)
    return match.group(1).strip() if match else "Cargo não encontrado"


def get_orgao_entidade(texto: str) -> str:
    """
    Extrai o Órgão/Entidade usando regex.
    """
    match = re.search(r"Órgão/Entidade\s*:\s*(.+?)(?=Natureza|$)", texto, re.IGNORECASE)
    return match.group(1).strip() if match else "Órgão/Entidade não encontrado"


def get_voto(texto: str) -> str:
    """
    Extrai a parte do texto referente ao voto, iniciando após 'VOTO'.
    """
    match = re.search(r"VOTO\s*(.+)", texto, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else "Voto não encontrado"


def get_conclusao_voto(texto: str) -> str:
    """
    Extrai a conclusão do voto, começando com 'Conclusos os autos' e terminando no próximo ponto relevante.
    """
    match = re.search(r"(Conclusos os autos\s*.+?)(?=Tribunal de Contas|$)", texto, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else "Conclusão do voto não encontrada"


def main(pasta_input: str, pasta_output: str):
    """
    Lê arquivos PDF de uma pasta, extrai informações e salva em CSV.
    """
    nomes_pdf = [f for f in os.listdir(pasta_input) if f.lower().endswith('.pdf')]

    if not nomes_pdf:
        print("Nenhum arquivo PDF encontrado na pasta especificada.")
        return

    resultados = {
        "num_processo": [],
        "interessado": [],
        "cargo_do_interessado": [],
        "orgao_entidade": [],
        "conclusao_voto": []
    }
    textos_segmentados = {"nome_pdf": [], "acordao": [], "relatorio": []}

    for nome_pdf in nomes_pdf:
        caminho_arquivo = os.path.join(pasta_input, nome_pdf)
        with open(caminho_arquivo, 'rb') as f:
            leitor = PyPDF2.PdfReader(f)
            texto = ''.join([pagina.extract_text() for pagina in leitor.pages])

        texto_limpo = limpar_texto(texto)
        partes_texto = segmentar_texto(texto_limpo)

        # Tratando caso o texto não seja dividido corretamente
        if len(partes_texto) == 2:
            textos_segmentados["nome_pdf"].append(nome_pdf)
            textos_segmentados["acordao"].append(partes_texto[0].strip())
            textos_segmentados["relatorio"].append("RELATÓRIO E VOTO " + partes_texto[1].strip())
        else:
            textos_segmentados["nome_pdf"].append(nome_pdf)
            textos_segmentados["acordao"].append(texto_limpo)
            textos_segmentados["relatorio"].append("Texto não segmentado corretamente")

        # Extraindo informações com regex
        num_processo = get_num_processo(texto_limpo)
        interessado = get_interessado(texto_limpo)
        cargo_do_interessado = get_cargo(texto_limpo)
        orgao_entidade = get_orgao_entidade(texto_limpo)
        voto = get_voto(texto_limpo)
        conclusao_voto = get_conclusao_voto(texto_limpo)

        resultados["num_processo"].append(num_processo)
        resultados["interessado"].append(interessado)
        resultados["cargo_do_interessado"].append(cargo_do_interessado)
        resultados["orgao_entidade"].append(orgao_entidade)
        resultados["conclusao_voto"].append(conclusao_voto)

    # Salvando resultados em CSV
    os.makedirs(pasta_output, exist_ok=True)

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(os.path.join(pasta_output, "resultado_completo.csv"), index=False)

    df_textos_segmentados = pd.DataFrame(textos_segmentados)
    df_textos_segmentados.to_csv(os.path.join(pasta_output, "segmentado.csv"), index=False)

    print(f"Extração concluída. Resultados salvos em: {pasta_output}")


# Executando o script
main(pasta_input="input", pasta_output="output")
