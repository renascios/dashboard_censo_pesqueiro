# Dashboard Censo Pesqueiro

Dashboard interativo para análise e visualização dos dados do censo pesqueiro da Zona Costeira Amazônica, desenvolvido para apoiar a leitura, comparação e acompanhamento de indicadores pesqueiros por RESEX, município, mês e espécie. O projeto foi feito para o Observatório da Costa Amazônica (OCA), e atualmente é utilizado por este.

## Visão geral

Este projeto transforma registros em planilha Excel em uma interface analítica web, permitindo explorar os principais indicadores do setor pesqueiro de forma visual, rápida e acessível. Em vez de depender de leitura manual de tabelas, a aplicação organiza os dados em KPIs, rankings, filtros, mapas interativos e séries temporais.

A proposta é facilitar a análise por parte de pesquisadores, gestores, equipes técnicas e interessados no acompanhamento da atividade pesqueira na região amazônica. A interface foi pensada para ser clara, informativa e de fácil navegação, com foco em tomada de decisão e diagnóstico territorial.

## Objetivo do projeto

O dashboard tem como principal objetivo permitir o monitoramento e a análise de dados do censo pesqueiro, com destaque para:

- volume total capturado em quilogramas;
- espécies com maior representatividade no total registrado;
- distribuição geográfica por RESEX e município;
- comparação entre meses e períodos;
- evolução temporal das espécies mais relevantes;
- visualização do contexto territorial da Zona Costeira Amazônica.

## Funcionalidades

- Painel de indicadores gerais com métricas principais;
- Ranking das espécies por peso total;
- Filtros por RESEX e mês;
- Mapa interativo das RESEXs com diferentes bases cartográficas;
- Análise filtrada por RESEX com participação percentual por espécie;
- Série temporal de evolução mensal das espécies selecionadas;
- Visualização em português com formatação de números e unidades;
- Interface responsiva e voltada para navegação em navegador;
- Estilo visual personalizado com identidade do Observatório da Costa Amazônica.

## Stack tecnológica

O projeto utiliza as seguintes tecnologias:

- [Python](https://www.python.org/) — linguagem principal da aplicação;
- [Streamlit](https://streamlit.io/) — criação da interface web interativa;
- [Pandas](https://pandas.pydata.org/) — manipulação, limpeza e agregação dos dados;
- [Plotly](https://plotly.com/python/) — gráficos interativos e dashboards analíticos;
- [Folium](https://python-visualization.github.io/folium/) — mapas interativos;
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium) — integração do Folium com Streamlit;
- [Pillow](https://python-pillow.org/) — processamento de imagens e uso de logotipos;
- [openpyxl](https://openpyxl.readthedocs.io/) — leitura de arquivos Excel.

## Estrutura do repositório

```text
dashboard_censo_pesqueiro/
├── app/
│   └── dashboard_censo.py          # Aplicação principal em Streamlit
├── assets/
│   └── oca_site.png                # Logotipo ou imagem visual da aplicação
├── data/
│   └── Base_Coleta_OCA_ATUALIZADA_02.07.2025.xlsx
├── .streamlit/
│   └── config.toml                 # Configuração visual do Streamlit
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação do repositório
└── .gitignore                      # Arquivos e pastas ignorados pelo Git
```

> Observação: a estrutura real do projeto pode variar conforme a forma como o repositório foi clonado ou adaptado. O importante é manter os arquivos de dados e ativos visuais acessíveis ao código da aplicação.

## Pré-requisitos

Antes de clonar e executar o projeto, verifique se o ambiente atende aos requisitos abaixo:

- Python 3.9 ou superior;
- `pip` instalado e configurado;
- ambiente virtual recomendado para isolar dependências;
- arquivo Excel com os dados do censo pesqueiro disponível localmente.

> Importante: alguns dados podem conter informações sensíveis, institucionais ou não autorizadas para publicação. Antes de subir o projeto para um repositório público, confirme se a base pode ser compartilhada.

## Como clonar o repositório

No terminal, execute:

```bash
git clone https://github.com/seu-usuario/dashboard-censo-pesqueiro.git
cd dashboard-censo-pesqueiro
```

Se o repositório estiver em um ambiente local ou em outra URL do GitHub, ajuste o comando conforme o endereço correto.

## Configuração do ambiente

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Em seguida:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Como executar a aplicação

A aplicação pode ser iniciada com o comando abaixo:

```bash
streamlit run app/dashboard_censo.py
```

O dashboard será aberto em um navegador local, normalmente em:

```text
http://localhost:8501
```

## Dados e configuração necessários

O dashboard foi desenvolvido para ler uma planilha Excel contendo registros mensais de produção pesqueira. A estrutura esperada inclui colunas como:

- `Nome Popular`
- `Total (kg)`
- `Qtidades`
- `Resex`
- `Municipio`
- `Mês`
- `Ano`

O código realiza limpeza, conversão de tipos, normalização de nomes e montagem temporal para alimentar os gráficos e filtros. Caso o arquivo não seja encontrado ou esteja ausente no caminho esperado, a aplicação exibirá uma mensagem de erro e terminará a execução.

## Uso do dashboard

Após iniciar a aplicação, o usuário pode:

1. visualizar os indicadores gerais do conjunto de dados;
2. consultar o ranking das espécies com maior peso acumulado;
3. filtrar os dados por RESEX e por mês;
4. analisar o mapa interativo das reservas extrativistas;
5. comparar o desempenho por espécie em diferentes períodos;
6. ajustar o controle de quantidade de espécies no gráfico temporal para explorar tendências.

Os gráficos are interativos e permitem análise detalhada por hover, com leitura de valores e variações ao longo do tempo.

## Personalização e manutenção

O projeto foi organizado para facilitar ajustes e extensões futuras. Entre os pontos que podem ser melhorados estão:

- organização dos caminhos de arquivos usando `Path` e base do projeto;
- parametrização do nome do arquivo Excel em uma variável de ambiente ou configuração;
- melhoria na estrutura de dados para publicação em produção;
- adaptação da interface para outros contextos além do censo pesqueiro.

## Implantação

O dashboard também pode ser publicado em ambientes web para acesso compartilhado. Uma opção comum é usar o Streamlit Community Cloud.

### Fluxo recomendado

1. enviar o projeto para um repositório GitHub;
2. criar uma nova aplicação no Streamlit Community Cloud;
3. selecionar o repositório e a branch correta;
4. apontar o arquivo principal para `app/dashboard_censo.py`;
5. verificar se os caminhos de dados e imagens permanecem válidos no ambiente deployado.

Se a base de dados não puder ser compartilhada publicamente, o ideal é manter o arquivo em ambiente local ou em uma fonte segura e não versioná-lo no repositório.

## Considerações finais

Este projeto é uma solução prática para transformar dados pesqueiros em uma ferramenta analítica acessível e visualmente clara. Ele combina coleta, organização e apresentação dos dados em um único painel, permitindo uma leitura muito mais eficiente do cenário observado na região.

O repositório é especialmente útil para públicos interessados em:

- ciência de dados aplicada ao setor pesqueiro;
- monitoramento territorial e socioambiental;
- geração de insights para tomada de decisão;
- apresentação de indicadores em formato visual e interativo.

## Créditos

Projeto desenvolvido para o Observatório da Costa Amazônica (OCA).

© Observatório da Costa Amazônica — Oca Social.
