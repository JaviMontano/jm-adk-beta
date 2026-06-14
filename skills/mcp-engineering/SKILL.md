---
name: mcp-engineering
version: 1.1.0
description: "Configurar MCP servers (project vs user scope, env-var expansion) y disenar contratos de error tipados con categoria y retryable."
owner: "JM Labs"
last_updated: 2026-06-11
triggers:
  - mcp engineering
  - mcp server config
  - mcp error contract
  - mcp scope
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Mcp Engineering

## Capacidad

Integrar servidores MCP de forma productiva: elegir el **scope** (project vs user), inyectar credenciales por **expansión de variables de entorno** y diseñar **contratos de error tipados** (`isError`, `errorCategory`, `isRetryable`, `retryAfterSeconds`) para que cliente y modelo sepan reintentar sin adivinar. [DOC]

El entregable es una config versionable por el equipo + un contrato de error consumible mecánicamente: **la política de reintento vive en el código del cliente, nunca en el juicio del modelo.** [INFERENCIA]

## Cuándo usarla

- Conectar un servidor MCP a un equipo y decidir entre `.mcp.json` (compartida, versionada) o `~/.claude.json` (personal). [DOC]
- Un servidor devuelve errores en prosa y el modelo reintenta a ciegas (típico con 429/500). [DOC]
- Hay un token literal en un archivo versionado: rotar + purgar historia. [DOC]
- Decidir si una capacidad debe ser servidor MCP o ya la cubre un tool built-in. [DOC]

**Anti-scope (no la uses cuando):**
- Un built-in (Read, Grep, Bash) ya resuelve → MCP solo cuando ningún built-in aplica. [INFERENCIA]
- La tarea no es de integración MCP (redactar prosa, búsquedas locales con grep) → no actives. [INFERENCIA]
- El usuario pide explícitamente dejar el secreto literal sin env-var → **rechaza**, no produzcas esa config. [SUPUESTO]

## Inputs / Outputs

**Inputs:** nombre del servidor + comando/args; alcance (equipo vs personal); nombres de env-vars (nunca valores); categorías de error a cubrir (`auth`/`rate_limit`/`transient`/`fatal`); límites de retry del cliente. [DOC]

**Outputs:** (1) bloque `mcpServers` con `${ENV_VAR}` y cero literales; (2) función `toolError(...)` tipada; (3) lazo de reintento client-owned, acotado; (4) plan de remediación si hubo fuga. Si el entregable es JSON, debe pasar `scripts/check.sh`. [CÓDIGO]

## Cómo construir

1. **Decide el scope.** Compartida del equipo → `.mcp.json` versionado. Personal del dev → `~/.claude.json` fuera del repo. Criterio: ¿quién debe heredar este servidor? [DOC]
2. **Inyecta credenciales por env-var.** Referencia `${ENV_VAR}`; nunca el literal. El valor real vive en el entorno del proceso. [CÓDIGO]
3. **Diseña el contrato de error tipado.** Cada error expone `isError`, `errorCategory` (auth/rate_limit/transient/fatal), `isRetryable` (bool) y `retryAfterSeconds` cuando aplica. El modelo lee campos, no infiere prosa. [CÓDIGO]
4. **Coloca la política de reintento en el cliente.** El cliente decide según `isRetryable` y respeta `retryAfterSeconds`; backoff acotado, no prosa del modelo. [CÓDIGO]
5. **Si se filtró un secreto, rótalo y purga.** Rotar la credencial + reescribir historia con `git filter-repo`. Un `.gitignore` posterior NO borra lo ya commiteado. [DOC]
6. **Justifica MCP frente al built-in.** Antes de añadir un servidor, confirma que ningún built-in cubre el caso. [INFERENCIA]

## Mapeo de error → retryability

Decisión por defecto; el cliente puede endurecerla pero no relajarla. [INFERENCIA]

| `errorCategory` | `isRetryable` | `retryAfterSeconds` | Razón |
|---|---|---|---|
| `auth` | `false` | n/a | Reintentar no arregla credencial inválida; escala a rotación. |
| `rate_limit` | `true` | server-provided | Respeta `Retry-After`; backoff si falta. |
| `transient` | `true` | `null` → default 1s | Fallo de red/temporal; retry acotado. |
| `fatal` | `false` | n/a | Error de contrato/lógica; reintentar amplifica el daño. |

## Contrato determinístico

Usa los assets de `assets/` como contrato de validación: [CONFIG]

- `mcp-engineering-contract.json`: campos obligatorios del reporte.
- `scope-policy.json`: team/personal ↔ `.mcp.json` / `~/.claude.json`.
- `secret-policy.json`: formato `${ENV_VAR}`, detección de literales, remediación por rotación + `git filter-repo`.
- `typed-error-policy.json`: categorías, retryability y `retryAfterSeconds`.
- `client-retry-policy.json`: límites de retry propiedad del cliente.
- `evidence-policy.json`: evidencia mínima para certificar.

Cuando el entregable sea JSON, valida offline con `scripts/validate_mcp_engineering.py`. Para la smoke completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas. [CÓDIGO]

## Patrón correcto

```jsonc
// .mcp.json — versionado para el equipo, secreto por env-var
{
  "mcpServers": {
    "billing": {
      "command": "node",
      "args": ["./servers/billing/index.js"],
      "env": { "BILLING_API_KEY": "${BILLING_API_KEY}" }
    }
  }
}
```

```ts
// Error contract returned by the server — typed, machine-readable
function toolError(category: ErrorCategory, retryAfter?: number) {
  return {
    isError: true,
    errorCategory: category,            // "auth" | "rate_limit" | "transient" | "fatal"
    isRetryable: category === "rate_limit" || category === "transient",
    retryAfterSeconds: retryAfter ?? null,
  };
}

// Retry policy lives in the CLIENT, not in the model's judgement
async function callTool(req: Req, maxRetries = 3) {
  for (let attempt = 0; ; attempt++) {
    const res = await invoke(req);
    if (!res.isError || !res.isRetryable || attempt >= maxRetries) return res;
    await sleep((res.retryAfterSeconds ?? 2 ** attempt) * 1000); // bounded, client-owned
  }
}
```

## Anti-patrón

```jsonc
// ANTI: token literal en archivo versionado — fuga garantizada
{
  "mcpServers": {
    "billing": { "env": { "BILLING_API_KEY": "sk-live-9f3c...a21" } }
  }
}
```

```ts
// ANTI: error como string genérico — el modelo debe adivinar si reintenta
function toolError() {
  return { content: "Something went wrong, please try again" };
}
// El modelo reintenta a ciegas un fatal, o no reintenta un transient.
// Y "git rm + gitignore" NO purga el secreto del historial.
```

## Edge cases

- **`rate_limit` sin `Retry-After`:** marca `isRetryable: true` con `retryAfterSeconds: null`; el cliente aplica backoff exponencial acotado. [INFERENCIA]
- **Servidor que mezcla `isError` con `content` útil:** prioriza `isError`; nunca infieras éxito de un payload presente. [SUPUESTO]
- **Mismo servidor en ambos scopes:** `~/.claude.json` (personal) hace shadowing del `.mcp.json` del repo; documenta cuál gana para evitar drift. [SUPUESTO]
- **Env-var ausente en runtime:** falla ruidoso al arrancar, no con credencial vacía silenciosa. [INFERENCIA]
- **Retry infinito:** todo lazo client-owned debe tener tope (`maxRetries`); sin tope, un `transient` persistente cuelga al agente. [INFERENCIA]

## Disparadores de auto-corrección

Detente y rehaz si: [INFERENCIA]
- Encuentras un literal con forma de secreto (`sk-`, `ghp_`, base64 largo) en un archivo versionado → conviértelo a `${ENV_VAR}` y dispara remediación.
- Un error carece de `errorCategory` o `isRetryable` → el contrato es inválido, no lo certifiques.
- Hay lógica de backoff en prosa o en el prompt del modelo → muévela al cliente.
- Propones MCP sin descartar antes el built-in equivalente → revierte a built-in.
- El plan ante fuga es solo `.gitignore`/`git rm` → insuficiente, exige rotación + `filter-repo`.

## Gate de aceptación (Checklist)

- [ ] Scope correcto (`.mcp.json` equipo / `~/.claude.json` personal). [DOC]
- [ ] Credenciales por `${ENV}`; cero secretos literales en archivos versionados. [CÓDIGO]
- [ ] Cada error expone `errorCategory` + `isRetryable` (+ `retryAfterSeconds` si aplica). [CÓDIGO]
- [ ] Política de reintento en el cliente, acotada (`maxRetries`), no en el modelo. [CÓDIGO]
- [ ] MCP solo cuando ningún built-in aplica. [INFERENCIA]
- [ ] Ante fuga: rotar + `filter-repo`, no solo `.gitignore`. [DOC]
- [ ] El reporte pasa `scripts/check.sh` cuando se requiere evidencia offline. [CÓDIGO]

## Katas y skills relacionadas

- Katas: 06, 22.
- Skills relacionadas: `katas-mcp-structured-errors`, `katas-mcp-server-configuration`, `tool-use-design`, `custom-tooling-extension`.
