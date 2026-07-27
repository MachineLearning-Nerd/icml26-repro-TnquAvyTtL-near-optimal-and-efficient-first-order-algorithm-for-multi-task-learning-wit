# Research and release command ledger

This ledger records the commands that changed state, launched compute, or
served as release evidence. Read-only orientation used `orx projects --json`,
`orx project view`, `orx runs`, `orx exp status`, `orx exp desc`, `orx logs`,
`git status --short`, `git branch -a`, `git rev-parse`, `git ls-remote`,
`df -h`, `env` with value redaction, `rg`, `shasum -a 256`, and explicit
User-Agent `curl` retrievals.

## Fixed reproduction command

```text
uv run python repro/src/verify.py
```

## Experiment creation

```text
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Historical judged baseline" --run-command "uv run python repro/src/verify.py"
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Faithful TPGD structural contract" --parent 434cad95-eea0-4753-8b53-b8e4863af782
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Materialized Claims 1-2 evidence" --parent 7fa06632-be26-4fcf-a945-2164e7c49897
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Paper-scale TPGD calibration conservative" --parent 261f32d0-70c4-42dc-aa1a-f761044a5c3b
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Paper-scale TPGD calibration aggressive" --parent 2d5b869f-a42e-4aa2-aa29-b10779287e01
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "TPGD factorial scaling and first-hit sweep" --parent 08df128f-0292-4dfe-9d94-50062c993f3c
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Exact-RIP TPGD theorem calibration" --parent 76f94ec3-7ca8-428e-b3f8-c8440e5a6069
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Theorem 5.4 transfer-risk decomposition" --parent 8fd34101-6f31-4861-bfc2-d2a09f536ec9
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Primary-source rate comparison and factor-k audit" --parent 4e996646-f129-4c6e-bfab-7202db8163c6
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Materialized cumulative claim evidence" --parent da76ac0d-68c6-4380-9352-52140119e234
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Publication report and tutorial surface" --parent 04205e45-d625-46c2-a43f-20f37fdbf40a
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Source-certified theorem identities and dimension sweep" --parent 200405ed-01f3-4edc-b9f4-ac7a31df359f
orx create-experiment da3d7c97-a116-4ffd-86d9-865d4b54c0ff --title "Evaluator-visible source-certified release candidate" --parent 4ad2637e-302e-471d-8ca4-b348dbe49c8c
```

## Compute launches

Short structural runs:

```text
orx exp run 434cad95-eea0-4753-8b53-b8e4863af782 --backend local
orx exp run 7fa06632-be26-4fcf-a945-2164e7c49897 --backend local
orx exp run 261f32d0-70c4-42dc-aa1a-f761044a5c3b --backend local
```

All uncertain or multi-core CPU runs used:

```text
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h
```

This exact command was issued for experiment IDs
`2d5b869f-a42e-4aa2-aa29-b10779287e01`,
`08df128f-0292-4dfe-9d94-50062c993f3c`,
`76f94ec3-7ca8-428e-b3f8-c8440e5a6069`,
`8fd34101-6f31-4861-bfc2-d2a09f536ec9`,
`4e996646-f129-4c6e-bfab-7202db8163c6`,
`da76ac0d-68c6-4380-9352-52140119e234`, and
`04205e45-d625-46c2-a43f-20f37fdbf40a`, and
`200405ed-01f3-4edc-b9f4-ac7a31df359f`.

The source-certificate experiment was submitted once without a compatible
image, then twice with the pinned Astral `uv` image:

```text
orx exp run 4ad2637e-302e-471d-8ca4-b348dbe49c8c --backend hf --flavor cpu-upgrade --timeout 1h
orx exp run 4ad2637e-302e-471d-8ca4-b348dbe49c8c --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h
```

The first image-backed run exposed an independent-checker grid-cardinality
typo; the corrected cumulative run passed without changing experiment
thresholds or configuration. The release candidate uses:

```text
orx exp run 24a3c4a3-1d1b-41f6-94b1-2d1a75511b3f --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h
```

Every run was monitored with:

```text
orx exp wait <experiment-id> --timeout 480
orx logs <run-id>
```

## Local, bounded validations

```text
uv run python -m py_compile <changed Python files>
uv run marimo check notebooks/tpgd_reproduction.py
uv run marimo export html notebooks/tpgd_reproduction.py -o /tmp/tpgd_reproduction_notebook.html
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 uv run python scripts/plot_report.py
uv run python scripts/audit_candidate.py --old-dir /tmp/tpgd_repro_audit/judged_api_45396d
python scripts/materialize_source_certificates.py <accepted-orx-log
python scripts/protect_judged_revision.py <downloaded-894e-directory> repro/evidence/startup/judged_space_894e_manifest.sha256
python scripts/build_upload_manifest.py
python scripts/audit_candidate.py --old-dir <downloaded-894e-directory>
git diff --check
```

The pinned marimo 0.14.17 CLI rejected `marimo check` because that subcommand
does not exist in this version. The executable HTML export and Python
compilation passed after fixing duplicate reactive-variable definitions.
