# NotebookLM MCP — auth por navegador

Cómo funciona y cómo recuperarse cuando expira. Aplica a los 3 runtimes (mismo
binario `notebooklm-mcp`, misma storage).

## Mecánica

1. **Login = cookies de Google capturadas vía Chrome dedicado.**
   `nlm login` lanza Chrome con perfil propio en `~/.notebooklm-mcp-cli/chrome-profile/`
   (129MB, persiste sesión Google). El usuario inicia sesión UNA vez; las cookies
   se guardan en `~/.notebooklm-mcp-cli/auth.json` (por perfil nlm).
2. **El server MCP lee esa misma storage** — no tiene flujo de login propio.
   `server_info.auth_status` = check LOCAL (presencia/edad de tokens, no llamada viva).
3. **Re-login es barato**: el chrome-profile conserva la sesión Google, así que
   `nlm login` re-captura cookies sin re-teclear password (abre y cierra navegador).

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
default en `[auth] default_profile`. Cambiar: `nlm login switch <perfil>`.

## Diagnóstico

- `nlm login --check` — validación viva (cuenta notebooks).
- `scripts/auth-doctor.sh` — incluye este check.
- Storage legacy `~/.notebooklm-mcp/` puede existir — ignorar; la actual es `~/.notebooklm-mcp-cli/`.

## Regla operativa para agentes (los 3 runtimes)

Si un tool `mcp__notebooklm__*` devuelve error de auth: ejecutar `nlm login` por
Bash y reintentar. Fallback final: tool `save_auth_tokens` con cookies manuales.
