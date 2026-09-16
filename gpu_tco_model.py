"""Own vs rent vs API: LLM inference cost model for a 4x H100 PCIe server.
Every input below is a public figure (Sept 2026) or arithmetic on public figures.
Run: python gpu_tco_model.py   -> prints results, writes CSVs to data/.

INPUTS AND SOURCES
  gpu_price  $27,500  midpoint of $25K-$30K H100 80GB PCIe card range (Runpod H100 guide, Sept 2026)
  host       $10,414  Dell R760xa barebone with 4-GPU kit, Newegg listing (excludes CPUs, memory,
                      storage, power supplies -> capex is a LOWER BOUND)
  kw         2.1      4 x 350 W H100 PCIe TDP (Runpod) + 2 x 350 W Xeon TDP (R760xa spec, IT Creations);
                      rated maximums, excludes memory/storage/fans
  pue        1.52     Uptime Institute Global Data Center Survey 2026
  kwh        $0.2575  EIA Electric Power Monthly, California commercial, Apr 2026
  colo       $194.95  per kW-month, CBRE national average colocation lease rate
                      (Silicon Valley range $180-$275)
  life       5 yr     Amazon 10-K: server useful life revised 6 -> 5 yrs (Jan 2025), citing AI;
                      Microsoft/Alphabet use 6; critics (e.g., Michael Burry) argue 2-3
  residual   $0       straight-line depreciation to zero
  rate       $3.29    Lambda H100 PCIe on-demand list price; 38-provider median $3.36 (GetDeploying, Sept 16, 2026)
  throughput 3,400 output tok/s (256 concurrent) and 1,400 (64 users x ~22 tok/s), vLLM,
             Llama 3.1 70B FP8, 4x H100 SXM (GeneralCompute benchmark, Jun 2026). Measured on NVLink
             hardware, so a PCIe server is likely slower.
  API prices per 1M tokens (input/output): DeepInfra 0.10/0.32 (OpenRouter, Aug 2026);
             AWS Bedrock 0.72, Fireworks 0.90, Together 1.04 (Markaicode pricing guides, Sept 2026)
Utilization is not assumed: the model solves for the break-even and reports a grid.
"""
import csv, os

H = 8760
A = dict(gpus=4, gpu_price=27_500, host=10_414, kw=2.1, pue=1.52, kwh=0.2575, colo=194.95, life=5, rate=3.29)
RATES = [("Runpod PCIe, community", 1.99), ("Runpod PCIe, secure", 2.89), ("Lambda PCIe", 3.29),
         ("Median, 38 providers", 3.36), ("Lambda (CloudZero)", 3.99), ("CoreWeave", 4.25), ("Azure, high end", 6.98)]
IN_TOK, OUT_TOK = 1024, 256
WORKLOADS = {"batch": 3400, "interactive": 1400}
APIS = {"DeepInfra": (0.10, 0.32), "AWS Bedrock": (0.72, 0.72), "Fireworks": (0.90, 0.90), "Together": (1.04, 1.04)}

def capex(a): return a["gpus"] * a["gpu_price"] + a["host"]
def energy(a): return a["kw"] * a["pue"] * H * a["kwh"]
def colo(a): return a["kw"] * a["colo"] * 12
def annual_owned(a): return capex(a) / a["life"] + colo(a) + energy(a)
def tco(a): return capex(a) + a["life"] * (colo(a) + energy(a))
def owned_per_hr(a, u): return annual_owned(a) / (a["gpus"] * H * u)
def breakeven(a, rate=None): return annual_owned(a) / (a["gpus"] * H * (rate or a["rate"]))

def owned_per_1k_req(a, tps, u): return annual_owned(a) / (tps / OUT_TOK * H * 3600 * u) * 1000
def rental_per_1k_req(a, tps): return a["gpus"] * a["rate"] / (tps / OUT_TOK * 3600) * 1000
def api_per_1k_req(i, o): return (IN_TOK * i + OUT_TOK * o) / 1e6 * 1000
def breakeven_vs_api(a, tps, i, o): return owned_per_1k_req(a, tps, 1.0) / api_per_1k_req(i, o)

def fmt(be): return "never" if be > 1 else f"{be:.1%}"

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    print(f"Capex ${capex(A):,.0f} | energy ${energy(A):,.0f}/yr | colo ${colo(A):,.0f}/yr | "
          f"annual owned ${annual_owned(A):,.0f} | {A['life']}-yr TCO ${tco(A):,.0f}")
    print(f"Break-even vs rental at ${A['rate']}: {fmt(breakeven(A))}")

    print("\nOwned $/GPU-hr by utilization")
    with open("data/utilization_grid.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["utilization", "owned_per_gpu_hr", "rental_per_gpu_hr"])
        for u in (0.25, 0.5, 0.75, 1.0):
            w.writerow([u, round(owned_per_hr(A, u), 3), A["rate"]]); print(f"  {u:.0%}: ${owned_per_hr(A, u):.2f}")

    print("\nBreak-even by rental rate")
    with open("data/sensitivity_rate.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["provider", "rate_per_gpu_hr", "breakeven_util"])
        for n, r in RATES:
            be = breakeven(A, r); w.writerow([n, r, round(be, 4)]); print(f"  {n} ${r}: {fmt(be)}")

    print("\nBreak-even by input range (other inputs at base)")
    with open("data/sensitivity_inputs.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["input", "value", "source", "breakeven_util"])
        for key, val, src in [("life", 3, "critic view"), ("life", 5, "Amazon 10-K"), ("life", 6, "Microsoft/Alphabet"),
                              ("gpu_price", 25000, "range low"), ("gpu_price", 30000, "range high"),
                              ("colo", 180, "Silicon Valley low"), ("colo", 275, "Silicon Valley high"),
                              ("kwh", 0.1351, "EIA US commercial avg")]:
            be = breakeven({**A, key: val}); w.writerow([key, val, src, round(be, 4)])
            print(f"  {key}={val} ({src}): {fmt(be)}")

    print("\nToken economics, $ per 1,000 requests (1,024 in / 256 out)")
    with open("data/token_economics.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["workload", "option", "cost_per_1k_req_or_owned_at_100pct", "owned_breakeven_util"])
        for wl, tps in WORKLOADS.items():
            o100, r = owned_per_1k_req(A, tps, 1.0), rental_per_1k_req(A, tps)
            print(f"  {wl} ({tps} tok/s): owned at 100% ${o100:.3f}, rental ${r:.3f}")
            w.writerow([wl, "owned_at_100pct", round(o100, 4), ""]); w.writerow([wl, "rental", round(r, 4), round(breakeven(A), 4)])
            for n, (i, o) in APIS.items():
                be = breakeven_vs_api(A, tps, i, o)
                print(f"    vs {n} ${api_per_1k_req(i, o):.3f}: owning wins above {fmt(be)}")
                w.writerow([wl, n, round(api_per_1k_req(i, o), 4), round(be, 4)])
