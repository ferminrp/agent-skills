# Gráficos para X — guía

Objetivo: un PNG que se entienda en 3 segundos en el celular, con datos reales, fuente y hora BA.

## 1. Lienzo
- **Horizontal 1600×900 (16:9)** por defecto: X lo muestra completo en el timeline, sin recorte. (`xchart.figure(size="landscape")`, 8×4.5 in @200 dpi.)
- **Vertical 1080×1350 (4:5)** para rankings o tablas largas: ocupa más pantalla en mobile (`size="vertical"`).
- Cuadrado 1200×1200 sólo si hace falta.
- Exportar **PNG** (no JPG: el texto se ensucia). Márgenes ≥ 4 % por lado; nada importante en el borde.

## 2. Jerarquía (de arriba hacia abajo)
1. **Título = la conclusión**, no el tema. "YPF y Pampa se mueven juntas: r = 0.71", no "Correlación YPF-PAMP". Máx. ~45 caracteres, bold 18 pt.
2. **Subtítulo** gris: qué se mide, unidad y período ("Retornos diarios ADR · 04/11/2025–04/11/2026, 252 ruedas").
3. Gráfico.
4. **Footer**: izquierda `Fuente: <fuente> · datos al <dd/mm/aaaa hh:mm> hora BA` (+ supuestos clave en ≤ 1 línea); derecha el handle del usuario (si lo dio) en bold.
Jerarquía por peso + tamaño + color, no sólo tamaño.

## 3. Tipografía
- Sans moderna con pesos estáticos: **Pretendard** si está instalada: `xchart.py` la busca en `$FINANZAS_AR_FONT_DIR` (una o varias carpetas con los `.otf`/`.ttf`), luego `~/.finanzas-ar/fonts`; si no la encuentra usa **DejaVu Sans** (viene con matplotlib). Nada de fuentes variables en matplotlib (ignora el peso).
- Tamaños a 1600 px: título 18 pt, número grande 30, subtítulo 12, ejes 12–12.5, etiquetas 11.5, footer 9.5. A 390 px el footer queda chico (≈6 px): es aceptable porque se lee al abrir la imagen; todo lo demás tiene que leerse sin abrirla.
- Números con el mismo formato en todo el gráfico (1 decimal para %, 2 para r).

## 4. Color
- **Siempre modo claro**. `theme="light"` es el default y el único recomendado; `dark` queda en el código sólo como legado.
- **Grises + UN acento**: una familia de grises fríos; el acento azul `#1663D6` sólo en lo que cuenta la historia (regresión, ley local + brecha, número grande).
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

## 8. Reglas de diseño
- **Decilo una vez**: el número clave (ej. r) aparece sólo en el número grande, no en título + etiqueta + subtítulo. El título queda para la frase.
- **Un número es grande, el resto son líneas**: `stat()` arriba a la derecha.
- **Un acento sobre grises callados**: puntos de scatter y series secundarias en gris medio (`#6B7280`); el azul sólo en la señal.
- **Lo más pesado va sobre lo que importa**: línea principal ~2.6 px en acento; nubes y grillas finas.
- **Palabras sólo donde cuentan la historia**: etiquetas con el ticker; el valor lo da el eje. Sin leyenda ni texto redundante.
- **Profundidad por escalones de superficie, no sombras**: suelo gris muy claro → panel blanco → satélite apenas más oscuro. Sin sombras ni bordes.
- **Un héroe + como mucho un satélite** de otro tipo (ej. scatter = héroe, correlación móvil = satélite chico).
- **Un solo gutter** en todos los bordes y **sin esquinas muertas**: el número grande llena arriba a la derecha, el satélite abajo a la derecha.
- La imagen tiene que contar la historia sola, en miniatura.
- **Modos de falla**: *demasiado* (números por todos lados), *plano* (todo con el mismo peso), *encajonado* (gráfico achicado con márgenes parejos), *soso* (gris sin acento ni número grande).
- **Silueta antes que detalle**: revisar con `phone_sheet()` a 390 px; arreglar primero la falla más grande (encuadre → jerarquía → pulido).
- Un gráfico no se recorta: cortar datos miente. Si hace falta formato mobile, hacer una versión 4:5 aparte.

## Helper
`scripts/xchart.py`:
- `figure(theme="light", size="landscape", plot_box=None)` → `(fig, ax)` con suelo + panel.
- `stat(fig, value, caption, x=None, y=None, ha="right")` → el número grande.
- `label(ax, x, y, text, color=None, dx=6, dy=0, **kw)` → etiqueta directa.
- `finish(fig, title, subtitle="", source="", out="chart.png", handle=HANDLE)` → título, subtítulo, footer (fuente + handle de `FINANZAS_AR_HANDLE`), guarda el PNG y devuelve `out`.
- `phone_sheet(paths, out, width=390)` → hoja de preview a ancho de celular.
