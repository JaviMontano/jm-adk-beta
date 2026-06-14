# NotebookLM MCP — auth por navegador

Cómo funciona la auth, cómo recuperarse cuando expira, y qué NO intentar.
Aplica a los 3 runtimes (`mcp__notebooklm__*`, `mcp__notebooklm-mcp__*`,
`mcp__plugin_sdf_notebooklm__*`): mismo binario `notebooklm-mcp`, misma storage. [DOC]

## Supuestos y anti-scope

- [ASSUMPTION] Una sola cuenta Google activa por `default_profile`; multi-cuenta = multi-perfil, no concurrencia.
- [ASSUMPTION] La GUI de macOS está disponible salvo runtime headless/remoto (fila correspondiente abajo).
- **No** hay OAuth/service-account ni refresh-token server-side: la única fuente de verdad son las cookies del navegador. [INFERENCE]
- **No** automatizar el teclado/SSO de Google (2FA, captchas): el login interactivo lo hace el usuario, una vez.
- **No** versionar ni copiar `auth.json`/`chrome-profile/` a otra máquina: cookies atadas a dispositivo/perfil. [ASSUMPTION]

## Mecánica

1. **Login = cookies de Google capturadas vía Chrome dedicado.** `nlm login` lanza
   Chrome con perfil propio en `~/.notebooklm-mcp-cli/chrome-profile/` (~129MB,
   persiste sesión Google). El usuario inicia sesión UNA vez; las cookies se guardan
   en `~/.notebooklm-mcp-cli/auth.json` (por perfil nlm). [DOC]
2. **El server MCP lee esa misma storage** — no tiene flujo de login propio.
   `server_info.auth_status` = check LOCAL (presencia/edad de tokens, NO llamada viva):
   puede reportar OK con cookies ya revocadas server-side. [INFERENCE]
3. **Re-login es barato**: el chrome-profile conserva la sesión Google, así que
   `nlm login` re-captura cookies sin re-teclear password (abre y cierra navegador). [DOC]

## Cuándo abre navegador

| Situación | Acción | ¿Abre navegador? |
|---|---|---|
| Tokens válidos | nada | no |
| Tool MCP falla con auth error | `nlm login` (Bash) | sí — re-captura, normalmente sin password |
| Tokens refrescados en disco por otro proceso | tool MCP `refresh_auth` | no |
| Headless/remoto (sin GUI) | `nlm login --manual -f cookies.txt` | no (cookies exportadas a mano) |
| Navegador ya corriendo (openclaw) | `nlm login --provider openclaw --cdp-url http://127.0.0.1:18800` | adjunta a Chrome existente vía CDP |
| Cambiar de cuenta Google | `nlm login --clear` | sí — perfil Chrome limpio |

## Config

`nlm config show` → `[auth] browser = "auto"` (elige Chrome). Perfiles: `nlm login profile list`,
default en `[auth] default_profile`. Cambiar: `nlm login switch <perfil>` (instantáneo, sin reiniciar server).

## Diagnóstico

- `nlm login --check` — validación VIVA (cuenta notebooks). Úsalo cuando `auth_status` dice OK pero los tools fallan.
- `scripts/auth-doctor.sh` — incluye este check.
- Storage legacy `~/.notebooklm-mcp/` puede existir — ignorar; la actual es `~/.notebooklm-mcp-cli/`. [DOC]

## Regla operativa para agentes (los 3 runtimes)

Si un tool `mcp__notebooklm__*` (o variante de runtime) devuelve error de auth:

1. `refresh_auth` (tool MCP) — barato, cubre el caso "otro proceso ya re-logueó". Si pasa, reintentar.
2. `nlm login` por Bash — re-captura cookies. Reintentar el tool original.
3. Fallback final: tool `save_auth_tokens` con cookies manuales (solo si el CLI falla). [DOC]

**No** reintentar el mismo tool en bucle sin pasar por (1)/(2): el error de auth no se cura solo.

## Criterios de aceptación

- [EXPLICIT] Tras recuperación, `nlm login --check` lista notebooks Y el tool original devuelve datos (no solo `auth_status` OK).
- [EXPLICIT] Cambio de cuenta: `nlm login switch <perfil>` seguido de un tool que devuelve datos de la cuenta nueva.
- [EXPLICIT] Headless: cookies importadas y `--check` válido sin que se abra ninguna GUI.

## Edge cases

- `auth_status` OK + tool falla → cookies revocadas server-side; ir directo a `nlm login`, no confiar en el check local. [INFERENCE]
- CDP (openclaw): si el Chrome de `--cdp-url` murió, `nlm login` cae al flujo normal (abre Chrome propio). [ASSUMPTION]
- 2FA expirado / cuenta deslogueada en Google → `nlm login --clear` para forzar perfil limpio y re-autenticar interactivamente.
- Múltiples runtimes compitiendo: comparten storage, así que un `nlm login` los re-habilita a todos a la vez. [INFERENCE]
