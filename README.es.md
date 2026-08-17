# CV Generator

**[English](README.md)** | **[Français](README.fr.md)** | **[Português](README.pt.md)**

Cree un CV PDF profesional de dos columnas, atractivo para reclutadores y compatible con ATS — ya sea con una **aplicacion de escritorio** (rellene un formulario, elija sus colores, pulse Generar) o **manualmente** con Python y archivos de configuracion JSON. Disenado para atraer a reclutadores, compatible con ATS (Applicant Tracking System) y optimizado para admisiones academicas.

## Vista previa

![Vista previa del CV](cv_preview.png)

> **Nota:** Este mismo CV me consiguio una plaza en mi nuevo master -- lo cual es genial.

## Para que sirve

- **Candidaturas a master** (MonMaster, expedientes universitarios) -- optimizado para comisiones de admision academica francesas
- **Candidaturas de empleo** -- diseno compatible con ATS con alta tasa de deteccion de palabras clave
- **Perfiles freelance / profesionales** -- diseno limpio y moderno con enlaces clicables
- **CVs multilingues** -- alterne entre frances, ingles, espanol y portugues con un solo clic

## Dos formas de usarlo

| | Aplicacion de escritorio (release) | Manual (Python + JSON) |
| --- | --- | --- |
| Para | Todos -- sin conocimientos tecnicos | Quienes quieren ajustarlo todo |
| Requiere | Nada en Windows/Linux; Python en macOS | Python 3.9+ |
| Controla | Contenido, foto, colores, tamanos, orden de secciones, insignias | Todo eso mas cada parametro de estilo avanzado |

## Usar la aplicacion de escritorio (recomendado)

### Obtenerla

Descargue el paquete mas reciente desde la [pagina de Releases](https://github.com/In-Veritas/cv-generator/releases) y descomprimalo:

- **Windows** (`…-win64.zip`): haga doble clic en `CV-Generator.exe`. Si SmartScreen muestra "Windows protegio su PC", pulse *Mas informacion* → *Ejecutar de todas formas* (el exe simplemente no esta firmado digitalmente).
- **Linux** (`…-linux-x64.tar.gz`): ejecute `chmod +x CV-Generator && ./CV-Generator` desde la carpeta descomprimida.
- **macOS / cualquier OS** (`…-source.zip`): instale Python 3.9+, luego `pip3 install -r requirements.txt` y `python3 cv_gui.py`.

Mantenga los archivos descomprimidos juntos -- la aplicacion lee `fonts/`, `cv_style.json`, `whale.png` y `app_icon.png` desde su propia carpeta.

### Usarla

1. **Elija un idioma** -- Francais, English, Espanol o Portugues. Define la interfaz y los titulos de seccion impresos en el PDF, y se cambia en cualquier momento desde el menu *Idioma*.
2. **Rellene las pestanas.** Cada cuadro de texto muestra una instruccion gris explicando que escribir. En las pestanas de listas (Formacion, Experiencia, Competencias, Certificaciones), pulse *Anadir* para crear una entrada; seleccione una entrada para editarla -- los cambios se guardan automaticamente mientras escribe.
3. **Elija el orden de las secciones.** Arrastre las pestanas de secciones para reordenarlas -- el PDF imprime sus secciones en ese orden exacto. El menu *Preajustes* ofrece **Profesional** (Experiencia primero -- el predeterminado) y **Academico** (Formacion primero).
4. **De estilo.** La pestana *Estilo* tiene selectores de colores y tamanos, mas un boton *Importar estilo JSON…* que carga un `cv_style.json` completo (vea la seccion manual mas abajo para todo lo que puede contener).
5. **Anada insignias de certificacion.** La pestana Certificaciones tiene un boton *Ayuda* con una guia paso a paso y una herramienta *Generar insignia…* que recorta cualquier imagen en cuadrado y la ajusta a 300×300 px.
6. **Genere.** La aplicacion comprueba los campos que los ATS y las herramientas de IA de los reclutadores suelen analizar (nombre, contacto, objetivo, entradas, competencias, fechas) y le avisa si estan vacios -- luego produce el PDF donde usted elija.

Consejos: **Archivo → Guardar datos del CV (.json)** mantiene su trabajo reutilizable (el archivo es totalmente compatible con el generador de linea de comandos de abajo), y la pequena ballena de la esquina inferior izquierda abre mi pagina de GitHub.

El manual completo de la aplicacion -- con solucion de problemas -- se incluye en cada paquete y tambien puede leerse aqui: [release_readme.md](release_readme.md).

### Compilar la aplicacion usted mismo

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name CV-Generator --icon whale.ico cv_gui.py
```

Un workflow de GitHub Actions (`.github/workflows/build-release.yml`) compila automaticamente los paquetes de Windows, Linux y macOS bajo demanda o al empujar una etiqueta `v*`.

## Uso manual (Python + JSON)

Para un control total, use el generador directamente y edite los archivos JSON a mano.

```bash
pip install -r requirements.txt
python generate_cv.py
```

### Opciones

```bash
python generate_cv.py --data cv_data.json --style cv_style.json --lang cv_lang.json -o output.pdf
```

| Opcion    | Por defecto     | Descripcion                          |
| --------- | --------------- | ------------------------------------ |
| `--data`  | `cv_data.json`  | Ruta al contenido del CV             |
| `--style` | `cv_style.json` | Ruta a la configuracion visual       |
| `--lang`  | `cv_lang.json`  | Ruta a las etiquetas de idioma       |
| `-o`      | `cv_output.pdf` | Ruta del PDF de salida               |

### Los tres archivos JSON

1. **`cv_data.json`** -- Su contenido (quien es usted, que ha hecho). `cv_data_fr.json` es la version francesa de mis propios datos, usable con `--data`.
2. **`cv_style.json`** -- La apariencia (colores, fuentes, tamanos, espaciados).
3. **`cv_lang.json`** -- Las etiquetas de seccion y el subtexto del pie de pagina en el idioma elegido.

El generador usa `fpdf2` para producir un diseno de dos columnas: una barra lateral azul marino oscuro (30%) con informacion personal, foto, objetivo y contacto, y un area principal blanca (70%) con las cuatro secciones de contenido. Todo el texto del area principal es casi negro sobre blanco para maxima legibilidad ATS.

### Cambiar el idioma

Edite `cv_lang.json` y ponga el campo `"lang"` en `"fr"`, `"en"`, `"es"` o `"pt"`. Esto cambia los titulos de seccion, el titulo del recuadro Objetivo y el subtexto del pie de pagina. El contenido en si (descripciones, titulos) debe traducirse manualmente en `cv_data.json`.

### Cambiar el orden de las secciones

Anada una clave `"section_order"` a `cv_data.json` (se muestra el orden por defecto):

```json
"section_order": ["formations", "experiences", "skills", "certifications"]
```

### Descripciones y vinetas

Las descripciones admiten un formato hibrido -- una frase de contexto seguida de vinetas. Las lineas que empiezan por `-` se muestran con marcadores de color e indentacion adecuada:

```json
"description": "Frase de contexto sobre el puesto.\n- Primer logro o responsabilidad\n- Segundo logro con resultados cuantificados"
```

### Insignias de certificacion

Coloque la imagen de la insignia (ej. descargada de Credly) en `badges/`, luego referenciela en la entrada de certificacion -- la imagen y el pequeno icono de enlace son clicables cuando `url` esta definido:

```json
{ "name": "IT Essentials", "issuer": "Cisco", "date": "2021",
  "url": "https://www.credly.com/...", "image": "badges/it_essentials.png" }
```

### Fuentes personalizadas

Anada archivos TTF/OTF y referencielos en el estilo (imprescindible para alfabetos no latinos):

```json
"fonts": {
  "heading": "MiFuente",
  "body": "MiFuente",
  "custom": {
    "MiFuente": { "": "fonts/MiFuente-Regular.ttf", "B": "fonts/MiFuente-Bold.ttf", "I": "fonts/MiFuente-Italic.ttf" }
  }
}
```

### Todo lo que controla `cv_style.json`

- **Barra lateral**: ratio de anchura, color de fondo, padding, tamano de foto
- **Fuentes**: familias de titulo/cuerpo, fuentes TTF/OTF personalizadas
- **Tamanos de fuente**: cada elemento de texto tiene su propio tamano configurable
- **Colores**: cada elemento tiene su propio color RGB
- **Espaciados**: separaciones entre secciones, ratio de altura de linea
- **Insignias**: padding, radio, separacion, colores por estilo (relleno/contorno/acento)
- **Seccion de competencias**: tamanos de insignias, colores por categoria
- **Certificaciones**: tamano de imagen, cuadricula, columnas
- **Recuadro objetivo**: fondo, borde, color del titulo, color del texto, padding, radio
- **Pie de pagina**: textos, tamano de fuente, color, iconos, URLs de enlace e imagen

## Estructura de archivos

| Archivo | Proposito |
| --- | --- |
| `generate_cv.py` | Generador de PDF (linea de comandos) |
| `cv_gui.py` | Aplicacion de escritorio (interfaz de formulario sobre el generador) |
| `cv_data.json` / `cv_data_fr.json` | Contenido del CV (version inglesa / francesa) |
| `cv_style.json` | Parametros visuales (fuentes, tamanos, colores, espaciados, insignias, pie) |
| `cv_lang.json` | Etiquetas de idioma para titulos de seccion y pie de pagina |
| `fonts/` | Archivos OTF de Font Awesome 7 para los iconos |
| `badges/` | Imagenes de insignias de certificacion (Credly) |
| `whale.png` / `app_icon.png` / `whale.ico` | Mascota del pie, icono de ventana, icono del exe |
| `release_readme.md` | Guia de usuario incluida en los paquetes de release |
| `.github/workflows/build-release.yml` | Compilaciones CI para Windows, Linux y macOS |
| `requirements.txt` | Dependencias de Python (`fpdf2`, `pillow`) |

## Investigacion de diseno

### Paleta de colores

La paleta se eligio basandose en investigaciones de fuentes del sector de los curriculos sobre lo que mejor funciona tanto con reclutadores humanos como con herramientas de cribado ATS/IA.

**Por que azul marino?**

- El azul es el color de CV n1 recomendado por todas las fuentes -- transmite confianza, fiabilidad y competencia
- Especialmente adecuado para tech/IT ya que la mayoria de las grandes tecnologicas usan branding azul
- El azul marino oscuro de los titulos (`#003366`) alcanzo una **tasa de deteccion de palabras clave ATS del 98%** en pruebas

| Elemento           | Hex       | Justificacion                                       |
| ------------------ | --------- | --------------------------------------------------- |
| Fondo barra lateral | `#1B2A4A` | Ratio de contraste con texto blanco: ~12.5:1 (WCAG AAA) |
| Titulos de seccion | `#003366` | Tasa de deteccion ATS del 98%                       |
| Titulos de elementos | `#0476D0` | Recomendado para CVs tech/IT                       |
| Texto principal    | `#212121` | Contraste con blanco: ~16:1 (WCAG AAA)              |
| Texto secundario   | `#555555` | Contraste con blanco: ~7.5:1 (WCAG AA)              |

### Reglas de compatibilidad ATS

1. El texto principal es casi negro sobre blanco -- la "Regla 90-10"
2. Todas las palabras clave criticas estan en el area blanca principal, no en la barra lateral
3. Ratios de contraste altos (minimo 4.5:1 segun WCAG AA) en cada par texto-fondo
4. Paleta cohesiva de 2 colores (marino + acento azul) mas neutros
5. Fuentes estandar (Helvetica) -- universalmente analizables por ATS

### Formato de las descripciones

Las descripciones siguen las buenas practicas de CV academico para candidaturas a master:

- Formato hibrido: una frase de contexto + vinetas
- Verbos de accion en infinitivo (convencion francesa)
- Logros cuantificados siempre que sea posible
- Palabras clave que reflejan las descripciones de los programas objetivo

## Pie de pagina

El pie de pagina en la parte inferior de la barra lateral muestra una linea de texto con iconos decorativos y un enlace clicable a este repositorio.

**Texto dinamico:** Cuando el nombre del CV es "Gabriel Verite" (el autor), el pie muestra *"Generateur de CV de ma conception"*. Para cualquier otro nombre, cambia automaticamente a *"generated with CV Generator by In Veritas"*, donde **In Veritas** es un enlace clicable a mi pagina de GitHub. Configurable via `text`, `text_other`, `text_other_link_text` y `text_other_link_url` en `cv_style.json`.

**Subtexto localizado:** la linea inferior ("disponible en codigo abierto") sigue el idioma del CV mediante la clave `footer_sub` de `cv_lang.json`.

**Fechas de certificacion:** Cada entrada de certificacion admite un campo opcional `"date"` mostrado en pequeno texto italico bajo el emisor.

### Icono de ballena

La pequena ballena junto al enlace del pie es un toque personal -- es mi animal favorito. Es puramente decorativa y no afecta al analisis ATS (esta en la barra lateral, fuera del area de contenido principal). La misma ballena es el icono de ventana de la aplicacion (`app_icon.png`) y, dentro de la aplicacion, una mascota clicable que abre mi pagina de GitHub.

Para quitarla del CV, vacie el campo `image_right` en `cv_style.json`:

```json
"footer": {
  "image_right": "",
  ...
}
```

## Atribucion

- <a href="https://www.flaticon.com/free-icons/whale" title="whale icons">Whale icons created by Mayor Icons - Flaticon</a>

## Fuentes

- [Resumly - Resume Color Scheme for ATS Compatibility & Readability](https://www.resumly.ai/blog/resume-color-scheme-for-ats-compatibility-and-readability)
- [AI ResumeGuru - Resume Colors: ATS-Safe Guide](https://airesume.guru/blog/resume-color-ats-safe-tips)
- [Resume.io - Best colors for a resume](https://resume.io/blog/should-you-use-color-on-your-resume)
- [Enhancv - How Does Color on a Resume Impact Your Chances?](https://enhancv.com/blog/color-on-resume/)
- [Jobscan - Should You Use Color on Your Resume?](https://www.jobscan.co/blog/best-color-for-resume/)
- [WebAIM - Contrast and Color Accessibility (WCAG 2)](https://webaim.org/articles/contrast/)
- [Mastersportal - 6 Steps to Writing an Awesome Academic CV](https://www.mastersportal.com/articles/2626/6-steps-to-writing-an-awesome-academic-cv-for-masters-application.html)
- [MakeMyCV - CV Master : Les cles pour seduire le jury](https://makemycv.com/fr/cv-master)
