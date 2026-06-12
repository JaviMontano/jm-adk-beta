<!-- distilled from alfa skills/mermaid-diagramming -->
<!-- This skill should be used when the user asks to "create diagrams", "generate Mermaid", -->
# Mermaid Diagramming Engine

Generates syntactically valid, semantically precise Mermaid diagrams for discovery deliverables. Every diagram earns its place — no decorative visuals. Each diagram must compress complexity into clarity, replacing paragraphs of prose with a single visual a reader grasps in seconds. [EXPLICIT]

## Principio Rector

**Un diagrama que no comprime complejidad en claridad no merece existir.** Decoración ≠ documentación. Tres reglas no negociables, en orden de prioridad cuando entran en conflicto:

1. **Sintaxis impecable.** Un diagrama que no renderiza es peor que ningún diagrama — gana primero. Validar antes de entregar. [EXPLICIT]
2. **Densidad informativa.** Si transmite ≤3 oraciones de texto, es ruido visual: eliminar o fusionar. [EXPLICIT]
3. **Contexto > estética.** Nodos con significado de dominio (no códigos), flechas etiquetadas, subgrafos con propósito. [EXPLICIT]

## Inputs ($ARGUMENTS)

| Argument | Required | Description |
|----------|----------|-------------|
| `$CONTEXT` | Yes | Source material: deliverable content, code analysis, or structured data to visualize |
| `$DIAGRAM_TYPE` | No | Specific type requested (auto-selected if omitted based on content) |
| `$AUDIENCE` | No | Target reader: `executive` (simplified), `technical` (detailed), `operational` (actionable) |

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
  - **piloto-auto**: Auto para selección de tipo y composición, HITL para validación de diagramas complejos (>15 nodos). [EXPLICIT]
  - **desatendido**: Cero interrupciones. Diagramas generados automáticamente. Supuestos documentados. [EXPLICIT]
  - **supervisado**: Autónomo con checkpoint al seleccionar tipo de diagrama. [EXPLICIT]
  - **paso-a-paso**: Confirma tipo, composición, y validación de cada diagrama. [EXPLICIT]
- `{FORMATO}`: `markdown` (default, fenced code blocks) | `html` (pre class="mermaid") | `dual`
- `{VARIANTE}`: `ejecutiva` (simplified, ≤10 nodes) | `técnica` (full detail, default)

## When to Use

- Any discovery deliverable needs architectural, flow, or relationship visualization
- A concept is better understood visually than textually
- Cross-references between components, stakeholders, or phases need mapping
- Decision trees, timelines, or state machines need representation

## When NOT to Use

- The diagram would merely repeat what the text already says clearly
- Data is better represented as a table (metrics, scores, comparisons)
- The audience won't have Mermaid rendering capability (use ASCII fallback)

## S1 — Diagram Type Selection

Analyze the content and select the optimal diagram type:

| Content Pattern | Diagram Type | Mermaid Syntax |
|----------------|--------------|----------------|
| System components + relationships | C4 Context/Container | `C4Context` / `C4Container` |
| Sequential process steps | Flowchart | `flowchart TD/LR` |
| Actor interactions over time | Sequence Diagram | `sequenceDiagram` |
| Entity relationships | Entity Relationship | `erDiagram` |
| State transitions | State Diagram | `stateDiagram-v2` |
| Project timeline / phases | Gantt Chart | `gantt` |
| Hierarchical decomposition | Mindmap | `mindmap` |
| 2-axis positioning (e.g., risk vs impact) | Quadrant Chart | `quadrantChart` |
| Class/module structure | Class Diagram | `classDiagram` |
| Git/decision branching | Gitgraph | `gitGraph` |
| User journey steps | User Journey | `journey` |
| Data flow / pipeline | Flowchart with subgraphs | `flowchart LR` + `subgraph` |

Selection criteria: Choose the type that maximizes information density while minimizing cognitive load. [EXPLICIT]

## S2 — Diagram Composition Rules

1. **Syntax validity**: Every diagram MUST render without errors in standard Mermaid renderers (GitHub, GitLab, Obsidian, Mermaid Live Editor). [EXPLICIT]
2. **Node naming**: Use descriptive IDs (`authService` not `A1`). Wrap display labels in quotes if they contain spaces. [EXPLICIT]
3. **Edge labels**: Every relationship/arrow carries a label explaining the connection. [EXPLICIT]
4. **Subgraphs**: Group related nodes. Name subgraphs meaningfully. [EXPLICIT]
5. **Direction**: Use `TD` (top-down) for hierarchies, `LR` (left-right) for flows/sequences. [EXPLICIT]
6. **Color/styling**: Use `classDef` for semantic coloring (e.g., `classDef critical fill:#f96,stroke:#333`). Max 4 style classes per diagram. [EXPLICIT]
7. **Size discipline**: Max 20 nodes per diagram. If more needed, split into multiple diagrams with cross-references. [EXPLICIT]
8. **Accessibility**: Include a 1-line text summary before each diagram for screen readers and non-rendering contexts. [EXPLICIT]

## S3 — Deliverable-Specific Diagram Catalog

Each discovery deliverable has recommended diagram types:

| Deliverable | Primary Diagram | Secondary Diagram |
|------------|-----------------|-------------------|
| 01_Stakeholder_Map | Quadrant (influence × interest) | Mindmap (org structure) |
| 02_Brief_Tecnico | Mindmap (stack overview) | Quadrant (health semaphore) |
| 03_Analisis_AS-IS | C4 Context + Container | Class (module dependencies) |
| 04_Mapeo_Flujos | Sequence (E2E flows) | Flowchart (integration map) |
| 05_Escenarios | Flowchart (decision tree) | Quadrant (score positioning) |
| 06_Solution_Roadmap | Gantt (phase timeline) | Flowchart (pivot decision tree) |
| 07_Spec_Funcional | Flowchart (use case flows) | ER (data model) |
| 08_Pitch_Ejecutivo | Mindmap (value pillars) | Gantt (investment timeline) |
| 09_Handover | Flowchart (governance flow) | Gantt (90-day plan) |

Minimum: 1 diagram per deliverable. Recommended: 2. Maximum: 4 (avoid visual overload). [EXPLICIT]

## S3.5 — Worked Examples (copy-paste baselines)

Canonical, render-tested templates for the highest-frequency types. Adapt node names to domain; keep the structural pattern. [EXPLICIT]

**Quadrant (Stakeholder influence × interest):**
```mermaid
quadrantChart
  title Stakeholder Influence vs Interest
  x-axis Low Interest --> High Interest
  y-axis Low Influence --> High Influence
  quadrant-1 Manage Closely
  quadrant-2 Keep Satisfied
  quadrant-3 Monitor
  quadrant-4 Keep Informed
  CFO: [0.85, 0.90]
  EndUsers: [0.75, 0.30]
```

**Flowchart with subgraph + classDef (integration map):**
```mermaid
flowchart LR
  classDef critical fill:#f96,stroke:#333,stroke-width:2px
  subgraph Frontend
    web["Web App"]
  end
  subgraph Backend
    api["Order API"]:::critical
    db[("Postgres")]
  end
  web -->|"REST /orders"| api
  api -->|"SQL"| db
```

**Sequence (E2E flow):**
```mermaid
sequenceDiagram
  participant U as User
  participant A as Auth Service
  participant O as Order API
  U->>A: POST /login
  A-->>U: JWT token
  U->>O: GET /orders (Bearer JWT)
  O-->>U: 200 order list
```

**ER (data model — note crow's-foot cardinality):**
```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places
  ORDER ||--|{ LINE_ITEM : contains
  CUSTOMER {
    string id PK
    string email
  }
```

**Gantt (roadmap phases):**
```mermaid
gantt
  title Solution Roadmap
  dateFormat YYYY-MM-DD
  section Discovery
  AS-IS Analysis :done, d1, 2026-01-06, 10d
  section Build
  MVP :active, b1, after d1, 30d
```

## S4 — Quality Validation

Every diagram must pass ALL criteria — any single fail blocks delivery. [EXPLICIT]

| Criterion | Pass condition (testable) |
|-----------|---------------------------|
| Syntax | Renders without errors in Mermaid Live Editor; no reserved-char or cardinality faults (see Failure Modes) |
| Semantics | Every node/edge traces to a source fact; no invented entities |
| Readability | Target audience grasps intent in <10s; ≤20 nodes, ≤4 style classes |
| Information density | Replaces ≥3 sentences of prose; otherwise cut |
| Consistency | Same terminology as surrounding document |
| Cross-reference | Node names exactly match entity names used elsewhere in the deliverable |
| Accessibility | A 1-line text summary precedes the diagram |
| Governance | No PII/credentials/internal IPs; abstracted to categories |

## S5 — Output Format Integration

**In Markdown deliverables (default):**
````markdown
> **Figure N**: [1-line description for accessibility]

```mermaid
[diagram code]
```

*Source: [CÓDIGO] / [DOC] / [INFERENCIA]*
````

**In HTML deliverables (on demand):**
Embed Mermaid via `<pre class="mermaid">` tag with Mermaid JS CDN include. Add `alt` attribute with text description. [EXPLICIT]

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|---|---|---|---|
| **Max 20 nodes** | Readability, quick comprehension | Cannot show full system in one view | Always — split complex diagrams |
| **Max 4 style classes** | Visual clarity | Limited visual differentiation | Always — more colors = more cognitive load |
| **Descriptive IDs** | Source readability, self-documenting | Longer Mermaid code | Always — readability > brevity |
| **Text summary before diagram** | Accessibility, fallback rendering | Minor overhead per diagram | Always — non-negotiable for accessibility |
| **C4 extension usage** | Rich architecture notation | Limited renderer support | When architecture visualization is primary |

## Assumptions

- Target renderers support Mermaid v10+ syntax
- Readers have basic familiarity with flowchart/diagram conventions
- Diagrams supplement text, never replace it entirely

## Limits

- Cannot generate raster images (PNG/SVG) — output is Mermaid code only
- C4 diagrams use Mermaid's C4 extension (may not render in all contexts)
- Complex diagrams (>20 nodes) require decomposition into sub-diagrams
- Animation/interactivity not supported in Mermaid

## Edge Cases

- If source data is insufficient for a meaningful diagram → skip diagram, note gap
- If two diagram types are equally valid → prefer the one with fewer nodes
- If diagram would contain sensitive data (credentials, internal IPs) → abstract to categories
- If the deliverable already has 4 diagrams → drop the lowest-density candidate, do not add a 5th

## Failure Modes (most common broken-render causes)

These break rendering silently or produce parse errors. Check each before delivery. [EXPLICIT]

| Symptom | Cause | Fix |
|---|---|---|
| Parse error on a node label | Label contains `()`, `[]`, `:`, `;`, `#`, or `>` unquoted | Wrap label in double quotes: `n["Order (v2)"]` |
| Edge label with spaces fails | Unquoted multi-word edge text | Quote it: `a -->\|"sends to"\| b` |
| Diagram silently blank | First non-comment line is not a valid type keyword | Ensure line 1 is `flowchart LR`, `sequenceDiagram`, etc. — no leading prose |
| `classDef` ignored | Applied with wrong syntax | Apply via `nodeId:::className` or `class nodeId className` |
| ER cardinality error | Wrong crow's-foot tokens | Use `\|\|--o{`, `\|\|--\|{`, `}o--o{` (left-mid-right symbols) |
| Gantt task not shown | `dateFormat` missing or task date malformed | Declare `dateFormat YYYY-MM-DD`; use `after <id>` for dependencies |
| C4 diagram fails in GitHub | Renderer lacks C4 extension | Fall back to `flowchart` with subgraphs; reserve C4 for Mermaid Live / supported targets |
| Mindmap indent error | Mixed tabs/spaces or inconsistent depth | Use consistent 2-space indents; root must be a single node |

**Reserved-character rule of thumb:** when in doubt, quote the label. Quoting never breaks a valid label. [EXPLICIT]

## Validation Gate

Before delivering any diagram:
1. Paste into Mermaid Live Editor mentally — would it render? Fix syntax if not. [EXPLICIT]
2. Does it add information the text doesn't? If no, remove it. [EXPLICIT]
3. Can the target audience understand it without explanation? If no, simplify. [EXPLICIT]
4. Are all labels/names consistent with the document? If no, align. [EXPLICIT]

## Cross-References

- discovery-orchestrator — coordinates which diagrams each deliverable needs
- All pipeline skills — embed diagrams in their output artifacts
- brand-html / brand-html-extended — HTML embedding with Mermaid JS

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | ✅ | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

Default output is Markdown with embedded Mermaid diagrams. HTML generation requires explicit `{FORMATO}=html` parameter. [EXPLICIT]

## Output Artifact

**Primary:** Mermaid diagram code blocks ready to embed in Markdown or HTML deliverables. Each diagram includes accessibility text summary, source evidence tag, and figure numbering.

**Supported diagram types:** C4Context, C4Container, flowchart, sequenceDiagram, erDiagram, stateDiagram-v2, gantt, mindmap, quadrantChart, classDiagram, gitGraph, journey.

**Author:** Javier Montaño | **Last updated:** 2026-06-11
