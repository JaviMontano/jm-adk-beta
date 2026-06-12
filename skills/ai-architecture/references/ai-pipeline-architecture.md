<!-- distilled from alfa skills/ai-pipeline-architecture -->
<!-- > -->
# AI Pipeline Architecture: Development & Production Pipelines for AI Systems

AI pipeline architecture defines how data flows through AI systems — from raw ingestion through model training and serving to production monitoring. This skill produces comprehensive pipeline architecture documentation covering development pipelines (experimentation to model artifact), production pipelines (data ingestion to prediction delivery), data store selection, model registry design, CI/CD strategy, and measurable requirements. [EXPLICIT]

## Principio Rector

**El pipeline es la arquitectura. El modelo es solo un componente dentro de él.** La mayoría del esfuerzo en sistemas de IA de producción está en la infraestructura de datos, no en el algoritmo. Un pipeline mal diseñado convierte un buen modelo en un sistema frágil. Un pipeline bien diseñado permite que modelos mediocres evolucionen.

### Filosofía de Pipeline Architecture

1. **Dos pipelines, un registro.** Development pipeline y production pipeline son sistemas distintos con requisitos distintos (experimentación vs. confiabilidad). El model registry es el puente que los conecta. Sin registro, no hay reproducibilidad. [EXPLICIT]
2. **Data quality es el primer gate, no el último test.** En pipelines de IA, basura entra, basura sale — con la agravante de que el modelo amplifica los sesgos de datos malos. Quality gates al inicio del pipeline, no al final. [EXPLICIT]
3. **Blue y Gold, no YOLO deploy.** Desplegar un modelo nuevo directamente a producción es irresponsable. La estrategia Blue (producción) y Gold (staging con validación) garantiza que ningún modelo llega a usuarios sin pasar gates automatizados. [EXPLICIT]
4. **Training-serving skew es el fallo silencioso #1.** Toda transformación aplicada en training debe ser bit-idéntica en serving, o el modelo ve en producción una distribución que nunca entrenó. La única defensa estructural es compartir el código de features (feature store), no reimplementarlo. [INFERIDO]
5. **Lo no versionado no es reproducible.** Código + datos + entorno + semillas + hiperparámetros deben versionarse juntos; versionar solo el código deja el experimento irreproducible. [INFERIDO]

## Inputs

The user provides a system or project name as `$ARGUMENTS`. Parse `$1` as the **system/project name** used throughout all output artifacts. [EXPLICIT]

**Parameters:**
- `{MODO}`: `piloto-auto` (default) | `desatendido` | `supervisado` | `paso-a-paso`
- `{FORMATO}`: `markdown` (default) | `html` | `dual`
- `{ALCANCE}`: `ejecutiva` (~40% — S1 dev pipeline + S2 prod pipeline + S5 CI/CD) | `tecnica` (full 6 sections, default)

**Precedencia de inputs:** `$ARGUMENTS` explícitos > contexto detectado en el codebase > defaults. Nunca sobre-escribir un parámetro explícito con uno inferido. [INFERIDO]

Before generating architecture, detect the codebase context:

```
Detección automática de contexto:
  Escanear el codebase por frameworks ML (PyTorch, TensorFlow, scikit-learn),
  orquestadores (Airflow, Dagster, Prefect, Kubeflow), y serving frameworks
  (TensorFlow Serving, TorchServe, Triton, vLLM) para adaptar recomendaciones. [EXPLICIT]
```

Load references:

```
Read ${CLAUDE_SKILL_DIR}/references/pipeline-patterns.md
Read ${CLAUDE_SKILL_DIR}/references/data-stores.md
Read ${CLAUDE_SKILL_DIR}/references/requirements-tables.md
```

Load deterministic DoD assets:

```
Read ${CLAUDE_SKILL_DIR}/assets/pipeline-architecture-contract.json
Read ${CLAUDE_SKILL_DIR}/assets/stage-policy.json
Read ${CLAUDE_SKILL_DIR}/assets/data-store-policy.json
Read ${CLAUDE_SKILL_DIR}/assets/registry-policy.json
Read ${CLAUDE_SKILL_DIR}/assets/cicd-policy.json
Read ${CLAUDE_SKILL_DIR}/assets/requirements-policy.json
```

When scripts are present, validate the final packet with:

```
bash skills/ai-pipeline-architecture/scripts/check.sh
```

---

## When to Use

- Designing data and model pipelines for new AI systems
- Evaluating existing pipeline architecture against production requirements
- Selecting data store technologies for AI workloads (relational, object, key-value, graph, vector)
- Designing model registry and versioning strategy
- Implementing CI/CD for ML (Blue and Gold deployment)
- Defining non-functional requirements for AI pipelines (performance, security, compliance)
- Planning pipeline evolution from experimental notebooks to production infrastructure

## When NOT to Use

- Internal module boundaries and layer architecture → **metodologia-ai-software-architecture**
- CONOPS and operational concept → **metodologia-ai-conops**
- Design pattern selection and system tactics → **metodologia-ai-design-patterns**
- Testing strategy → **metodologia-ai-testing-strategy**
- GenAI/LLM-specific patterns (RAG, agents) → **metodologia-genai-architecture**
- Infrastructure provisioning and platform design → **metodologia-infrastructure-architecture**

---

## Delivery Structure: 6 Sections

### S1: Development Pipeline Architecture

Maps the experimentation-to-artifact pipeline where models are built, trained, and validated. [EXPLICIT]

**Stages:**
- **Data Quality Checks**: Schema validation, anomaly detection, distribution analysis, business rule verification
- **Data Transforms**: Feature engineering, normalization, encoding, embedding generation
- **Data Summary**: Statistical profiling, correlation analysis, class balance assessment
- **Model Building**: Algorithm selection, architecture definition, initial training
- **Model Tuning**: Hyperparameter optimization, cross-validation, regularization
- **Model Verification**: Holdout evaluation, fairness testing, robustness assessment, explainability scoring
- **Code Commit**: Model artifacts + code + configs registered in model registry with full lineage
- **CI/CD Dev Ops**: Automated pipeline testing, artifact validation, security scanning

**Key decisions:**
- Experiment tracking tool (MLflow, W&B, Neptune, SageMaker Experiments)
- Training orchestration (Kubeflow Pipelines, Vertex AI, SageMaker Pipelines, Airflow)
- Reproducibility strategy (data versioning, environment pinning, seed management)

**Acceptance criteria (S1):** cada stage declara input/output/gate; el artefacto final lleva data-hash + commit-hash + env-lockfile + seeds; un re-run con los mismos inputs reproduce métricas dentro de tolerancia declarada. [INFERIDO]

**Decisión justificada — orquestador:** Airflow cuando ya existe ecosistema/ops maduro y los DAGs son scheduling-céntricos; Kubeflow/Vertex/SageMaker Pipelines cuando el equipo es ML-first y quiere lineage y artifact-tracking nativos; Dagster cuando el activo central son los *datos* (asset-based, type-checked) y el equipo es Python-first. Trade-off: managed (Vertex/SageMaker) reduce ops a cambio de lock-in; OSS (Airflow/Dagster/Kubeflow) maximiza portabilidad a cambio de operar la plataforma. [INFERIDO]

### S2: Production Pipeline Architecture

Maps the data-to-prediction pipeline that serves AI capabilities in production. [EXPLICIT]

**Stages:**
- **Data Cleansing**: Automated validation, anomaly detection, quality enforcement with feedback loops
- **Data Transformation**: Feature computation via feature store, embedding generation, format conversion
- **Model Execution**: Prediction generation with model registry integration, A/B testing, monitoring hooks
- **Results Store**: Prediction storage, feature attribution, explanation logging, BI integration
- **Pipeline Operations**: Monitoring, alerting, self-healing, visualization, configurable logging

**Key decisions:**
- Batch vs. streaming vs. hybrid pipeline topology
- Feature store adoption (Feast, Tecton, Vertex AI Feature Store, or custom) → evolving toward Feature Platform (compute + store + monitoring + governance as integrated platform)
- Model serving framework (TF Serving, TorchServe, Triton, vLLM, SageMaker Endpoints)
- Monitoring granularity (sample rate, logging level, retention policy)
- Streaming pipeline pattern (Kappa for pure streaming, Lambda for batch+streaming hybrid)

**Acceptance criteria (S2):** cada predicción es trazable a model-version + feature-version + input-hash; existe feedback loop de calidad de datos hacia el productor; el monitoreo cubre data drift, prediction drift y latencia/error por stage, no solo el modelo. [INFERIDO]

**Decisión justificada — topología:** elegir *batch* si la latencia tolerada es ≥ minutos y el costo manda; *streaming* solo si el SLA es sub-segundo y el valor de frescura justifica la complejidad de exactly-once; *hybrid* (Lambda/Kappa) cuando coexisten scoring online y analítica offline sobre las mismas features. Regla anti-sobreingeniería: no se adopta streaming sin un requisito de latencia que lo exija. [INFERIDO]

### S3: Data Store Technology Selection

Selects appropriate storage technologies for each pipeline component. [EXPLICIT]

**Store types and AI use cases:**
- **Relational** (PostgreSQL, MySQL): Metadata, experiment tracking, model registry, audit trails
- **Object** (S3, GCS): Training data, model artifacts, archives
- **Key-Value** (Redis, DynamoDB): Feature serving cache, prediction cache, real-time lookup
- **Graph** (Neo4j): Knowledge graphs, entity relationships, fraud networks
- **Vector** (Pinecone, Qdrant, pgvector): Embedding storage, semantic search, RAG retrieval

**Selection criteria:** Query complexity, latency requirements, scale, consistency model, cost, AI-native capability.

**Multi-store pattern:** Most production AI systems combine 3-4 store types with synchronization and lineage tracking across boundaries.

**Anti-patrón:** usar un único store para todo (p.ej. forzar embeddings en una relacional sin índice vectorial, o servir features de baja latencia desde object storage). Cada store se justifica por *workload*, no por familiaridad del equipo. [INFERIDO]

**Acceptance criteria (S3):** cada selección cita latencia, escala, modelo de consistencia y capacidad AI-native que la justifican; los límites de sincronización entre stores tienen estrategia de lineage y de resolución de inconsistencias declarada. [INFERIDO]

### S4: Model Registry & Versioning

Designs the bridge between development and production pipelines. [EXPLICIT]

**Registry capabilities:**
- Model artifact storage with version history
- Metadata: training metrics, data hash, hyperparameters, lineage
- Stage management: Staging → Canary → Production → Archived
- Access control and approval workflows
- A/B experiment configuration
- Rollback support with instant reversion

**Key decisions:**
- Registry tool (MLflow, SageMaker Model Registry, Vertex AI, W&B)
- Versioning strategy (semantic versioning, timestamp-based, hash-based)
- Promotion workflow (automated gates vs. manual approval vs. hybrid)
- Multi-model coordination (dependent models, ensemble management)

**Acceptance criteria (S4):** todo modelo promovible expone version, data-hash, métricas, lineage y stage; existe un rollback probado (no solo documentado) a la versión Blue anterior; las transiciones de stage quedan auditadas con actor y timestamp. [INFERIDO]

**Failure mode:** registry sin rollback probado → un mal deploy obliga a re-entrenar bajo presión. Mitigación: ensayar la reversión en cada release como parte del gate, no como contingencia. [INFERIDO]

### S5: CI/CD for AI (Blue & Gold)

Designs the deployment strategy connecting development artifacts to production serving. [EXPLICIT]

**Blue Pipeline** (Production): Currently serving, fully validated, rollback target.
**Gold Pipeline** (Staging): New version under validation, receives shadow/canary traffic.

**Validation gates:**
1. Model validation: accuracy, AUC, fairness, robustness meet thresholds
2. Feature validation: distributions match expected profiles
3. Data quality: input data passes schema and quality checks
4. Performance: latency and throughput within SLA
5. Security: no new vulnerabilities, access controls intact
6. Regression: no degradation vs. current Blue performance

**Promotion flow:** Gold passes all gates → canary traffic → gradual shift → full promotion → Gold becomes Blue → previous Blue archived.

**Key decisions:**
- Canary percentage and duration
- Automated vs. manual gate approval
- Rollback trigger criteria
- Pipeline-level vs. model-level deployment

**Acceptance criteria (S5):** ningún modelo alcanza tráfico de usuarios sin pasar los 6 gates; el canary tiene criterio de auto-rollback por métrica (no solo por error técnico); la promoción Gold→Blue archiva la Blue previa intacta para reversión inmediata. [INFERIDO]

**Worked example — promoción segura:** Gold entrena v2.3 → gates 1-6 en verde → canary 5% por 2 h → guardrail: si error-rate o p95-latency suben >X% vs Blue, auto-rollback → si estable, shift 5→25→50→100% → Gold se vuelve Blue, v2.2 a `Archived`. Si gate 6 (regresión) falla, v2.3 nunca recibe tráfico real. [INFERIDO]

### S6: Requirements Framework (AP/NF/SEC/CP)

Defines measurable requirements across four categories with thresholds and objectives. [EXPLICIT]

**Performance (AP-1 to AP-13):** Data processing speed, model accuracy, fairness, explainability, robustness.

**Non-Functional (NF-1 to NF-9):** Availability (>99.9%), recovery time (<1 min), fault detection (<0.5 secs), drift detection (<1 hour), pipeline isolation.

**Security (SEC-1 to SEC-6):** PKI for external interfaces, audit logging, adversarial protection, data access controls, model extraction monitoring.

**Compliance (CP-1 to CP-7):** Authorized data access, transaction archival, encryption at rest/in use, audit trails, model governance workflows.

**Acceptance criteria (S6):** todo requisito es *medible* (umbral + unidad + método de medición), no aspiracional; cada categoría (AP/NF/SEC/CP) tiene al menos un requisito mapeado a un gate de S5; un requisito sin forma de verificarse en CI/CD se marca `[Requiere instrumentación]` en vez de declararse cumplido. [INFERIDO]

**Trampa común:** confundir objetivo con umbral. Declarar "alta disponibilidad" no es un requisito; "disponibilidad >99.9% medida mensual sobre el endpoint de serving" sí lo es. [INFERIDO]

---

## Trade-off Matrix

| Decision | Enables | Constrains | When to Use |
|---|---|---|---|
| **Batch Pipeline** | Simple, cost-effective, easy debugging | High latency, not real-time | Offline analytics, nightly retraining |
| **Streaming Pipeline** | Real-time predictions, low latency | Complex, exactly-once semantics hard | Real-time fraud, recommendations |
| **Hybrid Pipeline** | Best of both, flexible | Two systems to maintain, consistency | Most production AI systems |
| **Feature Store** | Consistency, reuse, drift monitoring | Infra overhead, governance cost | Multiple models sharing features |
| **Blue & Gold CI/CD** | Safe deployments, instant rollback | Doubled infrastructure during validation | All production AI systems |
| **Single Model Registry** | Central governance, clear lineage | Single point of failure, access bottleneck | Standard team size |
| **Distributed Registry** | Team autonomy, reduced bottleneck | Consistency challenges, governance complexity | Large multi-team orgs |

---

## Assumptions

- Team has or will build experience with ML pipeline orchestration
- Infrastructure supports the compute requirements for training and inference
- Data sources are identified and access is available or negotiable
- Model registry and CI/CD are organizational priorities (not afterthoughts)
- Monitoring and observability budget is allocated

## Limits

- Focuses on *pipeline architecture*, not infrastructure provisioning (see **metodologia-infrastructure-architecture**)
- Does not design *internal module structure* (see **metodologia-ai-software-architecture**)
- Does not select *design patterns or tactics* (see **metodologia-ai-design-patterns**)
- Does not define *testing strategy* beyond pipeline gates (see **metodologia-ai-testing-strategy**)
- GenAI-specific pipelines (RAG indexing, agent orchestration) require **metodologia-genai-architecture**
- AWS-specific pipeline services (SageMaker Pipelines, Step Functions, Bedrock) covered by **metodologia-aws-architecture-design**

---

## Edge Cases

**Notebook-to-Production Migration:**
Data scientists work in Jupyter notebooks; production requires orchestrated pipelines. Bridge with notebook-aware orchestrators (Papermill, Ploomber). Prioritize extracting feature engineering and model training into reusable pipeline stages. [EXPLICIT]

**Multi-Team Pipeline Ownership:**
Different teams own different pipeline stages (data eng owns ingestion, ML eng owns training, platform owns serving). Clear data contracts between stages are essential. Feature store becomes the coordination point. [EXPLICIT]

**Real-Time + Batch Hybrid:**
System needs both real-time predictions (online serving) and batch analytics (offline scoring). Lambda or Kappa architecture patterns. Feature store must support both online (low-latency) and offline (batch) serving. [EXPLICIT]

**Regulated Pipeline (Finance, Healthcare):**
Every pipeline stage must produce audit-worthy artifacts. Data lineage tracking from source to prediction. Model governance gates require human approval before production promotion. [EXPLICIT]

**Cold-start sin datos de producción:**
No hay tráfico real para validar gates de regresión. Bootstrap con datos sintéticos/replay histórico y shadow deployment (Gold recibe copia del tráfico sin servir resultados) hasta acumular evidencia. [INFERIDO]

---

## Failure Modes (síntoma → causa → mitigación)

| Síntoma en producción | Causa raíz típica | Mitigación estructural |
|---|---|---|
| Métricas online << offline | Training-serving skew | Features compartidas vía feature store; validar paridad de transforms en gate de features [INFERIDO] |
| Degradación lenta de accuracy | Data/concept drift no detectado | Monitor de drift con umbral <1 h; retraining trigger automatizado [EXPLICIT] |
| Deploy rompe y no hay vuelta atrás | Registry sin rollback probado | Ensayar reversión en cada release; Blue archivada intacta [INFERIDO] |
| Predicciones no auditables | Lineage roto entre stores | Lineage source→prediction; hash de input/feature/model por predicción [INFERIDO] |
| Pipeline "verde" pero output inútil | Gate solo técnico, sin gate de negocio | Añadir validación de distribución y de métrica de negocio al canary [INFERIDO] |
| Costo de inferencia se dispara | Streaming adoptado sin requisito de latencia | Reevaluar topología; degradar a batch/hybrid donde el SLA lo permita [INFERIDO] |

*Nota de gobernanza: "verde" en un gate significa "umbral cumplido", no "éxito"; un gate verde con métrica de negocio plana sigue siendo un fallo. [INFERIDO]*

---

## Manejo de Inputs Ambiguos

- Si el nombre del sistema no se proporciona: solicitar antes de proceder.
- Si el MODO no se especifica: usar `piloto-auto` (default).
- Si el contexto es insuficiente para una sección: documentar como "[Requiere input adicional: {descripción}]" en lugar de inventar contenido.
- Si no hay pipeline existente: diseñar desde greenfield con la fase 0 (foundation) como prioridad.
- Si el equipo no tiene experiencia con orquestadores: recomendar el más simple viable (Dagster para Python-first, Airflow para ecosistema amplio).

---

## Validation Gate

Before finalizing delivery, verify:

- [ ] Development and production pipelines are designed as separate systems connected by model registry
- [ ] Each pipeline stage has defined inputs, outputs, and quality gates
- [ ] Data store selection justified by workload characteristics (not technology preference)
- [ ] Model registry design includes versioning, lineage, staging, and rollback
- [ ] CI/CD strategy uses Blue & Gold (or equivalent staged deployment)
- [ ] Validation gates cover model quality, data quality, performance, security, and regression
- [ ] Report packet conforms to `assets/pipeline-architecture-contract.json`
- [ ] Every pipeline stage, data store, registry decision, CI/CD gate, and requirement maps to evidence ids
- [ ] Offline validator passes before delivery
- [ ] Requirements framework includes all four categories (AP, NF, SEC, CP) with thresholds
- [ ] Training-serving skew risk explicitly addressed in pipeline design
- [ ] Monitoring strategy covers all pipeline stages (not just model serving)
- [ ] Pipeline architecture is deployable (not just theoretical)

*El agente que ejecuta este skill debe verificar cada item antes de entregar el output al usuario.*

---

## Cross-References

- **metodologia-ai-software-architecture**: Provides module structure context; receives pipeline as component
- **metodologia-ai-conops**: Provides operational requirements and success metrics
- **metodologia-ai-design-patterns**: Patterns applied within pipeline stages (Feature Store, Champion-Challenger)
- **metodologia-ai-testing-strategy**: Testing strategy for pipeline validation and integration
- **metodologia-genai-architecture**: GenAI-specific pipeline patterns (RAG indexing, embedding pipelines)
- **metodologia-infrastructure-architecture**: Provides compute and storage platform for pipelines
- **metodologia-aws-architecture-design**: Maps pipeline components to AWS services (SageMaker, Step Functions, Bedrock)
- **metodologia-devsecops-architecture**: Pipeline security controls and supply chain security

## Output Format Protocol

| Format | Default | Description |
|--------|---------|-------------|
| `markdown` | Yes | Rich Markdown + Mermaid diagrams. Token-efficient. |
| `html` | On demand | Branded HTML (Design System). Visual impact. |
| `dual` | On demand | Both formats. |

## Output Artifact

**Primary:** `A-02_AI_Pipeline_Architecture_Deep.html` — Development pipeline diagram, production pipeline diagram, data store selection matrix, model registry design, Blue & Gold CI/CD flow, requirements framework tables.

**Secondary:** Pipeline stage contracts (.md), data store comparison matrix, model registry workflow diagram (Mermaid/PNG/SVG), requirements checklist.

---
**Fuente**: Avila, R.D. & Ahmad, I. (2025). *Architecting AI Software Systems*. Packt.
