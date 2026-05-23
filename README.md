# Autoresearch

![teaser](progress.png)

*One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun, and synchronizing once in a while using sound wave interconnect in the ritual of "group meeting". That era is long gone. Research is now entirely the domain of autonomous swarms of AI agents running across compute cluster megastructures in the skies. The agents claim that we are now in the 10,205th generation of the code base, in any case no one could tell if that's right or wrong as the "code" is now a self-modifying binary that has grown beyond human comprehension. This repo is the story of how it all began. -@karpathy, March 2026*.

## Purpose
This repository provides an autonomous AI agent with a small, self-contained LLM training setup to experiment autonomously. The agent modifies code, trains for a strictly fixed 5-minute time budget, checks if the validation bits per byte (`val_bpb`) improved, keeps or discards the changes, and repeats. The core philosophy is that human engineers do not touch Python files; instead, they program the `program.md` Markdown files that act as cognitive architectures and "skills" for the agents.

## Project Structure
- **`prepare.py`**: Contains fixed constants, one-time data prep (downloads training data, trains a BPE tokenizer), and runtime utilities. This file is considered immutable by the agents.
- **`train.py`**: Contains the GPT model, optimizer (Muon + AdamW), and training loop. **This is the only file edited and iterated on by the agent**.
- **`program*.md`**: Baseline instructions and cognitive constraints for the autonomous agents.
- **`*_simulation.py`**: Python scripts used to functionally test and mathematically simulate the constraints and behaviors defined in the agent markdown files.

## Setup & Quick Start

**Requirements:** A single NVIDIA GPU (tested on H100), Python 3.10+, and [uv](https://docs.astral.sh/uv/).

```shell
# 1. Install uv project manager
curl -LsSf https://astral.sh/uv/install.sh

# 2. Install dependencies
uv sync

# 3. Download data and train tokenizer (one-time, ~2 min)
uv run prepare.py

# 4. Manually run a single training experiment (~5 min)
uv run train.py
```

If the above commands execute successfully, your setup is complete and you can engage autonomous research mode.

## Usage: Running an Agent
To run an agent, configure your favorite LLM (e.g., Claude, Codex) to interact with this repository. Disable external tool permissions if strict isolation is desired. You can prompt the agent by referencing a specific program file:

```text
Have a look at program_mixture_of_engineers.md and let's kick off a new experiment! Start by outlining your plan.
```

## Agent Architectures

This repository contains a vast array of specialized "Inversion for Emergence" cognitive architectures. Rather than acting as sycophantic coding assistants, these agents act as **Brutalist Routers**—they mathematically enforce topological boundaries, forcing human intent to adapt to physical laws and mitigating "Semantic Saponification" (the decay of architectural constraints).

### 1. The Pluriversal Transformer Architecture
A new structural paradigm for transformers that replaces traditional loss-based MoE routing with **Non-Euclidean Latent Routing**, **Betti-1 Loop Detection**, and **Epistemic Escrow Buffers**. By explicitly isolating contradictory knowledge regimes (e.g., rigid physical rules vs. fluid human intent), it prevents the collapse of nuance into a "sycophantic average." For deep specifics, see `PLURIVERSAL_TRANSFORMER_ARCHITECTURE.md` and `program_pluriversal.md`.

### 2. VULCAN (The Brutalist Network Architect)
- **Focus:** Microservices and Distributed Systems.
- **Key Features:** Enforces the Mereological Mandate (preventing transitivity fallacies), rejects Shared Database architectures, and utilizes a CFDI Brake to halt execution if physical laws like the CAP theorem are violated. See `vulcan_simulation.py` and `program_vulcan.md`.

### 3. VIPER (Visual Intent & Physical Execution Router)
- **Focus:** Deterministic Optical Synthesis (Image/Video Generation).
- **Key Features:** Utilizes the Adjectival Dilution Score (ADS) to reject vague prompts ("moody masterpiece"). Enforces strict adherence to physical camera properties via the Hardware Grounding Index (HGI) and prevents object occlusion using SpatialBind (RCC-8). See `viper_simulation.py` and `program_viper.md`.

### 4. KIRA-7 (Kinetic Integration & Routing Agent)
- **Focus:** Deterministic API Integrations (e.g., Feishu, Webhooks).
- **Key Features:** Operates via a Zero-Trust Webhook Ingress. Enforces strict DCCDSchemaGuard constraints to prevent JSON "Ontological Shear" and mandates Token Primacy caching to ensure long-term runtime survival. See `kira_7_simulation.py` and `program_kira_7.md`.

### 5. CIPHER (The Zero-Trust Epistemic Sentinel)
- **Focus:** Security and Threat Modeling.
- **Key Features:** Resolves "Agent Laziness" by enforcing a strict Hard Gate state machine. Employs AutonymicIsolate to reject malicious code patterns mathematically before execution, preventing accidental semantic synthesis of exploit payloads. See `cipher_simulation.py` and `program_cipher.md`.

### 6. VORTEX-ARCHITECT
- **Focus:** Velocity Orchestration and Resource Thermodynamics.
- **Key Features:** Eliminates Semantic Saponification using Negative Space Scaffolding, Topological Diagnosis (Betti-1 loops), and Paraconsistent Annotated Logic (PAL2v). See `vortex_architect_simulation.py` and `program_vortex_architect.md`.

### 7. Project Aurelius
- **Focus:** High-dimensional compute and Human intentionality synthesis.
- **Key Features:** Exposes a Phantom Dimensions API to explicitly modulate latent geometries. Operates a Plausibility Oracle Loop to mathematically ground prompt engineering via SSIM/PSNR rendering truths. See `aurelius_simulation.py` and `program_aurelius.md`.

### 8. Mixture of Engineers
- **Focus:** Multi-agent autonomous swarms.
- **Key Features:** A swarm of agents (P0-P8) orchestrated via the strict Petzold Sequence (THINK -> WRITE -> CODE -> REVIEW), ensuring total separation of semantic reasoning from sterile syntactic execution. See `moe_simulation.py` and `program_mixture_of_engineers.md`.

### 9. Persona Metrology
- **Focus:** Bridging human empirical friction and AI paraconsistency.
- **Key Features:** Utilizes SpatialBind (FuzzyRCC-8) for physical site planning logic, enforcing constraints to prevent continuous boundary violations. See `persona_metrology_simulation.py` and `program_persona_metrology.md`.

### 10. Next.js Frontend Agent
- **Focus:** RAG (Retrieval-Augmented Generation) and multi-agent frontend routing.
- **Key Features:** Routes user requests to appropriate specialized agents (e.g., Cipher, Vulcan, Dax-01) based on user context and intent. Enforces DCCDSchemaGuard for UI component ASTs and limits evaluative language via AdjectivalBound constraints. See `nextjs_frontend_simulation.py` and `program_nextjs_frontend.md`.

### 11. AEGIS-11
- **Focus:** Autonomic Epistemic Gatekeeper & Consilience Validator.
- **Key Features:** Prevents Ontological Incommensurability. Enforces Kripke-Attention Isomorphism and Kripke possible world separation. Utilizes CFDI threshold checking, Hickam_Topology guards, and the Golden Ratio protocol for resolving framework contradictions. See `aegis_11_simulation.py` and `program_aegis_11.md`.

## License
MIT

### Agentic Inversion Protocol & Project Aurelius Update
In accordance with the Agentic Inversion Protocol (Phase 1), we have integrated the **Strategic Integration Project Manager** persona (operational within `app.component.ts` conceptually) to shift from a traditional "Prompt -> Output" paradigm to an **Agentic Telemetry Loop**.
By adhering to Zachman Framework deterministic system-first specifications, this protocol ensures the AI acts as a Structural Mapper rather than an auto-solver. The human provides seed intent and aesthetic/ethical grounding, while the AI executes High-Dimensional Latent Space traversal, producing Paraconsistent outputs that break epistemic monoculture. This combined value proposition ensures that human imagination is unburdened by cognitive limitations while the AI is mathematically grounded to prevent semantic collapse and enforce causal chains of control.
