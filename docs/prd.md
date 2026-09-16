# PRD: Inference Cost Advisor

*Author: Mansi Shiroya · Sept 2026*

## Problem

Teams serving LLMs choose between hosted APIs, rented GPUs, and owned servers, and the public prices for each vary widely. As of September 2026:
- H100 rental list prices run from $1.99 to $6.98 per GPU-hour.
- Llama 3.3 70B API prices run from $0.10/$0.32 to $1.04 per million tokens.

With spreads that wide, the right choice depends on a team's own utilization and workload shape, which a single list-price comparison can't capture.

## Target user

ML platform or infrastructure owners responsible for LLM serving costs, and the finance partners who approve capex versus opex.

## Jobs to be done

1. Find the utilization at which buying GPUs pays off.
2. Compare self-hosting against specific APIs on cost per request.
3. Show finance a model where every input is sourced and adjustable.

## What v1 does

- Owned-server cost: depreciation, colocation, and energy
- Break-even utilization against rental, by provider rate
- Break-even across the published range of each input
- Self-host vs API cost per 1,000 requests for batch and interactive workloads
- Dated sources for every default, plus a reproducible Python model

## Not in v1

- Full server bill of materials
- Staff time
- Financing and taxes
- Reserved or negotiated pricing
- Model quality comparison
- Live price feeds

## Success metrics

Targets will be set after discovery interviews establish a baseline.

- **North star:** sessions where the user changes both utilization and workload inputs
- **Trust:** share of sessions that open the sources section
- **Outcome:** share of surveyed users who say the tool informed a real decision
- **Guardrail:** reported input or math errors, and time to fix

## Design choice

The break-even ranges from 7% to "never" depending on which alternative a team compares against. So the tool leads with break-even thresholds and comparison tables, not a single own-or-rent verdict.

## Open questions for discovery

- What utilization do teams actually measure, and how?
- What does a complete 4× H100 PCIe server cost in a real quote?
- How much slower is PCIe serving than the SXM benchmark?
- What depreciation life do finance teams use for GPUs?
- Which costs outside the bill do teams report missing?

## v2 candidates (prioritize after discovery)

1. Full server bill of materials from a vendor quote
2. Staff time input
3. Reserved and committed-use pricing
4. Upload usage logs to measure utilization
5. Model picker with benchmark-backed throughput
