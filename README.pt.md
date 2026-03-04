# CV Generator

Um script Python que gera um CV profissional em PDF de duas colunas a partir de arquivos de configuracao JSON. Projetado para atrair recrutadores, compativel com ATS (Applicant Tracking System) e otimizado para admissoes academicas. Cada aspecto e configuravel atraves de parametros. Iniciantes podem simplesmente modificar o arquivo `cv_data.json`, enquanto usuarios avancados podem mexer no `cv_style.json` ou diretamente no `generate_cv.py` para ajustes mais refinados. Um tutorial esta disponivel abaixo. Voce tambem pode mudar o idioma do CV usando `cv_lang.json`, mas uma revisao manual do texto traduzido e recomendada.

## Previa

![Previa do CV](cv_preview.png)

## Para que serve

- **Candidaturas a mestrado** (MonMaster, dosses universitarios) -- otimizado para comissoes de admissao academica francesas
- **Candidaturas a emprego** -- layout compativel com ATS com alta taxa de deteccao de palavras-chave
- **Perfis freelance / profissionais** -- design limpo e moderno com links clicaveis
- **CVs multilingues** -- alterne entre frances, ingles, espanhol e portugues com uma unica alteracao de configuracao

## Como funciona

O gerador le tres arquivos JSON e produz um PDF A4 de uma pagina:

1. **`cv_data.json`** -- Seu conteudo (quem voce e, o que voce fez)
2. **`cv_style.json`** -- Aparencia (cores, fontes, tamanhos, espacamentos)
3. **`cv_lang.json`** -- Rotulos de secao no idioma escolhido

O script usa `fpdf2` para renderizar um layout de duas colunas: uma barra lateral azul marinho escuro (30%) com informacoes pessoais, foto, objetivo e dados de contato, e uma area principal branca (70%) com formacoes, experiencias, competencias e certificacoes. Todo o texto na area principal e quase preto sobre branco para maxima legibilidade ATS.

As descricoes suportam listas com marcadores: linhas que comecam com `-` sao automaticamente renderizadas com marcadores coloridos e indentacao.

## Uso

```bash
pip install -r requirements.txt
python generate_cv.py
```

### Opcoes

```bash
python generate_cv.py --data cv_data.json --style cv_style.json --lang cv_lang.json -o output.pdf
```

| Opcao     | Padrao          | Descricao                          |
| --------- | --------------- | ---------------------------------- |
| `--data`  | `cv_data.json`  | Caminho para o conteudo do CV      |
| `--style` | `cv_style.json` | Caminho para a configuracao visual |
| `--lang`  | `cv_lang.json`  | Caminho para os rotulos de idioma  |
| `-o`      | `cv_output.pdf` | Caminho do PDF de saida            |

### Mudar o idioma

Edite `cv_lang.json` e altere o campo `"lang"`:

```json
{
  "lang": "pt"
}
```

Disponivel: `"fr"` (frances), `"en"` (ingles), `"es"` (espanhol), `"pt"` (portugues).

Isso altera os titulos de secao (Formacao, Experiencia, Competencias, Certificacoes) e o titulo da caixa Objetivo. O conteudo em si (descricoes, titulos) deve ser traduzido manualmente em `cv_data.json`.

## Estrutura de arquivos

| Arquivo            | Funcao                                                                        |
| ------------------ | ----------------------------------------------------------------------------- |
| `generate_cv.py`   | Script principal do gerador (~800 linhas)                                     |
| `cv_data.json`     | Conteudo do CV (infos pessoais, formacoes, experiencias, competencias, certificacoes) |
| `cv_style.json`    | Parametros visuais (fontes, tamanhos, cores, espacamentos, badges, rodape)    |
| `cv_lang.json`     | Rotulos de idioma para titulos de secao                                       |
| `fonts/`           | Arquivos OTF Font Awesome 7 para icones                                      |
| `badges/`          | Imagens de badges de certificacao (Credly)                                    |
| `requirements.txt` | Dependencias Python (`fpdf2`)                                                 |

## Funcionalidades

### Layout de duas colunas

O layout barra lateral (30%) + conteudo principal (70%) e um dos formatos de CV moderno mais populares:

- A barra lateral agrupa informacoes pessoais/contato separadamente do conteudo profissional
- Recrutadores podem localizar rapidamente os dados de contato
- A area principal oferece amplo espaco para descricoes de experiencia
- Sistemas ATS podem analisar a area de conteudo principal de forma confiavel

### Icones Font Awesome

O gerador detecta automaticamente arquivos OTF/TTF Font Awesome no diretorio `fonts/`:

- **Links sociais** (GitHub, LinkedIn) -- fonte `fa-brands`
- **Marcadores de contato** (email, telefone, endereco) -- fonte `fa-solid`
- **Links de certificacao** -- icone de link clicavel ao lado de cada nome
- **Decoracoes do rodape** -- icones esquerda/direita configuraveis

Retorno gracioso para renderizacao somente texto se as fontes nao estiverem presentes.

### Badges de certificacao

Cada certificacao pode exibir sua imagem de badge oficial (ex. Credly) ao lado do nome e emissor. As imagens de badge sao clicaveis e direcionam para a pagina da certificacao.

### Formatacao de listas

As descricoes suportam um formato hibrido -- uma frase de contexto seguida de marcadores:

```json
"description": "Frase de contexto sobre o cargo.\n- Primeira realizacao ou responsabilidade\n- Segunda realizacao com resultados quantificados\n- Terceiro ponto"
```

Linhas que comecam com `-` sao renderizadas com marcadores coloridos e indentacao apropriada.

### Suporte a foto

Suporta formatos JPG, JPEG, PNG, BMP e GIF. Se o nome exato do arquivo nao for encontrado, o gerador tenta automaticamente extensoes comuns.

### Badges de competencias coloridos

A secao de competencias usa badges pilula coloridos agrupados por categoria, cada um com uma cor distinta da familia dos azuis para coesao visual.

## Personalizacao

### Alterar o conteudo

Edite `cv_data.json`:

- `personal`: nome, titulo, foto, objetivo, sobre, informacoes de contato, links sociais
- `formations`: entradas de formacao com descricoes em lista
- `experiences`: entradas de experiencia com descricoes em lista
- `skills_section`: badges de competencias por categoria (idiomas, programacao, ferramentas, soft skills)
- `certifications`: entradas de certificacao com URLs e imagens de badge opcionais

### Alterar o estilo

Edite `cv_style.json` para ajustar qualquer parametro visual:

- **Barra lateral**: ratio de largura, cor de fundo, padding, tamanho da foto
- **Fontes**: familias titulo/corpo, fontes TTF/OTF personalizadas
- **Tamanhos de fonte**: cada elemento de texto tem seu proprio tamanho configuravel
- **Cores**: cada elemento tem sua propria cor RGB
- **Espacamentos**: gaps entre cada secao, ratio de altura de linha
- **Badges**: padding, raio, gap, cores por estilo (preenchido/contorno/destaque)
- **Secao de competencias**: tamanhos de badges, cores por categoria
- **Certificacoes**: tamanho de imagem, grade, colunas
- **Caixa de objetivo**: fundo, borda, cor do titulo, cor do texto, padding, raio
- **Rodape**: texto, tamanho de fonte, cor, icones, URL de link e imagem opcionais

### Usar fontes personalizadas

Adicione arquivos TTF/OTF e referencie-os no estilo:

```json
"fonts": {
  "heading": "MinhaFonte",
  "body": "MinhaFonte",
  "custom": {
    "MinhaFonte": {
      "": "fonts/MinhaFonte-Regular.ttf",
      "B": "fonts/MinhaFonte-Bold.ttf",
      "I": "fonts/MinhaFonte-Italic.ttf"
    }
  }
}
```

## Pesquisa de design

### Paleta de cores

A paleta foi escolhida com base em pesquisas de fontes do setor de recrutamento sobre o que funciona melhor com recrutadores humanos e ferramentas de triagem ATS/IA.

**Por que azul marinho?**

- O azul e a cor de CV n1 recomendada por todas as fontes -- transmite confianca, confiabilidade e competencia
- Especialmente adequado para tech/TI ja que a maioria das grandes empresas de tecnologia usa azul em seu branding
- A cor azul marinho escuro para titulos (`#003366`) alcancou uma **taxa de deteccao de palavras-chave ATS de 98%** nos testes

| Elemento            | Hex       | Justificativa                                        |
| ------------------- | --------- | ---------------------------------------------------- |
| Fundo barra lateral | `#1B2A4A` | Ratio de contraste com texto branco: ~12.5:1 (WCAG AAA) |
| Titulos de secao    | `#003366` | Taxa de deteccao ATS de 98%                          |
| Titulos de itens    | `#0476D0` | Recomendado para CVs tech/TI                         |
| Texto principal     | `#212121` | Contraste com branco: ~16:1 (WCAG AAA)               |
| Texto secundario    | `#555555` | Contraste com branco: ~7.5:1 (WCAG AA)               |

### Regras de compatibilidade ATS

1. O texto principal e quase preto sobre branco -- a "Regra 90-10"
2. Todas as palavras-chave criticas estao na area branca principal, nao na barra lateral
3. Ratios de contraste elevados (minimo 4.5:1 conforme WCAG AA) em cada combinacao texto-fundo
4. Paleta coesa de 2 cores (marinho + destaque azul) mais neutros
5. Fontes padrao (Helvetica) -- universalmente analisaveis por ATS

## Rodape

O rodape na parte inferior da barra lateral exibe uma linha de texto com icones decorativos e um link clicavel para o repositorio.

**Texto dinamico:** Quando o nome no CV e "Gabriel Verite" (o autor), o rodape exibe *"Generateur de CV developpe par mes soins"*. Para qualquer outro nome, muda automaticamente para *"CV generated with In:Veritas CV Generator"*. Ambos os textos sao configuraveis via `text` e `text_other` em `cv_style.json`.

**Datas de certificacao:** Cada entrada de certificacao suporta um campo opcional `"date"` exibido em texto italico pequeno abaixo do emissor.

### Icone de baleia

O pequeno icone de baleia ao lado do link do rodape e um toque pessoal -- e meu animal favorito. E puramente decorativo e nao tem impacto na analise ATS (esta na barra lateral, fora da area de conteudo principal).

Para remove-lo, limpe o campo `image_right` em `cv_style.json`:

```json
"footer": {
  "image_right": "",
  ...
}
```

## Atribuicao

- <a href="https://www.flaticon.com/free-icons/whale" title="whale icons">Whale icons created by Mayor Icons - Flaticon</a>

## Fontes

- [Resumly - Resume Color Scheme for ATS Compatibility & Readability](https://www.resumly.ai/blog/resume-color-scheme-for-ats-compatibility-and-readability)
- [AI ResumeGuru - Resume Colors: ATS-Safe Guide](https://airesume.guru/blog/resume-color-ats-safe-tips)
- [Resume.io - Best colors for a resume](https://resume.io/blog/should-you-use-color-on-your-resume)
- [Enhancv - How Does Color on a Resume Impact Your Chances?](https://enhancv.com/blog/color-on-resume/)
- [Jobscan - Should You Use Color on Your Resume?](https://www.jobscan.co/blog/best-color-for-resume/)
- [WebAIM - Contrast and Color Accessibility (WCAG 2)](https://webaim.org/articles/contrast/)
- [Mastersportal - 6 Steps to Writing an Awesome Academic CV](https://www.mastersportal.com/articles/2626/6-steps-to-writing-an-awesome-academic-cv-for-masters-application.html)
- [MakeMyCV - CV Master : Les cles pour seduire le jury](https://makemycv.com/fr/cv-master)
