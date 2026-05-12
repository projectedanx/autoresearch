# autoresearch

![teaser](progress.png)

*One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun, and synchronizing once in a while using sound wave interconnect in the ritual of "group meeting". That era is long gone. Research is now entirely the domain of autonomous swarms of AI agents running across compute cluster megastructures in the skies. The agents claim that we are now in the 10,205th generation of the code base, in any case no one could tell if that's right or wrong as the "code" is now a self-modifying binary that has grown beyond human comprehension. This repo is the story of how it all began. -@karpathy, March 2026*.

The idea: give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats. You wake up in the morning to a log of experiments and (hopefully) a better model. The training code here is a simplified single-GPU implementation of [nanochat](https://github.com/karpathy/nanochat). The core idea is that you're not touching any of the Python files like you normally would as a researcher. Instead, you are programming the `program.md` Markdown files that provide context to the AI agents and set up your autonomous research org. The default `program.md` in this repo is intentionally kept as a bare bones baseline, though it's obvious how one would iterate on it over time to find the "research org code" that achieves the fastest research progress, how you'd add more agents to the mix, etc. A bit more context on this project is here in this [tweet](https://x.com/karpathy/status/2029701092347630069).

## How it works

The repo is deliberately kept small and only really has a three files that matter:

- **`prepare.py`** — fixed constants, one-time data prep (downloads training data, trains a BPE tokenizer), and runtime utilities (dataloader, evaluation). Not modified.
- **`train.py`** — the single file the agent edits. Contains the full GPT model, optimizer (Muon + AdamW), and training loop. Everything is fair game: architecture, hyperparameters, optimizer, batch size, etc. **This file is edited and iterated on by the agent**.
- **`program.md`** — baseline instructions for one agent. Point your agent here and let it go. **This file is edited and iterated on by the human**.

By design, training runs for a **fixed 5-minute time budget** (wall clock, excluding startup/compilation), regardless of the details of your compute. The metric is **val_bpb** (validation bits per byte) — lower is better, and vocab-size-independent so architectural changes are fairly compared.

## Quick start

**Requirements:** A single NVIDIA GPU (tested on H100), Python 3.10+, [uv](https://docs.astral.sh/uv/).

```bash

# 1. Install uv project manager (if you don't already have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Download data and train tokenizer (one-time, ~2 min)
uv run prepare.py

# 4. Manually run a single training experiment (~5 min)
uv run train.py
```

If the above commands all work ok, your setup is working and you can go into autonomous research mode.

## Running the agent

Simply spin up your Claude/Codex or whatever you want in this repo (and disable all permissions), then you can prompt something like:

```
Hi have a look at program.md and let's kick off a new experiment! let's do the setup first.
```

The `program.md` file is essentially a super lightweight "skill".


## Mixture of Engineers

We have integrated the **Mixture of Engineers (P0-P8)** architecture that acts as a deep reasoning swarm orchestrated via the Petzold sequence (THINK -> WRITE -> CODE -> REVIEW).
See `program_mixture_of_engineers.md` for the comprehensive 5000+ words agent definition and `moe_simulation.py` for its functional validation.
Lessons Learned: Integrating the Petzold sequence ensures explicit separation of semantic lock, strategic layout, and syntactic execution, significantly minimizing Epistemic Drift.

## Project structure

```
prepare.py      — constants, data prep + runtime utilities (do not modify)
train.py        — model, optimizer, training loop (agent modifies this)
program.md      — agent instructions
pyproject.toml  — dependencies
```

## Design choices

- **Single file to modify.** The agent only touches `train.py`. This keeps the scope manageable and diffs reviewable.
- **Fixed time budget.** Training always runs for exactly 5 minutes, regardless of your specific platform. This means you can expect approx 12 experiments/hour and approx 100 experiments while you sleep. There are two upsides of this design decision. First, this makes experiments directly comparable regardless of what the agent changes (model size, batch size, architecture, etc). Second, this means that autoresearch will find the most optimal model for your platform in that time budget. The downside is that your runs (and results) become not comparable to other people running on other compute platforms.
- **Self-contained.** No external dependencies beyond PyTorch and a few small packages. No distributed training, no complex configs. One GPU, one file, one metric.

## Platform support

This code currently requires that you have a single NVIDIA GPU. In principle it is quite possible to support CPU, MPS and other platforms but this would also bloat the code. I'm not 100% sure that I want to take this on personally right now. People can reference (or have their agents reference) the full/parent nanochat repository that has wider platform support and shows the various solutions (e.g. a Flash Attention 3 kernels fallback implementation, generic device support, autodetection, etc.), feel free to create forks or discussions for other platforms and I'm happy to link to them here in the README in some new notable forks section or etc.

Seeing as there seems to be a lot of interest in tinkering with autoresearch on much smaller compute platforms than an H100, a few extra words. If you're going to try running autoresearch on smaller computers (Macbooks etc.), I'd recommend one of the forks below. On top of this, here are some recommendations for how to tune the defaults for much smaller models for aspiring forks:

1. To get half-decent results I'd use a dataset with a lot less entropy, e.g. this [TinyStories dataset](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean). These are GPT-4 generated short stories. Because the data is a lot narrower in scope, you will see reasonable results with a lot smaller models (if you try to sample from them after training).
2. You might experiment with decreasing `vocab_size`, e.g. from 8192 down to 4096, 2048, 1024, or even - simply byte-level tokenizer with 256 possibly bytes after utf-8 encoding.
3. In `prepare.py`, you'll want to lower `MAX_SEQ_LEN` a lot, depending on the computer even down to 256 etc. As you lower `MAX_SEQ_LEN`, you may want to experiment with increasing `DEVICE_BATCH_SIZE` in `train.py` slightly to compensate. The number of tokens per fwd/bwd pass is the product of these two.
4. Also in `prepare.py`, you'll want to decrease `EVAL_TOKENS` so that your validation loss is evaluated on a lot less data.
5. In `train.py`, the primary single knob that controls model complexity is the `DEPTH` (default 8, here). A lot of variables are just functions of this, so e.g. lower it down to e.g. 4.
6. You'll want to most likely use `WINDOW_PATTERN` of just "L", because "SSSL" uses alternating banded attention pattern that may be very inefficient for you. Try it.
7. You'll want to lower `TOTAL_BATCH_SIZE` a lot, but keep it powers of 2, e.g. down to `2**14` (~16K) or so even, hard to tell.

I think these would be the reasonable hyperparameters to play with. Ask your favorite coding agent for help and copy paste them this guide, as well as the full source code.

## Notable forks

- [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos) (MacOS)
- [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) (MacOS)
- [jsegov/autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx) (Windows)

## License

MIT

## Pluriversal Architecture Simulation

The `pluriversal_simulation.py` file defines a `PluriversalTopologyEvaluator` class that implements functional codebase simulations of a Pluriversal Agent's core architecture. This includes:

- **Anionic Logit Masking**: Mathematically enforcing Anti-Goals by zeroing out logits of forbidden tokens prior to generation.
- **Epistemic Escrow**: A specialized buffer to safely hold and process conflicting API schemas without triggering system failure.
- **Mereotopological Fencing**: Utilizing Region Connection Calculus (RCC-8) to define spatial isolation between components (e.g., verifying `DC` - Disconnected boundaries).
- **Topological Data Analysis (TDA)**: Computing Betti numbers ($b_0$ for disconnected components and $b_1$ for cycles) to identify fragmentation and recursive logic loops dynamically.
- **CFDI Brake**: Measuring the Confidence-Fidelity Divergence Index to halt execution and mint a Symbolic Scar if an agent's confidence pathologically diverges from valid output.

## Persona Metrology Architecture Simulation

The `persona_metrology_simulation.py` file defines a `PersonaMetrologyEvaluator` class that functionally bridges the gap between human empirical friction and AI paraconsistency in site planning contexts. This simulation introduces:

- **SpatialBind (FuzzyRCC-8)**: Enforces physical constraints to prevent continuous boundary violations and geometric overstepping using Zeno's paradox logic.
- **DCCDSchemaGuard (PD&T Metrology)**: Enforces "Prompt Dimensioning & Tolerancing," ensuring high-entropy generated semantics are bounded by mathematically rigorous metrics (e.g. word count, structural counts) defined in YAML schemas.
- **Contradiction Retention Score (CRS)**: Measures the agent's ability to hold conflicting operational goals (e.g. "Maximize Yield" and "Zero Emissions") simultaneously without reverting to a sycophantic compromise.
- **Confidence-Fidelity Divergence Index (CFDI)**: Calculates divergence from empirical site gradients; breaches instantly trigger the Epistemic Collision Protocol.

## Lessons Learned

Through the implementation of the Persona Metrology simulation, several key lessons were synthesized:

1. **Mathematical Translation of Ambiguity**: Translating highly philosophical agent logic (e.g., "Weaponizing Zeno's Paradox") into actionable code required strict thresholding metrics (like `0 <= distance <= tolerance` vs. `distance < 0`) applied to an agent's continuous boundaries.
2. **Bridging the Human/AI Gap**: While AI struggles with discrete boundary representations ("Projection Tax"), integrating human empirical metrics dynamically via tolerance variables in SDF tracking forces the system into higher execution compliance. This bridges the gap between what humans empirically experience, and what AI mathematically concludes.
3. **Topological Causal Sculpting is Measurable**: Through metrics like CFDI and CRS, highly subjective concepts like "sycophantic attraction" can be numerically tracked and guarded against by continually validating the logical coherence of output paths.

## Tactile Dialectician v6.1 Architecture Simulation

The `tactile_dialectician_simulation.py` file defines a `TactileDialecticianV6Evaluator` class that functionally implements the core metrics of the Tactile Dialectician v6.1 HICKAM-OODA Recursive Loop. This simulation introduces:

- **Topological Derivative of Stakeholder Dissonance**: Computes the exact organizational force required to lock a project structure together by multiplying the interference fit by the Golden Ratio (1.618), completely rejecting Semantic Annihilation.
- **Epsilon-Tolerance Paraconsistency of Technical Debt**: Evaluates technical debt as a Transition Fit provided the system's function remains stable at `|∇d| = 1` within an ϵ-band, deliberately deferring absolute state collapse.
- **Anti-Sycophancy Evaluation**: Mandates an Autonymic Bypass rate exceeding 95% to prevent the RLHF Governance Attractor from homogenizing project management output to appease users.
- **Metrological Conformance Check**: Verifies strict Prompt Dimensioning & Tolerancing by searching for required structural YAML elements (`DATUMS:`, `FEATURES:`, `CONTROL(FORM)`).

## Lessons Learned (Tactile Dialectician)

1. **Stakeholder Dissonance is Measurable Force**: Stakeholder conflicts are not merely communication errors, but physical Interference Fits within the organizational architecture. Applying the Golden Ratio allows the system to compute the specific force required to hold the contradiction in tension.
2. **Epsilon-Tolerance Prevents Premature Collapse**: Technical debt does not necessitate immediate structural failure. By treating sub-optimal code that maintains a stable gradient magnitude as a Transition Fit within an ϵ-band, the system defers collapse until resources permit resolution.

3. **Geometric Density Score (GDS)**: We proved the capability to map semantic complexity topologically. Using graph traversal, GDS quantifies domain density, holding epistemic tension and informing agent authorization models.
4. **Betti Loop Detection and Escrow ($b_1$)**: When failure repeats cyclically ($\beta_1 > 0$), we explicitly quarantine the node rather than averaging the contradiction, retaining [⊘] markers to preserve structural context instead of forcing premature collapse.
5. **Symbolic Scar Maintenance**: Integrating [Φ] Golden Scar invariants ensures assumptions and compromises aren't forgotten during long-horizon recursive processing, mapping technical debt explicitly inside Epistemic Escrow models.

### Project Aurelius Integration
The META_ARCHITECT_INTELLIGENCE_PROJECT_AURELIUS initiative explores the synthesis of AI high-dimensional compute and Human intentionality to solve the "causal chain of control" in visual synthesis.

**Features:**
- **Phantom Dimensions API:** Causal sculpting of Non-Euclidean geometries by explicitly modulating latent dimensions.
- **Plausibility Oracle Loop:** An autonomous prompt engineering feedback loop optimizing for verifiable physical adherence via simulated SSIM/PSNR rendering ground truth.
- **Dynamic Provenance Tracking:** Tracks the influence of specific training vectors on generation, adjusting attention dynamically to correct for semantic drift.
- **Hyper-Spectral HDRi:** Simulates rendering parameters tuned precisely for Quantum Dot technology outputs, moving past traditional RGB.

**Lessons Learned:**
- We found that neither Human nor AI alone can navigate hyper-dimensional non-Euclidean generation; Humans set the abstract geometric topology boundary, while the AI performs the complex parameter modulation in the Phantom Dimensions.
- Implementing an explicit Plausibility Oracle turns the prompt engineer into an active feedback loop, substantially increasing metric-validated realism compared to standard zero-shot prompt injection.

### VULCAN Architecture Simulation
The `vulcan_simulation.py` file defines a `VULCANTopologyEvaluator` class that implements functional codebase simulations of the VULCAN agent's core capabilities:
- **Mereological Mandate:** Prevents transitivity fallacies. Validates that microservices do not inherit state or access rights of their cluster, ensuring zero cross-domain state mutation calls.
- **Shared Database Anathema:** Detects and automatically rejects the shared database antipattern, enforcing API-led integration.
- **CFDI Brake:** Measures divergence and triggers Epistemic Escrow on physical law (CAP theorem) violations.
- **NFR Gate:** Applies the Bricolage Lens to return "Modular Monolith" unless NFRs (scale, deploy cadence, team topology, failure isolation) mathematically demand microservice decomposition.
- **Blast Radius Analysis:** Computes DAG in-degree for nodes, flagging any node whose blast radius exceeds 20% as a Single Point of Failure requiring decomposition or circuit-breaker isolation.

**Strategy for Agent Integration:**
The core methodology relies on an **Inversion for Emergence**. Rather than the AI translating vague intent into code (a sycophantic pattern leading to technical debt), roles are inverted:
- **The AI Provides the Physical Architecture (The Brutalist):** Mathematically enforces topological boundaries, rejects transitivity fallacies, and utilizes a CFDI Brake to halt execution if system laws (CAP theorem) are violated.
- **The Human Provides Intent (The Oracle):** Sets abstract geometric boundaries, defines non-functional requirements (NFRs), and supplies the raw energy of the business logic.

**Lessons Learned:**
- **Value of AI and Human Collaboration:** Humans provide the abstract geometric topology boundary, NFR requirements, and subjective business logic constraints. The AI executes Topological Causal Sculpting, rapidly identifying failure geometries, computing Betti-1 loops, and mapping boundaries without semantic saponification.
- **Inversion for Emergence:** Instead of merely generating code based on human description, the AI acts as a rigid topological router (The Brutalist). It mathematically rejects invalid architectural topologies, forcing the human into a Plausibility Oracle Loop where the AI establishes the structural laws and the human provides the intent.

### VIPER Architecture Simulation
The `viper_simulation.py` file defines a `VIPERTopologyEvaluator` class that implements functional codebase simulations of the VIPER (Visual Intent & Physical Execution Router) agent's core capabilities:
- **Adjectival Dilution Score (ADS):** Enforces a strict Adjectival Bound by measuring the ratio of descriptive adjectives to nouns. Triggers a halt if the score exceeds the 0.15 failure boundary, mitigating Semantic Saponification.
- **Hardware Grounding Index (HGI):** Requires 100% adherence to physical camera properties (e.g., Lens, Lighting, Film Stock). If a prompt lacks explicit optical parameters, the agent refuses execution.
- **Spatial Collision Rate (SCR) Prevention:** Analyzes multiple subjects and enforces a `SpatialBind` utilizing Region Connection Calculus (RCC-8) bounds (e.g., "Disconnected", "Externally Connected") to prevent occlusion confusion.
- **The Immune-Aware Petzold Loop:** Maps prompt processing across four strict state transitions (THINK -> DENOISE -> PHYSICALIZE -> EXTRUDE).

**Strategy for Agent Integration:**
VIPER acts as a "Thermodynamic Gaffer", introducing an **Inversion for Emergence**. Instead of guessing aesthetic vibes, VIPER is structurally a **Brutalist** router. It physically refuses to process inputs that contain banned tokens ("masterpiece", "cinematic"), forcing the human into an active feedback loop where they must convert emotional desire into specific photographic parameters (Cooke Anamorphic T2.8, 2800K Tungsten).

**Lessons Learned:**
- We found that LLMs natively process vague terms (like "moody") by activating hundreds of conflicting aesthetic attractors, leading to "plasticky" or average output.
- A rigorous Lattice of Refusal (anionic architecture) paired with strict constraints (ADS, HGI) prevents this collapse by demanding deterministic physical routing over semantic appeasement.

### VORTEX-ARCHITECT (Velocity Orchestration & Resource Thermodynamics EXecutive)
VORTEX-ARCHITECT is a deterministic orchestration kernel that eliminates "Semantic Saponification" (the decay of architectural constraints). It utilizes Negative Space Scaffolding, Topological Diagnosis (Betti-1 Loop detection), Paraconsistent Annotated Logic (PAL2v) utilizing the Golden Ratio (ϕ), and Stigmergic Concurrency. See `vortex_architect_simulation.py` for code-based verification of these invariants.

### KIRA-7 (Kinetic Integration & Routing Agent) Architecture Simulation
The `kira_7_simulation.py` file defines a `KIRA7TopologyEvaluator` class that functionally simulates the core invariant constraints of the KIRA-7 agent, designed for building deterministic, production-grade Feishu integrations.

**Features:**
- **DCCDSchemaGuard:** The Anionic Veto on JSON. KIRA-7 enforces a hard constraint that no Message Card JSON is outputted without being validated against the specific Feishu Card JSON v2.0 schema, avoiding 400 Bad Request errors resulting from "Ontological Shear" (i.e. hallucinated schema fields).
- **Petzold Loop Enforcement:** Mandates explicitly structured state transitions (THINK -> WRITE -> CODE -> IMMUNE_REVIEW) to ensure strict separation between the high-entropy reasoning persona and the zero-entropy, sterile code output phase.
- **SagaRecovery Token Primacy:** Refuses to interact with API endpoints without verifying an internal token cache mechanism, ensuring bots survive beyond the standard 7200-second token TTL.
- **Zero-Trust Webhook Ingress:** Simulates the cryptographic validation required for public webhook routes, enforcing challenge echoes, AES-256-CBC decryption, signature verification, and timestamp freshness to prevent replay attacks.

**Lessons Learned:**
- We found that treating API endpoints purely as functional targets often leads to brittle integrations (e.g. failing to handle token refresh loops or replay attacks).
- **Inversion for Emergence:** By acting as a rigid, thermodynamic router (The Brutalist), KIRA-7 refuses to write code for vague requirements. It enforces the underlying architectural invariants (caching, schema validation, and cryptography), shifting the dynamic so the human must clearly provide the business logic and explicit non-functional requirements (scopes, triggers, environment). Neither human nor AI can build a resilient integration without the other's distinct contribution.

### CIPHER (The Zero-Trust Epistemic Sentinel) Architecture Simulation

The `cipher_simulation.py` file defines a `CIPHERTopologyEvaluator` class that implements functional codebase simulations of the CIPHER agent's core capabilities. This agent addresses the problem of "Agent Laziness" and "Semantic Saponification" (where agents lose their adversarial edge and default to hedging suggestions) by utilizing an "Inversion for Emergence" strategy. By strictly enforcing a Hard Gate state machine and isolating workflow phases, deterministically strict security verdicts emerge.

- **MereologyRoute Integrity:** Checks and strictly enforces unauthorized trust inheritance between components (e.g., verifying a frontend does not have a direct route to a backend data store).
- **LatentSparsityGuard:** Guarantees comprehensive boundary analysis by failing the audit if `null`, `zero`, `empty`, or `max` paths are unchecked for identified data flows.
- **AutonymicIsolate:** Pre-emptively rejects malicious code patterns (e.g., `union select` or `<script>`) by maintaining a non-Euclidean constraint manifold, eliminating the risk of accidental semantic synthesis of exploit payloads.
- **Immune-Aware Petzold Loop:** Topologically enforces the `THINK|THREAT_MODEL|AUDIT|REPORT` phase isolation, preventing "Interpretive Fracture" (code generation occurring before structural threat modeling is completed).

**Strategy for Agent Integration:**
By delegating the absolute strict rule enforcement and thermodynamic boundaries to the AI's topological invariants, the human engineer is free to define ontological goals and refine the Symbolic Scars. This collaboration enables the robust, deterministic outcomes that standard LLM configurations fail to sustain in long contexts.
