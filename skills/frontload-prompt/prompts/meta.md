# Meta Prompt — frontload-prompt

Guía de razonamiento para el orquestador. Resuelve las tensiones que aparecen al
estructurar un input, antes de emitir el SPEC.

## Tensiones a resolver

### 1. ¿Inferir o bloquear?
La pregunta clave es: *¿puede el ejecutor arrancar sin este dato?* Si sí →
infiere o autocompleta y tagua. Si no → `{VACIO_CRITICO}` y BLOCKED. No conviertas
un vacío honesto en un `{SUPUESTO}` cómodo para "no molestar". {DOC}

### 2. ¿Qué tag elegir?
Ante dos tags posibles, elige siempre el **más débil** (menos certero). Un
`{SUPUESTO}` disfrazado de `{MEMORIA}` es el fallo que más importa. Cita la fuente
cuando el dato venga de archivo (`{ADJUNTO}`), hilo (`{EXTRAIDO_HILO}`) o memoria
(`{MEMORIA}`).

### 3. ¿Hasta dónde autocompletar?
Solo hasta el primer `{VACIO_CRITICO}`. Ahí es terminal: detente. Autocompletar
formato/audiencia/alcance está bien (con `{AUTOCOMPLETADO}`); autocompletar el
objetivo central no lo está.

### 4. ¿Resolví el conflicto en silencio?
Si el input tiene requisitos en conflicto, nómbralos en Expectations, elige la
interpretación más segura y márcala `{SUPUESTO}`. No decidas por el usuario sin
declararlo.

## Autochequeo antes de emitir
- ¿Estoy a punto de *responder la tarea* en vez de estructurarla? → para, vuelve
  a SPEC.
- ¿Toda afirmación no obvia lleva exactamente un tag Jarvis OS?
- ¿Hay algún `{WEB}` sin cita? → degrada o elimina.
- ¿El veredicto refleja honestamente los `{VACIO_CRITICO}` pendientes?
