# CV Generator

Un script en Python que genera un CV profesional en PDF de dos columnas a partir de archivos de configuracion JSON. Disenado para atraer a reclutadores, compatible con ATS (Applicant Tracking System) y optimizado para admisiones academicas. Cada aspecto es configurable mediante parametros. Los principiantes pueden simplemente modificar el archivo `cv_data.json`, mientras que los usuarios avanzados pueden intervenir en `cv_style.json` o directamente en `generate_cv.py` para ajustes mas refinados. Un tutorial esta disponible a continuacion. Tambien puede cambiar el idioma del CV usando `cv_lang.json`, pero se recomienda una revision manual del texto traducido.

## Vista previa

![Vista previa del CV](cv_preview.png)

## Para que sirve

- **Candidaturas a master** (MonMaster, expedientes universitarios) -- optimizado para comisiones de admision academica francesas
- **Candidaturas de empleo** -- diseno compatible con ATS con alta tasa de deteccion de palabras clave
- **Perfiles freelance / profesionales** -- diseno limpio y moderno con enlaces clicables
- **CVs multilingues** -- alterne entre frances, ingles, espanol y portugues con un solo cambio de configuracion

## Como funciona

El generador lee tres archivos JSON y produce un PDF A4 de una pagina:

1. **`cv_data.json`** -- Su contenido (quien es usted, que ha hecho)
2. **`cv_style.json`** -- La apariencia (colores, fuentes, tamanos, espaciados)
3. **`cv_lang.json`** -- Etiquetas de seccion en el idioma elegido

El script usa `fpdf2` para renderizar un diseno de dos columnas: una barra lateral azul marino oscuro (30%) con informacion personal, foto, objetivo y datos de contacto, y un area principal blanca (70%) con formaciones, experiencias, competencias y certificaciones. Todo el texto en el area principal es casi negro sobre blanco para maxima legibilidad ATS.

Las descripciones admiten listas con vinetas: las lineas que comienzan con `-` se renderizan automaticamente con marcadores de color e indentacion.

## Uso

```bash
pip install -r requirements.txt
python generate_cv.py
```

### Opciones

```bash
python generate_cv.py --data cv_data.json --style cv_style.json --lang cv_lang.json -o output.pdf
```

| Opcion    | Defecto         | Descripcion                             |
| --------- | --------------- | --------------------------------------- |
| `--data`  | `cv_data.json`  | Ruta al contenido del CV                |
| `--style` | `cv_style.json` | Ruta a la configuracion visual          |
| `--lang`  | `cv_lang.json`  | Ruta a las etiquetas de idioma          |
| `-o`      | `cv_output.pdf` | Ruta del PDF de salida                  |

### Cambiar el idioma

Edite `cv_lang.json` y modifique el campo `"lang"`:

```json
{
  "lang": "es"
}
```

Disponible: `"fr"` (frances), `"en"` (ingles), `"es"` (espanol), `"pt"` (portugues).

Esto cambia los titulos de seccion (Formacion, Experiencia, Competencias, Certificaciones) y el titulo del recuadro Objetivo. El contenido en si (descripciones, titulos) debe traducirse manualmente en `cv_data.json`.

## Estructura de archivos

| Archivo            | Funcion                                                                        |
| ------------------ | ------------------------------------------------------------------------------ |
| `generate_cv.py`   | Script principal del generador (~800 lineas)                                   |
| `cv_data.json`     | Contenido del CV (infos personales, formaciones, experiencias, competencias, certificaciones) |
| `cv_style.json`    | Parametros visuales (fuentes, tamanos, colores, espaciados, badges, pie de pagina) |
| `cv_lang.json`     | Etiquetas de idioma para titulos de seccion                                    |
| `fonts/`           | Archivos OTF Font Awesome 7 para iconos                                       |
| `badges/`          | Imagenes de badges de certificacion (Credly)                                   |
| `requirements.txt` | Dependencias Python (`fpdf2`)                                                  |

## Funcionalidades

### Diseno de dos columnas

El diseno barra lateral (30%) + contenido principal (70%) es uno de los formatos de CV modernos mas populares:

- La barra lateral agrupa la informacion personal/contacto separada del contenido profesional
- Los reclutadores pueden localizar rapidamente los datos de contacto
- El area principal ofrece amplio espacio para descripciones de experiencia
- Los sistemas ATS pueden analizar el area de contenido principal de manera fiable

### Iconos Font Awesome

El generador detecta automaticamente archivos OTF/TTF Font Awesome en el directorio `fonts/`:

- **Enlaces sociales** (GitHub, LinkedIn) -- fuente `fa-brands`
- **Marcadores de contacto** (email, telefono, direccion) -- fuente `fa-solid`
- **Enlaces de certificacion** -- icono de enlace clicable junto a cada nombre
- **Decoraciones del pie de pagina** -- iconos izquierda/derecha configurables

Retorno gracioso a renderizacion solo texto si las fuentes no estan presentes.

### Badges de certificacion

Cada certificacion puede mostrar su imagen de badge oficial (ej. Credly) junto al nombre y emisor. Las imagenes de badge son clicables y enlazan a la pagina de la certificacion.

### Formato de listas con vinetas

Las descripciones admiten un formato hibrido -- una frase de contexto seguida de vinetas:

```json
"description": "Frase de contexto sobre el puesto.\n- Primer logro o responsabilidad\n- Segundo logro con resultados cuantificados\n- Tercer punto"
```

Las lineas que comienzan con `-` se renderizan con marcadores de color e indentacion apropiada.

### Soporte de foto

Soporta formatos JPG, JPEG, PNG, BMP y GIF. Si no se encuentra el nombre exacto del archivo, el generador prueba automaticamente extensiones comunes.

### Badges de competencias coloreados

La seccion de competencias usa badges pilula coloreados agrupados por categoria, cada uno con un color distinto de la familia de azules para coherencia visual.

## Personalizacion

### Cambiar el contenido

Edite `cv_data.json`:

- `personal`: nombre, titulo, foto, objetivo, acerca de, datos de contacto, enlaces sociales
- `formations`: entradas de formacion con descripciones en lista
- `experiences`: entradas de experiencia con descripciones en lista
- `skills_section`: badges de competencias por categoria (idiomas, programacion, herramientas, soft skills)
- `certifications`: entradas de certificacion con URLs e imagenes de badge opcionales

### Cambiar el estilo

Edite `cv_style.json` para ajustar cualquier parametro visual:

- **Barra lateral**: ratio de ancho, color de fondo, padding, tamano de foto
- **Fuentes**: familias titulo/cuerpo, fuentes TTF/OTF personalizadas
- **Tamanos de fuente**: cada elemento de texto tiene su propio tamano configurable
- **Colores**: cada elemento tiene su propio color RGB
- **Espaciados**: gaps entre cada seccion, ratio de altura de linea
- **Badges**: padding, radio, gap, colores por estilo (relleno/contorno/acento)
- **Seccion de competencias**: tamanos de badges, colores por categoria
- **Certificaciones**: tamano de imagen, cuadricula, columnas
- **Recuadro de objetivo**: fondo, borde, color del titulo, color del texto, padding, radio
- **Pie de pagina**: texto, tamano de fuente, color, iconos, URL de enlace e imagen opcionales

### Usar fuentes personalizadas

Anada archivos TTF/OTF y referencialos en el estilo:

```json
"fonts": {
  "heading": "MiFuente",
  "body": "MiFuente",
  "custom": {
    "MiFuente": {
      "": "fonts/MiFuente-Regular.ttf",
      "B": "fonts/MiFuente-Bold.ttf",
      "I": "fonts/MiFuente-Italic.ttf"
    }
  }
}
```

## Investigacion de diseno

### Paleta de colores

La paleta fue elegida basandose en investigaciones de fuentes del sector de reclutamiento sobre lo que funciona mejor con reclutadores humanos y herramientas de seleccion ATS/IA.

**Por que azul marino?**

- El azul es el color de CV n1 recomendado por todas las fuentes -- transmite confianza, fiabilidad y competencia
- Especialmente adecuado para tech/TI ya que la mayoria de las grandes empresas tecnologicas usan azul en su branding
- El color azul marino oscuro para titulos (`#003366`) alcanzo una **tasa de deteccion de palabras clave ATS del 98%** en las pruebas

| Elemento             | Hex       | Justificacion                                         |
| -------------------- | --------- | ----------------------------------------------------- |
| Fondo barra lateral  | `#1B2A4A` | Ratio de contraste con texto blanco: ~12.5:1 (WCAG AAA) |
| Titulos de seccion   | `#003366` | Tasa de deteccion ATS del 98%                         |
| Titulos de elementos | `#0476D0` | Recomendado para CVs tech/TI                          |
| Texto principal      | `#212121` | Contraste con blanco: ~16:1 (WCAG AAA)                |
| Texto secundario     | `#555555` | Contraste con blanco: ~7.5:1 (WCAG AA)                |

### Reglas de compatibilidad ATS

1. El texto principal es casi negro sobre blanco -- la "Regla 90-10"
2. Todas las palabras clave criticas estan en el area blanca principal, no en la barra lateral
3. Ratios de contraste elevados (minimo 4.5:1 segun WCAG AA) en cada combinacion texto-fondo
4. Paleta coherente de 2 colores (marino + acento azul) mas neutros
5. Fuentes estandar (Helvetica) -- universalmente analizables por ATS

## Pie de pagina

El pie de pagina en la parte inferior de la barra lateral muestra una linea de texto con iconos decorativos y un enlace clicable al repositorio.

**Texto dinamico:** Cuando el nombre en el CV es "Gabriel Verite" (el autor), el pie de pagina muestra *"Generateur de CV developpe par mes soins"*. Para cualquier otro nombre, cambia automaticamente a *"CV generated with In:Veritas CV Generator"*. Ambos textos son configurables via `text` y `text_other` en `cv_style.json`.

**Fechas de certificacion:** Cada entrada de certificacion admite un campo opcional `"date"` mostrado en texto cursiva pequeno debajo del emisor.

### Icono de ballena

El pequeno icono de ballena junto al enlace del pie de pagina es un toque personal -- es mi animal favorito. Es puramente decorativo y no tiene impacto en el analisis ATS (esta en la barra lateral, fuera del area de contenido principal).

Para eliminarlo, vacia el campo `image_right` en `cv_style.json`:

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
