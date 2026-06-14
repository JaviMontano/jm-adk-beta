<!-- distilled from alfa skills/acta-formal -->
<!-- > -->
# Acta Formal

> "Lo que no se documenta, no existe." — Principio de gestion corporativa

## TL;DR

Genera borradores de actas formales de reunion con formato legal/corporativo: secciones numeradas (I-VIII), tabla de asistentes, quorum, acuerdos con responsables y deadlines, bloque de firmas, salida markdown/HTML. No inventa acuerdos, quorum, folios, asistentes ni firmantes; los datos faltantes quedan como `por_confirmar`. Subida a Drive o envio por email exigen confirmacion humana explicita tras revisar el borrador. [EXPLICIT]

## When to Activate

| Signal | Example |
|--------|---------|
| Acta formal | "Redacta el acta formal de la junta" |
| Acta corporativa | "Genera el acta de la reunion de consejo" |
| Formato legal | "Necesito las minutas en formato oficial" |
| Distribucion | "Crea el acta y mandala a los asistentes" |
| Firmas / quorum / folio | "Necesito acta con firmas, quorum y numero de folio" |

No activar para notas informales, resumen de standup o "acta de la reunion" sin senales formales; usar `meeting-notes`. Para preparar temas antes de la reunion, generar una agenda simple o derivar a una skill de agenda disponible; no referenciar una skill inexistente. [INFERRED]

**Anti-scope (fuera de alcance):** no emite dictamen de validez juridica del acta, no certifica firmas (no es notaria/fedatario), no calcula quorum estatutario sin que el umbral lo provea el usuario, no traduce, no archiva en sistemas de gestion documental, no genera el orden del dia desde cero (eso es agenda). [EXPLICIT]

## S1 — Recopilar Metadata

1. **Datos generales**: fecha, hora inicio/fin, lugar (fisico o virtual), tipo de reunion
2. **Convocante**: nombre y cargo de quien convoca
3. **Asistentes**: nombre, cargo, firma (presente/ausente/justificado)
4. **Quorum**: validar contra el umbral provisto; sin umbral, marcar `no verificable`
5. **Numero de acta**: secuencial o por folio (integrar con `folio-generator` si disponible)

Si falta un dato critico, usar `por_confirmar` o pedirlo antes de cerrar el acta. No completar por inferencia nombres, cargos, asistentes, acuerdos, fechas limite, firmantes, quorum ni numero secuencial. [EXPLICIT]

**Quorum — regla de calculo.** Quorum = `presentes / total_con_derecho >= umbral`. El umbral lo define el estatuto o el usuario; nunca se asume 50%+1 por defecto. Sin umbral o sin total fiable → `no verificable`, no `validado`. [EXPLICIT] Si no aplica (reunion informativa sin votacion) → `no aplica`. [INFERRED]

**Worked example (entrada → estado quorum).** Consejo de 7 miembros, umbral estatutario "mayoria simple" (>=4), asisten 5 → `validado` (5/7). [EXPLICIT] Mismo consejo, el usuario no aporta umbral → `no verificable`; se redacta el acta con la asistencia registrada y se pide el umbral antes de declarar acuerdos vinculantes. [SUPUESTO] verificar: solicitar clausula de quorum del estatuto.

## S2 — Estructurar Acta

Secciones obligatorias (numeradas con romanos):

I. **Datos Generales** — Fecha, hora, lugar, tipo, numero de acta
II. **Lista de Asistencia y Quorum** — Tabla con nombre, cargo, asistencia, firma y estado de quorum
III. **Orden del Dia** — Puntos a tratar (numerados)
IV. **Desarrollo de la Sesion** — Resumen por punto del orden del dia
V. **Acuerdos** — Tabla: acuerdo, responsable, fecha limite, estado
VI. **Asuntos Varios** — Temas no incluidos en orden del dia
VII. **Cierre** — Hora de cierre, siguiente reunion programada
VIII. **Firmas** — Bloque de firmas del presidente y secretario

**Acuerdo vs pendiente — frontera dura.** Solo entra en V un punto con decision tomada (aprobado/rechazado/diferido por votacion o consenso registrado). Una discusion sin resolucion va a IV (Desarrollo) o VI (Asuntos Varios), nunca a V como "aprobado". Convertir un pendiente en acuerdo es el anti-pattern mas costoso: fabrica obligaciones inexistentes. [EXPLICIT]

**Decision de diseno — numeracion romana.** Se usan romanos I-VIII (no arabigos) para diferenciar secciones estructurales del acta de la numeracion arabiga de puntos del orden del dia y de acuerdos; evita colision de referencias cruzadas ("punto 3 de la seccion IV"). Trade-off: menos familiar para lectores no corporativos, a cambio de cero ambiguedad en citas. [INFERRED]

## S3 — Generar Output

1. Generar version markdown (para workspace)
2. Generar version HTML con estilo corporativo neutro, o branded solo si existen tokens de marca verificables (sin tokens → neutro, no inventar paleta) [EXPLICIT]
3. Si solicitado: preparar borrador para Google Doc via `create_doc`
4. Si solicitado: preparar subida a Drive via `create_drive_file` solo despues de confirmacion humana explicita
5. Si solicitado: preparar correo a asistentes via `send_gmail_message` solo despues de confirmacion humana explicita

**Gate de distribucion — semantica.** Pasos 4 y 5 son acciones con efecto externo irreversible: se preparan (payload listo) pero quedan en estado `pendiente_confirmacion`. La confirmacion debe ser explicita y posterior a mostrar el borrador; un "si" generico previo a ver el acta no cuenta. Sin confirmacion → no ejecutar y reportar el borrador. [EXPLICIT]

## S4 — Validar

- [ ] Todas las secciones I-VIII presentes
- [ ] Quorum en estado `validado`, `no verificable` o `no aplica` (nunca vacio)
- [ ] Cada acuerdo tiene responsable y fecha limite (o `por_confirmar` visible)
- [ ] Numero de acta es unico y secuencial, o queda `por_confirmar` si no hay fuente de folio
- [ ] Formato consistente (numeracion romana en secciones, arabiga en puntos)
- [ ] No hay asistentes, acuerdos, firmantes, folios o deadlines inventados
- [ ] Ningun pendiente o discusion reclasificado como acuerdo aprobado
- [ ] Distribucion externa bloqueada hasta confirmacion humana explicita
- [ ] Evidence tags aplicados fuera del texto final del acta (el acta entregable no lleva tags)

## Quality Criteria

- [ ] Formato legal/corporativo valido
- [ ] Secciones numeradas con romanos (I-VIII)
- [ ] Tabla de asistentes completa
- [ ] Acuerdos con responsable y deadline
- [ ] Bloque de firmas al final
- [ ] Placeholders `por_confirmar` visibles para datos faltantes

**Acceptance criteria (acta lista para revision humana).**
- Cero campos inventados; todo dato no derivable del input es `por_confirmar`. [EXPLICIT]
- Estado de quorum justificado por presentes/total/umbral, o `no verificable`/`no aplica`. [EXPLICIT]
- Toda fila de V es una decision registrada, no una discusion. [EXPLICIT]
- Acciones de Drive/email en `pendiente_confirmacion`, nunca ejecutadas en el mismo turno. [EXPLICIT]
- El entregable final no contiene evidence tags; los tags viven en la traza/razonamiento. [DOC]

## Anti-Patterns

- Generar acta sin validar (o declarar) el estado de quorum
- Asumir umbral de quorum 50%+1 cuando el estatuto no lo provee
- Omitir la seccion de acuerdos
- No numerar el acta secuencialmente
- Mezclar formato informal con formato de acta
- Inventar asistentes, firmantes, votos, quorum, folios o acuerdos
- Convertir pendientes o discusiones en acuerdos aprobados
- Inventar paleta de marca cuando no hay tokens verificables
- Enviar o subir el acta sin aprobacion humana explicita
- Dejar evidence tags dentro del texto entregable del acta

## Edge Cases

- **Sin quorum suficiente:** redactar el acta como sesion no constituida o de caracter informativo; los puntos quedan sin acuerdos vinculantes y se marca `quorum: no alcanzado`. No fabricar acuerdos. [EXPLICIT]
- **Asistente que llega tarde o se retira:** registrar hora de entrada/salida en la fila; un acuerdo solo cuenta su voto si estaba presente al momento de la votacion. [INFERRED]
- **Reunion virtual:** lugar = plataforma + enlace si se provee; la firma puede ser electronica/`por_confirmar` segun politica, nunca asumir firma fisica. [SUPUESTO] verificar: politica de firma electronica del cliente.
- **Empate en votacion:** registrar el empate y el mecanismo de desempate solo si existe y se provee (voto de calidad del presidente); sin mecanismo provisto → acuerdo `no resuelto`, no se fuerza un resultado. [EXPLICIT]
- **Acta de continuacion / sesion reanudada:** referenciar el folio del acta previa; numeracion continua, no reinicia. [INFERRED]
- **Datos contradictorios en el input (dos horas de inicio):** no elegir uno por inferencia; marcar `por_confirmar` y exponer ambos. [EXPLICIT]

## Failure Modes

- **Falso `validado` de quorum** por asumir umbral o total → acuerdos aparentan validez juridica que no tienen. Mitigacion: S1 paso 4 exige umbral explicito. [EXPLICIT]
- **Acuerdo fantasma:** discusion no resuelta colada en V. Mitigacion: frontera dura S2 + checklist S4. [EXPLICIT]
- **Distribucion prematura:** email/Drive ejecutado antes de revision humana. Mitigacion: gate `pendiente_confirmacion` en S3. [EXPLICIT]
- **Folio duplicado/saltado** por no consultar fuente de numeracion → `por_confirmar` hasta tener folio fiable. [INFERRED]
- **Tags filtrados al entregable** restan formalidad legal al documento. Mitigacion: checklist final S4. [DOC]

## Related Skills

- `meeting-notes` — notas informales de reunion
- `follow-up-email` — enviar seguimiento post-reunion
- `folio-generator` — numeracion de documentos
- `office-workflow-runner` — orquestar borrador, revision y distribucion con gates

## Usage

- `/acta-formal` — generar acta completa
- "redacta el acta de la reunion de hoy"
- "genera el acta y mandala por email a todos"

## Assumptions & Limits

- Requiere input de la reunion (notas, transcript, o datos); sin input → `[OPEN]` y se solicita. [EXPLICIT]
- Formato latinoamericano corporativo por defecto; ajustable si el usuario indica jurisdiccion. [EXPLICIT]
- Numeracion secuencial requiere tracking manual o folio-generator. [EXPLICIT]
- No sustituye validacion juridica ni certificacion notarial del acta. [EXPLICIT]
- Estado de quorum depende de un umbral externo; la skill no lo deriva sola. [INFERRED]

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
