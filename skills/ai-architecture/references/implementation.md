<!-- distilled from alfa skills/ai-architecture-implementation -->
<!-- > -->
# AI Architecture Implementation: From Design to Production

Guiar la implementación de arquitecturas AI desde el diseño hasta producción — selección de tecnología,
implementación de pipelines, configuración de serving, despliegue de monitoreo, y automatización CI/CD. [EXPLICIT]
Produce blueprints de implementación, guías de selección de tecnología, y un playbook fase-a-fase que
transforma decisiones arquitectónicas en infraestructura operativa. [EXPLICIT]

Use the deterministic policies in `assets/` for phases, technology decisions, evidence, deployment controls, and report shape. When producing a JSON implementation packet, validate it offline with `bash skills/ai-architecture-implementation/scripts/check.sh`. [EXPLICIT]

---

## Principio Rector

1. **Phased delivery, not big bang.** Implementar en fases con valor entregable por fase. Fase 0 (Foundation) → Fase 1 (Data Pipeline) → Fase 2 (Model Development) → Fase 3 (Serving) → Fase 4 (CI/CD) → Fase 5 (Monitoring). Cada fase produce capacidad usable. [EXPLICIT] Antifase: no avanzar a la siguiente fase sin la Definition of Done de la actual cumplida con evidencia — fases incompletas acumulan deuda que reaparece en producción. [INFERENCIA]

2. **Start simple, evolve with evidence.** No sobre-ingenierar para escala hipotética. Empezar con la implementación más simple que resuelva el problema actual. Feature Store no es necesario para un modelo; multi-model tiering no es necesario para un tier. [EXPLICIT] Regla de disparo: agregar complejidad (Feature Store, tiering, streaming) solo cuando una métrica observada lo justifique (≥2 modelos comparten features; latencia de cómputo de feature excede SLA; costo de tier único excede presupuesto). [INFERENCIA]

3. **Tests and monitoring from Phase 0, not Phase 5.** La infraestructura de testing y monitoreo se establece en la primera fase, no se agrega después de incidentes. Cada componente implementado incluye sus tests y sus métricas desde el día uno. [EXPLICIT] Anti-patrón observado: posponer observabilidad a la última fase convierte cada incidente en una investigación a ciegas; el costo de retrofitear monitoreo supera el de instrumentarlo desde el inicio. [INFERENCIA]

4. **Training/serving parity is non-negotiable.** La lógica de feature engineering debe compartirse (mismo código o misma definición) entre entrenamiento y serving. Skew entre ambos es la causa raíz más común de degradación silenciosa en producción. [INFERENCIA]

---

## Inputs

```
Parámetros:
  MODO:        [greenfield | brownfield | remediation | migration]
  FORMATO:     [ejecutivo | técnico | híbrido]
  ALCANCE:     [pipeline | serving | genai | mlops | full]
  STACK:       [python | java | typescript | polyglot]
  INFRA:       [kubernetes | serverless | containers | hybrid]

Detección automática:
  - Si existe codebase → MODO=brownfield
  - Si existe audit report → MODO=remediation
  - Si el input menciona "migrar" → MODO=migration
  - Si existe LangChain/LlamaIndex → ALCANCE incluye genai
  - Default: MODO=greenfield, ALCANCE=full, STACK=python, INFRA=containers
```

---

## When to Use

- Implementar una arquitectura AI diseñada (output de ai-software-architecture o ai-pipeline-architecture)
- Seleccionar stack tecnológico para un nuevo sistema AI (frameworks, tools, databases)
- Implementar Feature Store, Model Registry, o Drift Detection desde cero
- Configurar CI/CD para ML (Blue & Gold deployment, validation gates)
- Desplegar sistema de monitoring y observabilidad para AI
- Implementar pipeline RAG completo (ingestion, chunking, embedding, retrieval, generation)
- Ejecutar roadmap de remediación de una auditoría de arquitectura AI
- Migrar de notebooks a producción (MLOps maturity progression)

## When NOT to Use

- Diseñar la arquitectura (antes de implementar) → **metodologia-ai-software-architecture**
- Auditar un sistema existente → **metodologia-ai-architecture-audit**
- Seleccionar patrones de diseño → **metodologia-ai-design-patterns**
- Definir estrategia de testing (sin implementar) → **metodologia-ai-testing-strategy**
- Implementar específicamente en AWS → **metodologia-aws-architecture-implementation**
- Implementar infraestructura cloud genérica → **metodologia-infrastructure-architecture**

---

## Delivery Structure: 6 Sections

### S1: Technology Stack Selection

Selecciona las tecnologías para cada componente del sistema AI con justificación basada en constraints. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/technology-selection.md
```

**Decision Framework:**
1. **Constraints**: Cloud provider, Kubernetes availability, team expertise, budget, regulations
2. **Workload type**: Traditional ML, Deep Learning, LLM Application, Agentic AI
3. **Scale**: Prototype, Production single-model, Production multi-model, Enterprise

**Selection matrix por componente:**

| Componente | Tecnología | Alternativa | Justificación |
|------------|-----------|-------------|---------------|
| ML Framework | [selección] | [alternativa] | [por qué] |
| Pipeline Orchestration | [selección] | [alternativa] | [por qué] |
| Experiment Tracking | [selección] | [alternativa] | [por qué] |
| Model Registry | [selección] | [alternativa] | [por qué] |
| Model Serving | [selección] | [alternativa] | [por qué] |
| Vector DB (si GenAI) | [selección] | [alternativa] | [por qué] |
| LLM Framework (si GenAI) | [selección] | [alternativa] | [por qué] |
| Data Quality | [selección] | [alternativa] | [por qué] |
| Monitoring | [selección] | [alternativa] | [por qué] |
| CI/CD | [selección] | [alternativa] | [por qué] |

**Worked example (RAG genai, equipo pequeño, K8s disponible, presupuesto medio):** LLM Framework → LangChain (madurez de ecosistema) sobre LlamaIndex; Vector DB → Qdrant self-hosted (control + K8s) sobre Pinecone (lock-in); Serving → vLLM (throughput de tokens) sobre TorchServe; Monitoring → Prometheus + Grafana + Evidently (open-source, sin lock-in). Cada elección lleva ADR con la constraint que la decidió. [SUPUESTO]

**Acceptance criteria:** (a) cada componente del matrix tiene tecnología + alternativa + justificación trazable a una constraint o workload type; (b) toda selección no-obvia tiene ADR con contexto, decisión, consecuencias y alternativas descartadas; (c) no hay tecnología elegida por familiaridad sin justificación de constraint. [INFERENCIA]

**Failure modes:** elegir el stack del último proyecto sin re-evaluar constraints; optimizar para escala que el roadmap no demanda (over-engineering); ignorar la curva de aprendizaje del equipo (un stack óptimo que nadie sabe operar es un riesgo, no una ventaja). [INFERENCIA]

**Entregable:** Stack decision document con ADRs por cada selección no-obvia.

### S2: Data Pipeline Implementation

Implementa el pipeline de datos desde ingestion hasta feature serving. [EXPLICIT]

```
Load references:
  Read ${CLAUDE_SKILL_DIR}/references/implementation-blueprints.md
```

**Componentes a implementar:**
- Data ingestion (sources → raw store)
- Data quality gates (schema validation, distribution checks, business rules)
- Feature engineering (transformation logic, shared between training/serving)
- Feature store setup (if applicable — offline + online + registry)
- Data versioning (training datasets)
- Pipeline orchestration (DAGs, scheduling, retry logic)
- Data monitoring (drift, freshness, coverage)

**Blueprint selection:**
- Single model, simple features → direct pipeline, no feature store
- Multiple models, shared features → Feature Store (Blueprint 1)
- Streaming requirements → Kafka/Kinesis + streaming feature computation
- Batch only → Airflow/Dagster + batch transformation

**Acceptance criteria:** quality gates rechazan datos malformados antes de que lleguen a entrenamiento; feature engineering compartido entre training y serving (un solo código fuente); datasets de entrenamiento versionados y reproducibles; pipeline con retry idempotente y alertas de freshness. [INFERENCIA]

**Failure modes:** schema validation que solo loguea pero no bloquea (datos malos pasan); feature logic duplicada en training y serving (training/serving skew garantizado); orquestación sin idempotencia (un retry corrompe el estado); pipeline sin monitoreo de freshness (features stale sirviendo predicciones obsoletas sin alerta). [INFERENCIA]

**Entregable:** Implemented pipeline with tests, monitoring, and documentation.

### S3: Model Development & Registry Setup

Implementa el ciclo de desarrollo de modelos con tracking, registro, y evaluación. [EXPLICIT]

**Componentes a implementar:**
- Experiment tracking setup (MLflow/W&B)
- Training pipeline (reproducible: code + data + config = model)
- Evaluation framework (accuracy, fairness, robustness, explainability)
- Model registry (artifact storage, metadata, versioning, staging)
- Hyperparameter optimization (Optuna/Ray Tune integration)
- Fairness testing suite (demographic parity, equal opportunity)
- Explainability integration (SHAP/LIME for traditional ML, attention for transformers)

**Blueprint selection:**
- MVP → MLflow local, manual training, basic evaluation
- Production → MLflow/W&B + automated training pipeline + full evaluation suite
- Enterprise → Full MLOps platform + governance workflows + compliance

**Acceptance criteria:** todo modelo en el registry es reproducible (code + data + config versionados juntos); evaluación incluye fairness y robustez, no solo accuracy; staging workflow exige promoción explícita antes de producción; experimentos comparables (mismas métricas, mismo split). [INFERENCIA]

**Failure modes:** modelos en producción sin lineage (no se puede reproducir ni auditar); evaluación solo por accuracy agregado que oculta sesgo en subgrupos; registry usado como dumping ground sin metadata de staging; hyperparameter tuning sin tracking (resultados no reproducibles). [INFERENCIA]

**Entregable:** Training pipeline, experiment tracking, model registry operational.

### S4: Serving & Inference Implementation

Implementa model serving, API layer, caching, y fallback mechanisms. [EXPLICIT]

**Componentes a implementar:**
- Model serving deployment (vLLM/Triton/TorchServe/Seldon)
- API layer (REST/gRPC endpoints, versioning, documentation)
- Authentication and authorization (API keys, OAuth, service mesh)
- Rate limiting (per-client, per-endpoint)
- Caching layer (prediction cache + semantic cache for GenAI)
- Circuit breaker (fallback cascade: model → cache → previous → denial)
- Load testing baseline (P50, P95, P99, max throughput)

**GenAI-specific implementation:**
- Guardrails system (input validation, output filtering, PII masking)
- RAG pipeline (Blueprint 5: ingestion, chunking, embedding, retrieval, generation)
- Agent framework (tool definitions, governance, memory, orchestration)
- Multi-model routing (Blueprint 6: tier assignment, cost tracking)

**Acceptance criteria:** load test ejecutado con P50/P95/P99 y throughput máximo documentados vs. SLA; circuit breaker probado con fallo inyectado (cascade verificado: model → cache → previous → denial); rate limiting activo por cliente y endpoint; en GenAI, guardrails de input y output verificados con casos adversariales (prompt injection, PII en salida). [INFERENCIA]

**Failure modes:** desplegar sin baseline de carga (capacidad real desconocida hasta el primer pico); fallback cascade nunca probado (falla cuando más se necesita); cache sin invalidación tras nuevo modelo (sirve predicciones del modelo viejo); guardrails GenAI solo en input, dejando salidas tóxicas o con PII sin filtrar. [INFERENCIA]

**Entregable:** Serving infrastructure operational, API documented, load tested.

### S5: CI/CD & Deployment Automation

Implementa Blue & Gold deployment con validation gates automatizados. [EXPLICIT]

**Componentes a implementar:**
- Code CI (linting, type checking, unit tests, security scan)
- Data CI (data quality tests triggered on pipeline changes)
- Model CI (model quality tests triggered on model changes)
- Blue & Gold pipeline (Blue=production, Gold=staging with validation)
- Canary deployment (gradual traffic shift with metric monitoring)
- Rollback automation (one-click rollback to previous version)
- Promotion workflow (automated gates + configurable manual approval)

**Gate configuration:**
- Code quality gate: lint + type check + unit tests + security scan
- Data quality gate: schema + distribution + freshness
- Model quality gate: accuracy ≥ threshold + fairness ≥ threshold + latency ≤ SLA
- Regression gate: no accuracy drop > X% vs. current production
- Security gate: vulnerability scan + access control verification

**Blue & Gold semantics:** Blue = entorno sirviendo producción; Gold = entorno candidato que pasa todos los gates antes de recibir tráfico. La promoción Gold→Blue es atómica y reversible. Canary inserta un paso de tráfico gradual con monitoreo de métricas antes de la promoción completa. [INFERENCIA]

**Acceptance criteria:** rollback probado de extremo a extremo (no solo configurado) con tiempo de recuperación medido; regression gate compara contra producción actual, no contra un baseline estático; ningún cambio de modelo o datos llega a Blue sin pasar todos los gates; aprobación manual configurable para cambios de alto riesgo. [INFERENCIA]

**Failure modes:** gates definidos pero no bloqueantes (cosmética de CI); rollback documentado pero nunca ejecutado (falla en el incidente real); canary sin criterio de aborto automático (degradación pasa a 100% del tráfico); promoción que omite el regression gate y degrada accuracy silenciosamente. [INFERENCIA]

**Entregable:** CI/CD pipeline operational, gates configured, rollback tested.

### S6: Monitoring & Observability Implementation

Implementa el stack de observabilidad completo para el sistema AI. [EXPLICIT]

**Componentes a implementar:**
- Infrastructure monitoring (CPU, GPU, memory, storage, network)
- Application monitoring (request rate, error rate, latency)
- Model monitoring (accuracy tracking, prediction distribution, confidence)
- Data monitoring (input drift, feature freshness, quality violations)
- Drift detection system (Blueprint 3: statistical monitoring + alerts)
- Dashboards (executive, operations, ML, data)
- Alerting (thresholds, escalation policies, on-call integration)
- Runbooks (incident response for common AI failures)

**Dashboard hierarchy:**
- Executive: Business KPIs, model impact, cost summary
- Operations: System health, latency, errors, throughput
- ML: Model metrics, drift, fairness, prediction quality
- Data: Pipeline health, quality scores, freshness

**Acceptance criteria:** las cuatro capas (infra, app, model, data) instrumentadas; cada alerta tiene umbral, política de escalamiento y runbook asociado; drift detection con baseline estadístico y alertas activas; al menos un runbook validado mediante un game-day o simulacro de incidente. [INFERENCIA]

**Failure modes:** dashboards sin alertas (nadie mira hasta que el cliente reporta); alertas sin runbook (el on-call recibe el page sin saber qué hacer); drift detection que alerta sin baseline calibrado (ruido que se ignora — alert fatigue); monitorear infra y app pero no model/data (el modelo se degrada sin señal). [INFERENCIA]

**Entregable:** Full observability stack, dashboards, alerts, runbooks.

---

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|----------|---------|------------|-------------|
| **Managed MLOps platform** | Fast setup, integrated tools | Vendor lock-in, less customization | Teams without ML infra expertise |
| **Open-source stack** | Full control, no lock-in | Integration effort, operations burden | Teams with strong infra skills |
| **Monorepo** | Unified CI/CD, shared code | Build complexity, repo size | Small-medium teams, shared components |
| **Multi-repo** | Team autonomy, independent releases | Integration testing harder, code duplication | Large teams, independent services |
| **Kubernetes-native** | Scaling, orchestration, ecosystem | Complexity, K8s expertise required | Multi-model, high-scale systems |
| **Serverless** | Zero-ops, pay-per-use | Cold starts, limited customization | Event-driven, low-to-medium traffic |

**Trade-offs decididos (con justificación):**
- **Feature Store sí/no** → habilita reuso y parity training/serving; cuesta operación e infraestructura. Justificado solo con ≥2 modelos compartiendo features o skew observado. Para un modelo, pipeline directo. [INFERENCIA]
- **Managed vs. open-source serving** → managed reduce time-to-prod pero acopla a vendor y limita tuning de throughput; open-source (vLLM/Triton) da control de latencia/costo a cambio de carga operativa. Decidir por madurez del equipo de infra. [INFERENCIA]
- **Canary vs. promoción directa** → canary reduce blast radius de un mal deploy a costo de complejidad de routing y métricas. Justificado cuando el costo de una regresión en producción supera el costo del setup. [INFERENCIA]

---

## Phase Sequencing & Definition of Done

Las 6 secciones de entrega (S1–S6) se materializan en 6 fases. La Fase 0 (Foundation), referida en el Output Artifact, precede a la implementación de S2–S6 y se cubre en S1 + repository skeleton. [INFERENCIA]

| Fase | Cubre | DoD (evidencia requerida) |
|------|-------|----------------------------|
| 0 Foundation | Stack (S1), repo structure, CI skeleton, dev env | Repo con tests + CI corriendo; ADRs publicados; entorno reproducible |
| 1 Data Pipeline | S2 | Quality gates bloqueantes; features consistentes training=serving; datasets versionados |
| 2 Model Development | S3 | Modelo reproducible en registry; evaluación con fairness; staging workflow |
| 3 Serving | S4 | API documentada; load test con P50/P95/P99; circuit breaker probado; guardrails (si GenAI) |
| 4 CI/CD | S5 | Gates bloqueantes; Blue & Gold con rollback ejecutado; canary con aborto automático |
| 5 Monitoring | S6 | 4 capas instrumentadas; alertas con runbook; drift detection activo |

**Regla de avance:** no se inicia la fase N+1 sin la DoD de la fase N firmada con evidencia. La excepción es remediación post-auditoría, donde el orden lo dicta el priority score del audit (ver Edge Case 3). [INFERENCIA]

---

## Assumptions

1. Arquitectura AI ya diseñada (output de ai-software-architecture, ai-pipeline-architecture, o similar)
2. Cloud provider y presupuesto definidos
3. Equipo técnico disponible con habilidades core (Python, ML basics, CI/CD)
4. Ambiente de desarrollo provisionado o provisionable
5. Acceso a datos de entrenamiento (o plan para obtenerlos)

## Limits

1. NO diseña la arquitectura — implementa una arquitectura ya diseñada
2. NO selecciona patrones — implementa patrones ya seleccionados (ver **metodologia-ai-design-patterns**)
3. NO genera modelos ML — implementa la infraestructura para entrenarlos y servirlos
4. Implementación AWS-específica requiere **metodologia-aws-architecture-implementation**
5. NO reemplaza la expertise del equipo — guía y estructura, no ejecuta en solitario

---

## Edge Cases

1. **Equipo sin experiencia ML**: Fase 0 extendida con capacitación. Empezar con managed services (SageMaker, Vertex). Reducir complejidad de Feature Store y multi-model tiering hasta que el equipo madure. [EXPLICIT]

2. **Migración desde notebooks**: Priorizar extracción de feature engineering y training logic a módulos Python testeables. Notebooks quedan solo para exploración. Fase 2 se convierte en la fase más larga. [EXPLICIT]

3. **Remediación post-auditoría**: Ordenar implementación por priority score del audit report, no por la secuencia estándar de fases. Puede requerir empezar por Fase 5 (monitoring) si el hallazgo crítico es "no hay observabilidad". [EXPLICIT]

4. **Sistema GenAI puro (sin ML tradicional)**: Fases 2 y 3 se fusionan en "RAG/Agent Implementation". Feature Store no aplica. Focus en guardrails, vector DB, prompt management, cost controls. [EXPLICIT]

5. **Restricciones de presupuesto extremas**: Open-source everything. MLflow (free), Feast (free), Evidently (free), GitHub Actions (free tier). Docker Compose para desarrollo, single-instance para producción inicial. [EXPLICIT]

---

## Manejo de Inputs Ambiguos

- Si el nombre del sistema no se proporciona: solicitar antes de proceder.
- Si el MODO no se especifica: usar `piloto-auto` (default).
- Si el contexto es insuficiente para una sección: documentar como "[Requiere input adicional: {descripción}]" en lugar de inventar contenido.
- Si no hay arquitectura diseñada previamente: recomendar ejecutar primero metodologia-ai-software-architecture o metodologia-ai-pipeline-architecture antes de implementar.
- Si el equipo no tiene experiencia en la tecnología seleccionada: agregar fase 0 de capacitación y empezar con managed services.

---

## Validation Gate

- [ ] Stack tecnológico seleccionado con ADR por cada decisión no-obvia
- [ ] Repository structure creada con tests y CI desde Fase 0
- [ ] Data pipeline implementado con quality gates operativos
- [ ] Feature store/pipeline produciendo features consistentes (training = serving)
- [ ] Model registry operativo con versioning, metadata, y staging workflow
- [ ] Serving layer operativo con API documentada y load tested
- [ ] Guardrails implementados (si GenAI) — input + output + operational
- [ ] CI/CD con validation gates configurados y testeados
- [ ] Blue & Gold deployment operativo con rollback verificado
- [ ] Monitoring stack completo: infrastructure, application, model, data
- [ ] Drift detection activo con alertas configuradas
- [ ] Runbooks documentados para failure scenarios comunes
- [ ] Cada fase tiene Definition of Done cumplida con evidencia
- [ ] Si se produce JSON, el paquete pasa `scripts/check.sh`

*El agente que ejecuta este skill debe verificar cada item antes de entregar el output al usuario.*

---

## Cross-References

| Skill | Relación |
|-------|----------|
| `ai-software-architecture` | Proporciona diseño de arquitectura a implementar |
| `ai-pipeline-architecture` | Proporciona diseño de pipelines a implementar |
| `ai-design-patterns` | Proporciona patrones seleccionados a implementar |
| `ai-testing-strategy` | Proporciona estrategia de testing a implementar en CI/CD |
| `genai-architecture` | Proporciona diseño GenAI a implementar |
| `ai-architecture-audit` | Proporciona roadmap de remediación a ejecutar |
| `ai-conops` | Proporciona modos operacionales y métricas de éxito |
| `aws-architecture-implementation` | Implementación AWS-específica (complementaria) |
| `aws-architecture-design` | Diseño AWS que se implementa con el skill AWS |
| `infrastructure-architecture` | Proporciona diseño de infraestructura base |

---

## Output Format Protocol

```
if FORMATO == "ejecutivo":
  Stack summary + implementation timeline + resource needs + milestones
  Audiencia: Project managers, sponsors

if FORMATO == "técnico":
  Full 6-section implementation guide + blueprints + configurations
  Audiencia: ML engineers, DevOps, platform engineers

if FORMATO == "híbrido":
  Executive timeline + technical deep-dive completo
  Audiencia: Tech leads planning implementation sprints
```

## Output Artifact

```
## {System Name} — AI Architecture Implementation Guide

### Stack Decision
[S1: Technology selection matrix with ADRs]

### Phase 0: Foundation
[Repository structure, CI skeleton, development environment]

### Phase 1: Data Pipeline
[S2: Pipeline implementation, quality gates, feature store]

### Phase 2: Model Development
[S3: Training pipeline, experiment tracking, model registry]

### Phase 3: Serving & Inference
[S4: Model serving, API, caching, guardrails, RAG/agents]

### Phase 4: CI/CD & Deployment
[S5: Blue & Gold pipeline, gates, canary, rollback]

### Phase 5: Monitoring & Operations
[S6: Observability stack, dashboards, alerts, runbooks]

### Implementation Timeline
[Gantt chart with milestones and dependencies]
```

---
**Fuente**: Avila, R.D. & Ahmad, I. (2025). *Architecting AI Software Systems*. Packt.
