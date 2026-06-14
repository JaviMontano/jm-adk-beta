# Ejemplo — Input

Contexto del usuario:

> Tengo un agente de soporte que llama al SDK de Anthropic. El loop actual decide
> cuándo parar leyendo el texto: `if "listo" in resp.content[0].text: break`. A
> veces el modelo dice "todavía no estoy listo" y el agente sale igual; otras
> veces se queda en bucle. Además, cuando el modelo pide dos herramientas a la vez
> (`buscar_ticket` y `leer_kb`) solo se ejecuta la primera y la conversación se
> rompe en el siguiente turno. No hay límite de iteraciones.
>
> Handlers disponibles: `{ "buscar_ticket": buscar_ticket, "leer_kb": leer_kb }`.
> Quiero `max_iterations = 12`, fallo fuerte para señales no contempladas, y poder
> auditar qué pasó en cada iteración.

Objetivo: convertir el control por prosa en un loop enrutado por `stop_reason`,
con despacho de tool calls en paralelo, budget duro y traza por iteración.
