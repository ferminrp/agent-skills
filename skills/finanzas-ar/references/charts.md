# Gráficos para X — guía (borrador)

Objetivo: un PNG que se entienda en 3 segundos en el celular, con datos reales, fuente y hora BA.

## 1. Lienzo
- **Horizontal 1600×900 (16:9)** por defecto: X lo muestra completo en el timeline, sin recorte. (`xchart.figure(size="landscape")`, 8×4.5 in @200 dpi.)
- **Vertical 1080×1350 (4:5)** para rankings o tablas largas: ocupa más pantalla en mobile (`size="vertical"`).
- Cuadrado 1200×1200 sólo si hace falta.
- Exportar **PNG** (no JPG: el texto se ensucia). Márgenes ≥ 4 % por lado; nada importante en el borde.

## 2. Jerarquía (de arriba hacia abajo)
1. **Título = la conclusión**, no el tema. "YPF y Pampa se mueven juntas: r = 0.71", no "Correlación YPF-PAMP". Máx. ~45 caracteres, bold 17 pt.
2. **Subtítulo** gris: qué se mide, unidad y período ("Retornos diarios ADR · 04/11/2025–04/11/2026, 252 ruedas").
3. Gráfico.
4. **Footer**: izquierda `Fuente: <fuente> · datos al <dd/mm/aaaa hh:mm> hora BA` (+ supuestos clave en ≤ 1 línea); derecha el handle del usuario (si lo dio) en bold.
Jerarquía por peso + tamaño + color, no sólo tamaño.

## 3. Tipografía
- Sans moderna con pesos estáticos: **Pretendard** (en el box); fallback DejaVu Sans. Nada de fuentes variables en matplotlib (ignora el peso).
- Tamaños a 1600 px (v2): título 18 pt, número grande 30, subtítulo 12, ejes 12–12.5, etiquetas 11.5, footer 9.5. A 390 px el footer queda chico (≈6 px): es aceptable porque se lee al abrir la imagen; todo lo demás tiene que leerse sin abrirla.
- Números con el mismo formato en todo el gráfico (1 decimal para %, 2 para r).

## 4. Color
- **Siempre modo claro**. `theme="light"` es el default y el único recomendado; `dark` queda en el código sólo como legado.
- **Grises + UN acento** (stageshow): una familia de grises fríos; el acento azul `#1663D6` sólo en lo que cuenta la historia (regresión, ley local + brecha, número grande).
- Suelo `#F3F4F6` → panel `#FFFFFF` → superficie elevada `#F5F6F8` (satélite). Grilla `#E8EAED`, ejes de referencia `#C9CDD3`.
- Texto: `#111827` (título), `#4B5563` (subtítulo/etiquetas), `#6B7280` (ticks, footer, serie secundaria). El gris más claro usado para texto es `#6B7280` ≈ 4.8:1 sobre blanco (pasa AA); nada de texto en `#C9CDD3` o más claro.
- Verde/rojo sólo si significan sube/baja.

## 5. Datos-tinta
- **Etiquetas directas** junto a la serie/punto en lugar de leyenda.
- Grilla horizontal tenue, sin bordes arriba/derecha/izquierda, sin ticks.
- Anotar el último valor o el dato clave (ej. "0.69" al final de la correlación móvil).
- Eje Y con unidad en los ticks (`12%`), no en un label aparte cuando se pueda.
- Evitar superposición de etiquetas: mover con `dx/dy` o cambiar el eje (ej. vencimiento en lugar de duration si los puntos se amontonan).

## 6. Honestidad
- Sólo datos reales de la skill finanzas-ar; si un número se calcula (TIR, r), decirlo en el footer ("TIR propia").
- Indicar convención (TIR efectiva anual vs S.A.), especie (D/C), rueda en curso, fallbacks.
- Ejes Y que empiezan en 0 cuando el gráfico es de barras; en líneas/scatter, rango ajustado está bien.

## 7. Checklist antes de publicar
- [ ] ¿El título dice la conclusión? [ ] ¿Período en el subtítulo? [ ] ¿Fuente + hora BA?
- [ ] ¿`phone_sheet` a 390 px: título y número grande se leen? [ ] ¿Un solo acento? [ ] ¿El número clave aparece una sola vez? [ ] ¿Sin etiquetas pisadas? [ ] ¿Handle (si hay)?

## 8. Lecciones de stageshow (Benji Taylor) aplicadas a gráficos estáticos
Basado en la skill stageshow de Benji Taylor, MIT (SKILL.md, references/craft.md, framing.md, looks.md, verify.md, rehearse.md, teaching.md; ejemplos dark-hero, dark-bento, chart-scrub, static-card).
- **Decilo una vez** (craft "Say it once", dark-bento): r aparece sólo en el número grande, no en título + etiqueta + subtítulo. El título queda para la frase.
- **Un número es grande, el resto son líneas** (craft "One number gets to be big"; chart-scrub `.cs-value` 30px/600 con tracking negativo): `stat()` arriba a la derecha.
- **Un acento sobre grises callados** (dark-hero "one lit color"; looks "cinco tintas y un acento"): puntos de scatter y ley NY en gris medio (`#6B7280`), no gris oscuro, para que pesen menos que el acento; el azul sólo en la señal.
- **Lo más pesado va sobre lo que importa** (craft): línea de regresión 2.6 px en acento; nubes y grillas finas y oscuras.
- **Palabras reales sólo en la historia** (craft "Count the real strings", 3–7): etiquetas sólo con ticker; el valor lo da el eje. Sin β ni leyenda ni texto redundante.
- **Profundidad por escalones de superficie, no sombras** (craft, dark-hero; adaptado a claro con craft "The light inks are tuned for white cards on gray canvas"): suelo gris muy claro → panel blanco → satélite en gris apenas más oscuro que el blanco. Sin sombras ni bordes (craft "No redundant tonal borders").
- **Un héroe + como mucho un satélite** de otro tipo (framing 1, 17; static-card): scatter = héroe, móvil = satélite chico.
- **Un solo gutter** en todos los bordes (framing 10–11) y **sin esquinas muertas** (framing 15): el número grande llena la esquina superior derecha, el satélite la inferior derecha.
- **Póster** (motion "the poster is the frame most people see"): la imagen tiene que contar la historia sola, en miniatura.
- **Modos de falla** (SKILL.md): *too much* (números por todos lados → v1 tenía TIR en cada etiqueta), *flat* (todo con el mismo peso → v1 tenía azul y ámbar al mismo nivel), *boxed* (gráfico achicado con márgenes parejos), *bland* (gris sin energía; el acento y el número grande lo evitan).
- **Silueta antes que detalle + revisión a ancho de celular** (craft "Judge the silhouette"; verify/rehearse `--width 390`, contact sheet): `phone_sheet()` arma una hoja a 390 px; ahí se decide.
- **Quiet is not faint** (craft): los grises secundarios se chequean contra el suelo real; nada por debajo de `ink3` para texto.
- **Arreglar la falla más grande primero** (verify): encuadre → jerarquía → pulido.
**No aplican a estáticos:** todo motion.md/choreography (springs, entradas, loops, "dibujar el chart de izquierda a derecha", scrub con hairline), cursores, crop/bleed de ventanas y dispositivos (un gráfico no se recorta: cortar datos miente), satélites a caballo del borde del héroe, chrome/íconos/avatares, `compact` como rediseño responsive (X no tiene breakpoints; sí se puede hacer una versión 4:5 aparte), herramientas film.mjs/--gate (las reemplaza `phone_sheet` + mirar la imagen).

## Helper
`xchart.py` (v2; v1 en `xchart_v1.py`): `figure(theme, size, plot_box)` → `(fig, ax)` con suelo + panel; `stat(fig, valor, caption)` número grande; `phone_sheet(paths, out, 390)` preview celular; `label(ax, x, y, texto)` para etiquetas directas; `finish(fig, ax, title, subtitle, source, out)` agrega título, subtítulo, footer y handle y guarda el PNG.
Ejemplos v3 (claro): `corr_v3.py` → `correlacion-ypf-pampa-v3.png`, `curva_v3.py` → `curva-soberanos-v3.png`, `phone-preview-v3.png`. v2 (oscuro): `corr_v2.py` → `correlacion-ypf-pampa-v2.png`, `curva_v2.py` → `curva-soberanos-v2.png`, preview `phone-preview.png`. v1: `corr.py` → `correlacion-ypf-pampa.png`, `bonds.py` + `curva.py` → `curva-soberanos.png`.

## De dónde salió cada idea (skills instaladas)
- **apple-design**: jerarquía con peso+tamaño+leading; tracking/leading según tamaño; "Simplicity, not minimalism" (cada elemento se gana su lugar, a veces sumar contexto simplifica → anotar último valor); claridad por orden/espaciado/contraste; paletas que funcionan en claro y oscuro; "Craft: nada es aleatorio".
- **emil-design-eng**: "buenos defaults importan más que opciones" (→ helper con estilo listo), los detalles invisibles suman (alineaciones, márgenes fijos), revisar con ojos frescos / en chico.
- **slides**: el título/slide tiene "un solo trabajo y su punto"; cada afirmación con su fuente.
- web-design-guidelines y technical-writing: no se cargaron en esta pasada (sin guía específica de gráficos estáticos). La búsqueda "chart design" no encontró ninguna skill de gráficos.
- Convenciones propias (estándar de periodismo de datos): título-conclusión, etiquetado directo, grilla mínima, footer de fuente.
