import json
import math
import statistics as stats
from pathlib import Path

def load(filename):
    return json.loads(Path(filename).read_text(encoding="utf-8"))

def index(rows):
    result = {str(row["id"]): row for row in rows}
    if len(result) != len(rows):
        raise ValueError("Duplicate question IDs")
    return result

local_eval = index(load("eval_results_local.json"))
cloud_eval = index(load("eval_results_cloud.json"))
local_outputs = index(load("pipeline_outputs_local.json"))
cloud_outputs = index(load("pipeline_outputs_cloud.json"))
original_outputs = load("pipeline_outputs.json")

def normalize(value):
    return " ".join(str(value).casefold().split())

def original_for(question):
    matches = [
        r for r in original_outputs
        if normalize(r["question"]) == normalize(question)
    ]
    rated = [r for r in matches if r.get("rating_note")]
    return (rated or matches)[-1] if matches else {}

ids = sorted(
    set(local_eval) & set(cloud_eval),
    key=lambda x: int(x) if x.isdigit() else x
)

def mean_error(values):
    if not values:
        return None, None
    average = stats.mean(values)
    error = (
        2 * stats.stdev(values) / math.sqrt(len(values))
        if len(values) > 1 else None
    )
    return average, error

def formatted(values):
    avg, error = mean_error(values)
    if avg is None:
        return "N/A"
    if error is None:
        return f"{avg:.3f} (n=1)"
    return f"{avg:.3f} +/- {error:.3f}"

metrics = [
    "Faithfulness",
    "Answer Relevancy",
    "Contextual Relevancy",
    "Contextual Recall",
    "Contextual Precision",
]

lines = [
    "# Day 12 - Local vs Cloud Comparison",
    "",
    "Difference = cloud minus local; uncertainty = 2 x standard error.",
    "",
    "| Metric | n | Local mean +/- 2SE | Cloud mean +/- 2SE | Paired difference +/- 2SE | Verdict |",
    "|---|---:|---:|---:|---:|---|",
]

for name in metrics:
    pairs = []

    for qid in ids:
        left = local_eval[qid]["metrics"].get(name, {}).get("score")
        right = cloud_eval[qid]["metrics"].get(name, {}).get("score")

        if (
            isinstance(left, (int, float))
            and isinstance(right, (int, float))
            and math.isfinite(left)
            and math.isfinite(right)
        ):
            pairs.append((float(left), float(right)))

    local_scores = [a for a, b in pairs]
    cloud_scores = [b for a, b in pairs]
    differences = [b - a for a, b in pairs]

    avg, error = mean_error(differences)

    if avg is None or error is None or avg - error <= 0 <= avg + error:
        verdict = "no clear difference"
    elif avg > 0:
        verdict = "cloud higher"
    else:
        verdict = "local higher"

    lines.append(
        f"| {name} | {len(pairs)} | "
        f"{formatted(local_scores)} | "
        f"{formatted(cloud_scores)} | "
        f"{formatted(differences)} | {verdict} |"
    )

lines += [
    "",
    "## Generation statistics",
    "",
    "| Measure | Local | Cloud |",
    "|---|---:|---:|",
]

def generation_stats(rows, use_original=False):
    times = []
    tokens = []
    empty = 0
    non_stop = 0

    for row in rows.values():
        raw = original_for(row["question"]) if use_original else {}
        merged = {**raw, **row}

        milliseconds = merged.get("generation_time_ms")
        if milliseconds is not None:
            times.append(float(milliseconds) / 1000)
        elif merged.get("latency_seconds") is not None:
            times.append(float(merged["latency_seconds"]))

        token_count = merged.get("generated_tokens")
        if isinstance(token_count, (int, float)):
            tokens.append(token_count)

        answer = merged.get("actual_answer", merged.get("answer", ""))
        if not str(answer or "").strip():
            empty += 1

        finish = merged.get("finish_reason")
        if finish not in (None, "stop"):
            non_stop += 1

    return {
        "median": stats.median(times) if times else None,
        "slowest": max(times) if times else None,
        "tokens": stats.mean(tokens) if tokens else None,
        "empty": empty,
        "non_stop": non_stop,
    }

local_stats = generation_stats(local_outputs, use_original=True)
cloud_stats = generation_stats(cloud_outputs)

def number(value, decimals=2):
    return f"{value:.{decimals}f}" if value is not None else "N/A"

for label, key, suffix in [
    ("Median generation time", "median", " s"),
    ("Slowest generation time", "slowest", " s"),
    ("Average completion tokens", "tokens", ""),
    ("Empty answers", "empty", ""),
    ("Non-stop finishes", "non_stop", ""),
]:
    lines.append(
        f"| {label} | {number(local_stats[key])}{suffix} | "
        f"{number(cloud_stats[key])}{suffix} |"
    )

lines += [
    "",
    f"Paired question IDs: {', '.join(ids)}",
    "",
    "Completion tokens use provider-reported totals, including reasoning tokens where reported.",
    "Non-stop finishes indicate possible truncation or other incomplete generations.",
]

report = "\n".join(lines) + "\n"

Path("comparison_output.md").write_text(report, encoding="utf-8")
print(report)
print("Saved: comparison_output.md")
