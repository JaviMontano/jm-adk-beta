<!-- distilled from alfa skills/katas-mcp-server-configuration -->
<!-- Configuracion de MCP servers: project vs user scope, env-var expansion para credenciales y rotacion ante secreto leakeado. -->
# Kata 22 · Configuracion de MCP Servers

## Que es

Los MCP servers se declaran en `.mcp.json` (project scope, versionado con el repo) o en `~/.claude.json` (user scope, personal). [DOC] Las credenciales se inyectan mediante env-var expansion (`${GITHUB_TOKEN}`), nunca hardcodeadas. [CONFIG] Al conectarse, Claude Code descubre simultaneamente todos los servers declarados y expone sus tools y resources. [DOC]

La decision central es de scope: un server en `.mcp.json` viaja con el repositorio y sirve a toda la flota; un server en `~/.claude.json` solo existe en tu laptop. [DOC] La eleccion equivocada deja a la mitad del equipo sin acceso, o publica un secreto. [INFERENCIA]

## Por que importa (falla que evita)

- Hardcodear un token en `.mcp.json` versionado equivale a publicarlo: queda en el historial de git para siempre. [INFERENCIA]
- Poner reglas de equipo en `~/.claude.json` deja a los nuevos devs sin acceso al server: la config no se replica. [DOC]
- Activar un MCP cuando un built-in (Grep, Read, Glob) ya cubre el caso es overkill que infla la superficie de tools sin ganancia. [INFERENCIA]
- Ante un secreto leakeado, agregar el archivo a `.gitignore` NO lo remueve: ya esta versionado. [DOC]

## Modelo mental

- Project scope (`.mcp.json`): viaja con el repo, descubrimiento automatico al conectar, sirve a toda la flota. [DOC]
- User scope (`~/.claude.json`): experimentos personales que no afectan al equipo. [DOC]
- Precedencia ante mismo nombre de server: el scope de usuario (`~/.claude.json`) gana sobre el de proyecto en tu laptop, lo que puede enmascarar la config de equipo sin avisar. [SUPUESTO]
- Credenciales siempre por `${ENV_VAR}` expansion, nunca literal en el archivo. [CONFIG]
- MCP resources (catalogos) reducen llamadas exploratorias frente a invocar tools una y otra vez. [INFERENCIA]
- MCP solo cuando un built-in no aplica: la integracion externa se justifica, no se asume. [DOC]
- Regla de decision de scope: ¿lo necesita toda la flota y es reproducible? → `.mcp.json`. ¿Es un experimento o credencial atada a tu maquina? → `~/.claude.json`. [INFERENCIA]

## Patron correcto

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "internal-docs": {
      "command": "node",
      "args": ["./scripts/mcp-docs.js"]
    }
  }
}
```

Server de equipo en `.mcp.json` versionado, credencial inyectada por env-var expansion (`${GITHUB_TOKEN}`), server interno sin secreto apuntando a un script del repo. [CONFIG]

## Anti-patron

```json
{ "env": { "GITHUB_TOKEN": "ghp_AbCdEfG123456789" } }
```

Token literal hardcodeado en un archivo versionado. Queda expuesto en el historial de git; agregar el archivo a `.gitignore` no lo remueve. [DOC]

## Casos limite

- **`${ENV_VAR}` no exportada en el shell** → la expansion no falla ruidosamente; el server arranca con credencial vacia y la auth rechaza con 401. Verifica `printenv GITHUB_TOKEN` antes de culpar a la config. [INFERENCIA]
- **Secreto ya commiteado** → rotar la credencial en el proveedor PRIMERO (la del historial ya es publica), luego reemplazar por `${ENV}` y purgar con `git filter-repo`; el orden inverso deja una ventana de exposicion. [DOC]
- **Server interno con path relativo** (`./scripts/mcp-docs.js`) → se resuelve respecto al cwd de Claude Code, no al de `.mcp.json`; si difieren, el server no levanta. [SUPUESTO]
- **Mismo server en ambos scopes** → la version de usuario gana en silencio; un dev puede creer que usa la config de equipo cuando no. Ante comportamiento divergente, revisa `~/.claude.json` primero. [SUPUESTO]
- **Built-in cubre el caso** (busqueda en filesystem local → Grep) → no declarar un MCP; cada server añade tools al contexto de cada turno. [INFERENCIA]

## Anti-scope

- No cubre la **implementacion** de un MCP server ni su contrato de errores (ver `mcp-structured-errors`). [DOC]
- No define la **politica de seleccion** entre built-in y MCP en detalle (ver `builtin-tool-selection`); aqui solo se afirma el principio. [DOC]
- No gestiona rotacion automatica de secretos ni vaults; asume `${ENV}` provisto por el entorno o un secret manager externo. [SUPUESTO]
- No cubre transportes remotos (SSE/HTTP) ni su auth; el patron canonico es server local via `command`/`args`. [SUPUESTO]

## Argumento de certificacion

Para certificar dominio de esta kata el agente debe:

- Distinguir project vs user scope con criterio (config de equipo va a `.mcp.json` versionado). [DOC]
- Defender env-var expansion para credenciales en lugar de literales. [CONFIG]
- Justificar un MCP solo cuando un built-in no aplica (Grep cubre busqueda en filesystem local; MCP seria overkill). [INFERENCIA]
- Responder a un secreto leakeado con rotacion de la credencial + reemplazo por `${ENV}` + purga del historial (`git filter-repo`), no con `.gitignore`. [DOC]

## Criterios de aceptacion

- Ningun secreto literal aparece en archivos versionados; toda credencial usa `${ENV_VAR}`. [CONFIG]
- Cada server declarado se justifica: o lo necesita la flota (project) o es personal (user), y ningun built-in lo hace redundante. [DOC]
- La respuesta a un leak ejecuta rotacion ANTES de purgar el historial, no `.gitignore`. [DOC]
- El scope elegido se corresponde con el alcance real (equipo → `.mcp.json`; experimento → `~/.claude.json`). [INFERENCIA]

## Cuando activar

- Configurar o revisar `.mcp.json` o `~/.claude.json`. [DOC]
- Decidir el scope de un server MCP (equipo vs personal). [DOC]
- Manejar credenciales de un server externo. [DOC]
- Responder a un token o secreto filtrado en config versionada. [DOC]

## Skills relacionadas

- `katas-builtin-tool-selection`
- `katas-custom-commands-skills`
- `katas-hierarchical-claude-memory`
