# Own, Rent, or API: LLM Inference Cost Findings

*Data as of September 2026. Every input is a dated public figure; sources are in the README.*

**Question:** When does an owned 4× H100 PCIe server cost less than renting GPUs or calling a hosted Llama 70B API?

## Findings

1. **Owned vs rented:** owning wins above **31.4%** utilization against Lambda's $3.29/GPU-hour PCIe list price. Against Runpod's $1.99–$2.89 rates, the threshold rises to 36–52%. Against Azure's $6.98, it falls to 15%.
2. **Depreciation life drives the answer more than price inputs do.** A 3-year life puts break-even at 45%; a 6-year life puts it at 28%. The published range for H100 price, colocation, and electricity each shifts break-even by less than 3 points.
3. **The cheapest API beats owning in most cases.** For Llama 3.x 70B, owning beats DeepInfra only above 47% utilization on batch work, and never on interactive chat. Against Bedrock, Fireworks, and Together, owning wins above 7–23%.
4. **Batching determines self-hosting economics.** The same server produced ~3,400 output tok/s at 256 concurrent requests versus ~1,400 at 64 chat users, a 2.4× difference in cost per request.

## Cost build

| Line | Annual |
|---|---|
| Depreciation: ($110,000 GPUs + $10,414 chassis) / 5 yr | $24,083 |
| Colocation: 2.1 kW × $194.95 × 12 | $4,913 |
| Energy: 2.1 kW × 1.52 × 8,760 h × $0.2575 | $7,200 |
| **Total** | **$36,196** |

Break-even = $36,196 / (4 × 8,760 × $3.29) = 31.4%.

## Self-host vs API (cost per 1,000 requests, 1,024 in / 256 out)

| Option | Batch | Interactive |
|---|---|---|
| Owned at 100% utilization | $0.086 | $0.210 |
| Rented at $3.29/hr | $0.275 | $0.668 |
| DeepInfra | $0.184 | $0.184 |
| AWS Bedrock | $0.922 | $0.922 |
| Fireworks | $1.152 | $1.152 |
| Together | $1.331 | $1.331 |

## Implications

- For a team already paying premium API rates (Bedrock, Fireworks, Together), owning pays off at low utilization, even with the understated server cost.
- For interactive chat, the cheapest API wins outright. Self-hosting needs a reason other than cost, such as data residency.
- Before buying, the numbers to pin down are measured utilization, a full server quote, PCIe throughput, and the depreciation life the finance team will use.

## Why these results are optimistic for ownership

- The chassis price excludes CPUs, memory, storage, and power supplies.
- Throughput comes from NVLink-connected SXM GPUs, which are faster than PCIe.
- Staff time, networking, and installation are excluded.

Each of these raises owned cost, so real break-evens will be higher than shown.
