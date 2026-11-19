# Monitor Argy (MCP) — v2
URL: POST https://monitorargy.com/mcp · streamable-http JSON-RPC · Auth: none. tools/list and one tools/call per tool verified 2026-10-28.
Macro series (INDEC, BCRA, etc.; 97 series, 16 panels: precios, cambiario, actividad, industria, construccion, consumo, comercio_exterior, agro, energia_mineria, salarios, empleo, expectativas, pobreza, tasas, dinero, fiscal).
Tools:
- listar_series {buscar?, panel?, frescura?: vigente|demorado|vencido, limite? ≤300} — {total, devueltas, paneles, series[{id, nombre, unidad, frecuencia, fuente, ultimaFecha, ultimoValor, frescura}]}
- obtener_serie {id, desde?, hasta?, resolucion? 1d|1w|1m (default 1m)} — {id, nombre, unidad, fuente{nombre, web}, ultimaFecha, ultimoValor, frescura, puntos[{fecha, ...}]}
- coyuntura {} — {meses[], secciones[{nombre, filas[{id, nombre, valores{mes: valor}}]}]}
- calendario {serie?, desde?, hasta?} — {desde, hasta (default +7d), total, eventos[{fecha, hora, series[], titulo, metodo}]}
```
curl -s https://monitorargy.com/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
 -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"obtener_serie","arguments":{"id":"ipc_mensual"}}}'
```
