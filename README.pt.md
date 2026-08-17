# CV Generator

**[English](README.md)** | **[Français](README.fr.md)** | **[Español](README.es.md)**

Crie um CV PDF profissional de duas colunas, atraente para recrutadores e compativel com ATS — seja com um **aplicativo de desktop** (preencha um formulario, escolha suas cores, clique em Gerar) ou **manualmente** com Python e arquivos de configuracao JSON. Projetado para atrair recrutadores, compativel com ATS (Applicant Tracking System) e otimizado para admissoes academicas.

## Previa

![Previa do CV](cv_preview.png)

> **Nota:** Este proprio CV me garantiu uma vaga no meu novo mestrado -- o que e bem legal.

## Para que serve

- **Candidaturas a mestrado** (MonMaster, dosses universitarios) -- otimizado para comissoes de admissao academica francesas
- **Candidaturas a emprego** -- layout compativel com ATS com alta taxa de deteccao de palavras-chave
- **Perfis freelance / profissionais** -- design limpo e moderno com links clicaveis
- **CVs multilingues** -- alterne entre frances, ingles, espanhol e portugues com um unico clique

## Duas formas de usar

| | Aplicativo de desktop (release) | Manual (Python + JSON) |
| --- | --- | --- |
| Para | Todos -- sem conhecimento tecnico | Quem quer ajustar tudo nos minimos detalhes |
| Requer | Nada no Windows/Linux; Python no macOS | Python 3.9+ |
| Controla | Conteudo, foto, cores, tamanhos, ordem das secoes, selos | Tudo isso mais cada parametro de estilo avancado |

## Usar o aplicativo de desktop (recomendado)

### Como obter

Baixe o pacote mais recente da [pagina de Releases](https://github.com/In-Veritas/cv-generator/releases) e descompacte-o:

- **Windows** (`…-win64.zip`): de um duplo clique em `CV-Generator.exe`. Se o SmartScreen mostrar "O Windows protegeu o computador", clique em *Mais informacoes* → *Executar assim mesmo* (o exe simplesmente nao e assinado digitalmente).
- **Linux** (`…-linux-x64.tar.gz`): execute `chmod +x CV-Generator && ./CV-Generator` a partir da pasta descompactada.
- **macOS / qualquer OS** (`…-source.zip`): instale Python 3.9+, depois `pip3 install -r requirements.txt` e `python3 cv_gui.py`.

Mantenha os arquivos descompactados juntos -- o aplicativo le `fonts/`, `cv_style.json`, `whale.png` e `app_icon.png` da sua propria pasta.

### Como usar

1. **Escolha um idioma** -- Francais, English, Espanol ou Portugues. Ele define a interface e os titulos de secao impressos no PDF, e pode ser mudado a qualquer momento no menu *Idioma*.
2. **Preencha as abas.** Cada caixa de texto mostra uma instrucao cinza explicando o que escrever. Nas abas de listas (Formacao, Experiencia, Competencias, Certificacoes), clique em *Adicionar* para criar uma entrada; selecione uma entrada para edita-la -- as mudancas sao salvas automaticamente enquanto voce digita.
3. **Escolha a ordem das secoes.** Arraste as abas de secoes para reordena-las -- o PDF imprime suas secoes exatamente nessa ordem. O menu *Predefinicoes* oferece **Profissional** (Experiencia primeiro -- o padrao) e **Academico** (Formacao primeiro).
4. **De estilo.** A aba *Estilo* tem seletores de cores e tamanhos, mais um botao *Importar estilo JSON…* que carrega um `cv_style.json` completo (veja a secao manual abaixo para tudo o que ele pode conter).
5. **Adicione selos de certificacao.** A aba Certificacoes tem um botao *Ajuda* com um guia passo a passo e uma ferramenta *Gerar selo…* que recorta qualquer imagem em quadrado e ajusta para 300×300 px.
6. **Gere.** O aplicativo verifica os campos que os ATS e as ferramentas de IA dos recrutadores costumam analisar (nome, contato, objetivo, entradas, competencias, datas) e avisa se estiverem vazios -- depois produz o PDF onde voce escolher.

Dicas: **Arquivo → Salvar dados do CV (.json)** mantem seu trabalho reutilizavel (o arquivo e totalmente compativel com o gerador de linha de comando abaixo), e a pequena baleia no canto inferior esquerdo abre minha pagina do GitHub.

O manual completo do aplicativo -- com solucao de problemas -- acompanha cada pacote e tambem pode ser lido aqui: [release_readme.md](release_readme.md).

### Compilar o aplicativo voce mesmo

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name CV-Generator --icon whale.ico cv_gui.py
```

Um workflow do GitHub Actions (`.github/workflows/build-release.yml`) compila automaticamente os pacotes de Windows, Linux e macOS sob demanda ou quando uma tag `v*` e enviada.

## Uso manual (Python + JSON)

Para controle total, use o gerador diretamente e edite os arquivos JSON a mao.

```bash
pip install -r requirements.txt
python generate_cv.py
```

### Opcoes

```bash
python generate_cv.py --data cv_data.json --style cv_style.json --lang cv_lang.json -o output.pdf
```

| Opcao     | Padrao          | Descricao                            |
| --------- | --------------- | ------------------------------------ |
| `--data`  | `cv_data.json`  | Caminho para o conteudo do CV        |
| `--style` | `cv_style.json` | Caminho para a configuracao visual   |
| `--lang`  | `cv_lang.json`  | Caminho para os rotulos de idioma    |
| `-o`      | `cv_output.pdf` | Caminho do PDF de saida              |

### Os tres arquivos JSON

1. **`cv_data.json`** -- Seu conteudo (quem voce e, o que voce fez). `cv_data_fr.json` e a versao francesa dos meus proprios dados, utilizavel com `--data`.
2. **`cv_style.json`** -- A aparencia (cores, fontes, tamanhos, espacamentos).
3. **`cv_lang.json`** -- Os rotulos de secao e o subtexto do rodape no idioma escolhido.

O gerador usa `fpdf2` para produzir um layout de duas colunas: uma barra lateral azul-marinho escuro (30%) com informacoes pessoais, foto, objetivo e contato, e uma area principal branca (70%) com as quatro secoes de conteudo. Todo o texto da area principal e quase preto sobre branco para maxima legibilidade ATS.

### Mudar o idioma

Edite `cv_lang.json` e defina o campo `"lang"` como `"fr"`, `"en"`, `"es"` ou `"pt"`. Isso muda os titulos de secao, o titulo do quadro Objetivo e o subtexto do rodape. O conteudo em si (descricoes, titulos) deve ser traduzido manualmente em `cv_data.json`.

### Mudar a ordem das secoes

Adicione uma chave `"section_order"` ao `cv_data.json` (ordem padrao mostrada):

```json
"section_order": ["formations", "experiences", "skills", "certifications"]
```

### Descricoes e marcadores

As descricoes aceitam um formato hibrido -- uma frase de contexto seguida de marcadores. Linhas comecando com `-` sao renderizadas com marcadores coloridos e indentacao adequada:

```json
"description": "Frase de contexto sobre o cargo.\n- Primeira realizacao ou responsabilidade\n- Segunda realizacao com resultados quantificados"
```

### Selos de certificacao

Coloque a imagem do selo (ex. baixada do Credly) em `badges/`, depois referencie-a na entrada de certificacao -- a imagem e o pequeno icone de link sao clicaveis quando `url` esta definido:

```json
{ "name": "IT Essentials", "issuer": "Cisco", "date": "2021",
  "url": "https://www.credly.com/...", "image": "badges/it_essentials.png" }
```

### Fontes personalizadas

Adicione arquivos TTF/OTF e referencie-os no estilo (indispensavel para alfabetos nao latinos):

```json
"fonts": {
  "heading": "MinhaFonte",
  "body": "MinhaFonte",
  "custom": {
    "MinhaFonte": { "": "fonts/MinhaFonte-Regular.ttf", "B": "fonts/MinhaFonte-Bold.ttf", "I": "fonts/MinhaFonte-Italic.ttf" }
  }
}
```

### Tudo o que o `cv_style.json` controla

- **Barra lateral**: proporcao de largura, cor de fundo, padding, tamanho da foto
- **Fontes**: familias de titulo/corpo, fontes TTF/OTF personalizadas
- **Tamanhos de fonte**: cada elemento de texto tem seu proprio tamanho configuravel
- **Cores**: cada elemento tem sua propria cor RGB
- **Espacamentos**: intervalos entre secoes, proporcao de altura de linha
- **Selos**: padding, raio, intervalo, cores por estilo (preenchido/contorno/acento)
- **Secao de competencias**: tamanhos de selos, cores por categoria
- **Certificacoes**: tamanho de imagem, grade, colunas
- **Quadro objetivo**: fundo, borda, cor do titulo, cor do texto, padding, raio
- **Rodape**: textos, tamanho de fonte, cor, icones, URLs de link e imagem

## Estrutura de arquivos

| Arquivo | Funcao |
| --- | --- |
| `generate_cv.py` | Gerador de PDF (linha de comando) |
| `cv_gui.py` | Aplicativo de desktop (interface de formulario sobre o gerador) |
| `cv_data.json` / `cv_data_fr.json` | Conteudo do CV (versao inglesa / francesa) |
| `cv_style.json` | Parametros visuais (fontes, tamanhos, cores, espacamentos, selos, rodape) |
| `cv_lang.json` | Rotulos de idioma para titulos de secao e rodape |
| `fonts/` | Arquivos OTF do Font Awesome 7 para os icones |
| `badges/` | Imagens de selos de certificacao (Credly) |
| `whale.png` / `app_icon.png` / `whale.ico` | Mascote do rodape, icone da janela, icone do exe |
| `release_readme.md` | Guia do usuario incluido nos pacotes de release |
| `.github/workflows/build-release.yml` | Compilacoes CI para Windows, Linux e macOS |
| `requirements.txt` | Dependencias Python (`fpdf2`, `pillow`) |

## Pesquisa de design

### Paleta de cores

A paleta foi escolhida com base em pesquisas de fontes do setor de curriculos sobre o que funciona melhor tanto com recrutadores humanos quanto com ferramentas de triagem ATS/IA.

**Por que azul-marinho?**

- O azul e a cor de CV n1 recomendada por todas as fontes -- transmite confianca, fiabilidade e competencia
- Especialmente adequado para tech/TI ja que a maioria das grandes empresas de tecnologia usa branding azul
- O azul-marinho escuro dos titulos (`#003366`) alcancou uma **taxa de deteccao de palavras-chave ATS de 98%** nos testes

| Elemento           | Hex       | Justificativa                                       |
| ------------------ | --------- | --------------------------------------------------- |
| Fundo barra lateral | `#1B2A4A` | Razao de contraste com texto branco: ~12.5:1 (WCAG AAA) |
| Titulos de secao   | `#003366` | Taxa de deteccao ATS de 98%                         |
| Titulos de itens   | `#0476D0` | Recomendado para CVs tech/TI                        |
| Texto principal    | `#212121` | Contraste com branco: ~16:1 (WCAG AAA)              |
| Texto secundario   | `#555555` | Contraste com branco: ~7.5:1 (WCAG AA)              |

### Regras de compatibilidade ATS

1. O texto principal e quase preto sobre branco -- a "Regra 90-10"
2. Todas as palavras-chave criticas estao na area branca principal, nao na barra lateral
3. Razoes de contraste altas (minimo 4.5:1 conforme WCAG AA) em cada par texto-fundo
4. Paleta coesa de 2 cores (marinho + acento azul) mais neutros
5. Fontes padrao (Helvetica) -- universalmente analisaveis por ATS

### Formatacao das descricoes

As descricoes seguem as boas praticas de CV academico para candidaturas a mestrado:

- Formato hibrido: uma frase de contexto + marcadores
- Verbos de acao no infinitivo (convencao francesa)
- Realizacoes quantificadas sempre que possivel
- Palavras-chave refletindo as descricoes dos programas-alvo

## Rodape

O rodape na parte inferior da barra lateral mostra uma linha de texto com icones decorativos e um link clicavel para este repositorio.

**Texto dinamico:** Quando o nome do CV e "Gabriel Verite" (o autor), o rodape mostra *"Generateur de CV de ma conception"*. Para qualquer outro nome, muda automaticamente para *"generated with CV Generator by In Veritas"*, onde **In Veritas** e um link clicavel para minha pagina do GitHub. Configuravel via `text`, `text_other`, `text_other_link_text` e `text_other_link_url` no `cv_style.json`.

**Subtexto localizado:** a linha abaixo ("disponivel em codigo aberto") segue o idioma do CV atraves da chave `footer_sub` do `cv_lang.json`.

**Datas de certificacao:** Cada entrada de certificacao aceita um campo opcional `"date"` mostrado em texto pequeno italico abaixo do emissor.

### Icone de baleia

A pequena baleia ao lado do link do rodape e um toque pessoal -- e meu animal favorito. E puramente decorativa e nao afeta a analise ATS (fica na barra lateral, fora da area de conteudo principal). A mesma baleia e o icone de janela do aplicativo (`app_icon.png`) e, dentro do aplicativo, uma mascote clicavel que abre minha pagina do GitHub.

Para remove-la do CV, esvazie o campo `image_right` no `cv_style.json`:

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
