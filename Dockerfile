# D2: Dockerfile — Multi-stage, CUDA 12.4, pinned deps
# Compliant: RULE R5 (immutable), RULE R12 (pinned reqs)

# ── Stage 1: Builder ──────────────────────────────────────
FROM nvidia/cuda:12.4.1-cudnn9-devel-ubuntu22.04 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.lock .

# RULE R12: Install from pinned lock file ONLY
RUN pip install --no-cache-dir --require-hashes -r requirements.lock

COPY src/ ./src/
COPY configs/ ./configs/

# ── Stage 2: Production Runtime ───────────────────────────
FROM nvidia/cuda:12.4.1-cudnn9-runtime-ubuntu22.04 AS production

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user — security invariant
RUN groupadd -r mluser && useradd -r -g mluser mluser

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /build/src ./src
COPY --from=builder /build/configs ./configs

USER mluser

# RULE R8: Reproducibility seed enforced at runtime via ENV
ENV PYTHONHASHSEED=42
ENV CUBLAS_WORKSPACE_CONFIG=:4096:8

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:8080/health').raise_for_status()"

ENTRYPOINT ["python3", "-m", "src.inference_server"]