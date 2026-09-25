# Dashboard Censo Pesqueiro

Dashboard interativo para visualização e análise dos dados do censo pesqueiro da Zona Costeira Amazônica, desenvolvido para o Observatório da Costa Amazônica (OCA).

## Sobre o projeto

O projeto transforma registros de coleta pesqueira em uma interface visual para consulta, comparação e acompanhamento ao longo do tempo. A aplicação reúne indicadores gerais, rankings de espécies, filtros por território e período, localização das RESEXs e gráficos de evolução mensal.

O dashboard foi pensado para apoiar a leitura dos dados por equipes técnicas, pesquisadores, gestores e demais pessoas interessadas na atividade pesqueira da região. Em vez de exigir a análise manual da planilha, a aplicação organiza os principais recortes em uma página interativa.

## Objetivo

O objetivo é facilitar o acesso aos dados do censo pesqueiro e apoiar análises sobre:

- volume total registrado em quilogramas;
- espécies com maior participação no peso coletado;
- distribuição dos registros entre municípios e RESEXs;
- diferenças entre meses e territórios;
- evolução temporal das principais espécies de uma RESEX.

> **Status:** projeto em desenvolvimento.

<!-- IMAGEM PENDENTE: inserir aqui uma captura da tela inicial do dashboard. -->

## Funcionalidades

- Indicadores gerais de peso total, número de espécies, municípios e RESEXs.
- Ranking geral das 10 espécies com maior peso registrado.
- Filtros por RESEX e mês.
- Mapa interativo das RESEXs com basemap OpenStreetMap ou Esri Satélite.
- Ranking filtrado por RESEX e mês, com peso total e participação percentual.
- Série temporal mensal das espécies mais relevantes da RESEX selecionada.
- Formatação dos valores em português, incluindo separadores numéricos, meses e unidades em quilogramas.
- Interface personalizada com identidade visual do OCA.

<!-- IMAGEM PENDENTE: inserir uma captura da seção de filtros e do mapa. -->

## Como utilizar o dashboard

Após iniciar a aplicação, a página apresenta uma visão geral dos dados e, em seguida, as ferramentas de exploração:

1. Consulte os KPIs e o ranking geral para obter uma visão inicial do conjunto de registros.
2. Escolha uma RESEX no filtro correspondente.
3. Selecione um ou mais meses para restringir a análise.
4. Use o mapa para localizar as RESEXs e alterne o tipo de mapa quando necessário.
5. Analise o ranking filtrado, observando o peso total e a participação percentual de cada espécie.
6. Ajuste o controle `Top N espécies` para acompanhar a série temporal das espécies mais relevantes da RESEX selecionada.

Os gráficos são interativos: é possível passar o cursor sobre os elementos para consultar detalhes e usar os controles disponíveis do Plotly para explorar os resultados.

<!-- IMAGEM PENDENTE: inserir uma captura da análise por RESEX e da série temporal. -->

## Tecnologias

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Folium](https://python-visualization.github.io/folium/)
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)
- [Pillow](https://python-pillow.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)

## Estrutura do projeto

```text
Dashboard_Censo_Pesqueiro/
├── app/
│   └── dashboard_censo.py       # Aplicação Streamlit
├── assets/
│   └── oca_site.png             # Identidade visual utilizada no app
├── data/
│   └── Base_Coleta_OCA_ATUALIZADA_02.07.2025.xlsx
├── .streamlit/
│   └── config.toml              # Tema visual do Streamlit
├── requirements.txt              # Dependências Python
└── README.md
```

## Pré-requisitos

- Python 3.9 ou superior.
- `pip` disponível no ambiente Python.
- Arquivo de dados Excel autorizado para uso e publicação.

Os dados podem conter informações institucionais ou sensíveis. Antes de publicar o repositório, confirme se a base pode ser disponibilizada publicamente e, quando necessário, mantenha o arquivo fora do GitHub.

## Instalação local

No terminal, a partir da raiz do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execução

A aplicação atualmente utiliza caminhos relativos ao diretório de execução. Para executar a versão presente neste repositório, copie ou disponibilize no diretório de execução os arquivos esperados pelo script:

- `Base_Coleta_OCA_ATUALIZADA_02.07.2025.xlsx`
- `oca_site.png`
- `oca_logo2.png` para o cabeçalho, caso essa imagem seja utilizada

Em seguida, execute:

```bash
streamlit run app/dashboard_censo.py
```

O Streamlit abrirá o dashboard no navegador, normalmente em `http://localhost:8501`.

> **Atenção:** na estrutura atual, a base está em `data/` e a imagem disponível está em `assets/`. Para uma publicação reproduzível, recomenda-se ajustar o código para construir os caminhos a partir da raiz do projeto, por exemplo com `Path(__file__).resolve().parents[1]`, ou então adaptar a organização dos arquivos antes do deploy.

<!-- IMAGEM PENDENTE: inserir uma captura da análise por RESEX e da série temporal. -->

## Dados utilizados

O dashboard lê uma planilha Excel com registros mensais de produção pesqueira. Entre as colunas utilizadas pelo código estão:

| Coluna | Uso |
| --- | --- |
| `Nome Popular` | Nome da espécie e agrupamentos dos rankings |
| `Total (kg)` | Peso usado nos KPIs, gráficos e série temporal |
| `Qtidades` | Quantidade numérica, quando disponível |
| `Resex` | Identificação da reserva extrativista |
| `Municipio` | Contagem de municípios e normalização de nomes |
| `Mês` | Filtro mensal e conversão para número do mês |
| `Ano` | Construção da série temporal |

Durante o carregamento, o app converte tipos numéricos, remove registros sem campos essenciais, normaliza nomes de municípios e cria uma data mensal para os gráficos temporais.

## Publicação no GitHub

Antes do primeiro `push`:

1. Renomeie `gitignore.txt` para `.gitignore`, para que o Git reconheça as regras de exclusão.
2. Verifique se a planilha pode ser publicada e remova dados protegidos ou não autorizados.
3. Remova arquivos temporários, como `.~lock.*`.
4. Confirme que `requirements.txt`, `README.md`, o código e os assets necessários estão versionados.
5. Revise os caminhos relativos descritos na seção de execução.

Exemplo de configuração inicial do repositório:

```bash
git init
git add README.md requirements.txt app assets .streamlit .gitignore
git commit -m "Adiciona dashboard do censo pesqueiro"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

Substitua `SEU_USUARIO/SEU_REPOSITORIO` pelo endereço do repositório criado no GitHub.

## Deploy com Streamlit Community Cloud

Para publicar a aplicação no Streamlit Community Cloud:

1. Envie o projeto para um repositório GitHub.
2. Crie uma nova aplicação no Streamlit Community Cloud.
3. Selecione o repositório e a branch desejados.
4. Informe `app/dashboard_censo.py` como arquivo principal.
5. Publique somente depois de validar os caminhos da base e das imagens.

Se a base não puder ser pública, ela não deve ser versionada nem embutida no deploy. Nesse caso, será necessário adaptar a aplicação para receber os dados por uma fonte autorizada ou por um mecanismo de configuração seguro.

## Créditos

Projeto desenvolvido para o **Observatório da Costa Amazônica (OCA)**.

© Observatório da Costa Amazônica — Oca Social.
