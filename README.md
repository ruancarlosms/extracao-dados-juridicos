# Extrator de Informações de PDFs de Processos

## Descrição
Este projeto consiste em um script Python que processa arquivos PDF contendo informações de processos administrativos, extrai dados relevantes e os organiza em arquivos CSV. É especialmente útil para automatizar a análise de documentos jurídicos ou administrativos, reduzindo a necessidade de revisão manual.

## Funcionalidades
- **Leitura de PDFs**: Processa vários arquivos PDF dentro de um diretório.
- **Extração de informações**: Captura automaticamente dados essenciais como:
  - Número do processo
  - Interessado e CPF
  - Cargo do interessado
  - Órgão ou entidade envolvida
  - Conclusão do voto
- **Segmentação do texto**: Divide o documento entre "Acórdão" e "Relatório e Voto".
- **Exportação para CSV**: Os dados extraídos são organizados em planilhas para análise posterior.

## Como Usar
1. **Configurar diretórios**
   - Crie uma pasta `input/` e coloque os arquivos PDF nela.
   - Crie uma pasta `output/` (ou o script irá criá-la automaticamente para salvar os resultados).

2. **Executar o script**
   - Rode o seguinte comando no terminal:
     ```bash
     python script.py
     ```

3. **Ver os resultados**
   - O script gerará dois arquivos CSV dentro da pasta `output/`:
     - `resultado_completo.csv` contendo os dados extraídos.
     - `segmentado.csv` com a segmentação do texto.

## Problemas que este projeto soluciona
- **Automatiza a extração de dados**: Em vez de copiar manualmente informações de documentos extensos, o script faz isso automaticamente.
- **Reduz erros humanos**: A captura automatizada garante maior precisão e consistência nos dados extraídos.
- **Facilita análise em larga escala**: Com os dados em formato CSV, é mais fácil realizar buscas, filtrar e processar informações em massa.

## Requisitos
- Python 3.x
- Bibliotecas necessárias:
  ```bash
  pip install PyPDF2 pandas
  ```

## Possíveis Melhorias
- Adicionar suporte a outros formatos de documentos.
- Melhorar a precisão da extração com modelos de NLP.
- Criar uma interface gráfica para facilitar o uso por pessoas sem conhecimento técnico.

