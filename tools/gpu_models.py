"""Publisher-sourced examples for the inference model explorer.

Parameter counts are approximate, including embeddings. DeepSeek's repository
lists roughly 685B stored parameters, rather than
using its much smaller active-parameter count as a memory estimate.
"""
from decimal import Decimal, ROUND_CEILING
from html import escape

MODELS_REVIEWED_ISO = "2026-11-20"
MODELS_REVIEWED_LABEL = "Nov 20, 2026"
MODELS = [
    {"name": "Qwen3-8B", "parameters": 8.2, "kind": "Dense", "use": "Chat & reasoning",
     "url": "https://huggingface.co/Qwen/Qwen3-8B"},
    {"name": "Qwen2.5-Coder-32B-Instruct", "parameters": 32.5, "kind": "Dense", "use": "Coding assistants",
     "url": "https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct"},
    {"name": "Qwen3-32B", "parameters": 32.8, "kind": "Dense", "use": "Chat & reasoning",
     "url": "https://huggingface.co/Qwen/Qwen3-32B"},
    {"name": "Llama-3.3-70B-Instruct", "parameters": 70, "kind": "Dense", "use": "Multilingual chat",
     "url": "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct"},
    {"name": "Qwen3-235B-A22B", "parameters": 235, "kind": "MoE · total parameters", "use": "Chat & reasoning",
     "url": "https://huggingface.co/Qwen/Qwen3-235B-A22B"},
    {"name": "Llama-3.1-405B-Instruct", "parameters": 405, "kind": "Dense", "use": "Large chat model",
     "url": "https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct"},
    {"name": "DeepSeek-R1-0528", "parameters": 685, "kind": "MoE · stored parameters", "use": "Advanced reasoning",
     "url": "https://huggingface.co/deepseek-ai/DeepSeek-R1-0528",
     "note": "Publisher checkpoint mixes FP8 and higher-precision tensors; format choices below are memory comparisons."},
]


def capacity(parameters, bytes_per_parameter, gpu_memory):
    need = Decimal(str(parameters)) * Decimal(str(bytes_per_parameter)) * Decimal("1.2")
    minimum = int((need / Decimal(str(gpu_memory))).to_integral_value(rounding=ROUND_CEILING))
    count = 1
    while count < minimum:
        count *= 2
    return need, count


def model_explorer(gpus, guide=False):
    """Render a working H100/16-bit fallback; site.js enables the controls."""
    gpu_options = "".join(
        f'<option value="{key}" data-memory="{memory}" data-vendor="{vendor}">'
        f'{name} · {memory} GB</option>'
        for key, vendor, name, memory, *_ in gpus
    )
    rows = []
    for model in MODELS:
        need, count = capacity(model["parameters"], 2, gpus[0][3])
        tight = count == 1 and need / Decimal(str(gpus[0][3])) > Decimal("0.9")
        status = "Tight budget" if tight else "Memory candidate" if count == 1 else "Multiple GPUs"
        style = "tight" if tight else "single" if count == 1 else "multi"
        note = f'<small class="model-checkpoint">{escape(model["note"])}</small>' if model.get("note") else ""
        rows.append(f"""
          <tr data-parameters="{model['parameters']}">
            <th scope="row"><a href="{escape(model['url'], quote=True)}">{escape(model['name'])}</a>
              <small>≈{model['parameters']:g}B parameters · {escape(model['kind'])}</small>{note}</th>
            <td data-label="Typical use">{escape(model['use'])}</td>
            <td data-label="Est. memory" class="model-memory">{float(need):,.1f} GB</td>
            <td data-label="GPU count"><span class="model-count {style}">{count} {'GPU' if count == 1 else 'GPUs'}</span>
              <small class="model-fit-label">{status}</small></td>
          </tr>""")
    end_link = (
        '<a class="link" href="/#fit-section">Try the size calculator</a>'
        if guide else '<a class="link" href="/gpu-guide#ai-models">Full GPU &amp; model guide</a>'
    )
    return f"""
<section class="section model-section" id="ai-models" aria-labelledby="models-title">
  <div class="{'model-guide-inner' if guide else 'wrap'}">
    <div class="sec-head">
      <h2 id="models-title">AI models by GPU</h2>
      <p>Choose a GPU to shortlist open-weight text models for chat, coding, and reasoning.</p>
    </div>
    <div class="model-explorer" id="model-explorer" data-default-expanded="{'true' if guide else 'false'}">
      <div class="model-controls">
        <label for="model-gpu">Your GPU<select id="model-gpu" disabled>{gpu_options}</select></label>
        <label for="model-precision">Weight precision<select id="model-precision" disabled>
          <option value="2">16-bit · BF16 / FP16</option>
          <option value="1">FP8 · memory estimate</option>
          <option value="0.5">INT4 · memory estimate</option>
        </select></label>
      </div>
      <p class="model-summary" id="model-summary" role="status" aria-live="polite">
        All {len(MODELS)} examples · NVIDIA H100 · 16-bit estimates</p>
      <p class="model-runtime" id="model-runtime">NVIDIA: use a CUDA-compatible serving build and check support for this GPU and checkpoint.</p>
      <noscript><p class="note">Enable JavaScript to change the GPU and precision. This table shows NVIDIA H100 with 16-bit estimates.</p></noscript>
      <table class="model-table">
        <caption class="sr-only">Example language models, estimated memory budget, and candidate GPU counts</caption>
        <thead><tr><th scope="col">Model · publisher card</th><th scope="col">Typical use</th><th scope="col">Est. memory</th><th scope="col">GPU count</th></tr></thead>
        <tbody id="model-results">{''.join(rows)}
        </tbody>
      </table>
      <p class="note" id="model-empty" hidden>No single-GPU candidates in this selection. Expand the list to see multi-GPU estimates.</p>
      <button class="btn model-toggle" id="model-toggle" type="button" aria-expanded="false" aria-controls="model-results" hidden>Show all {len(MODELS)} models</button>
      <div class="model-notes">
        <p>Memory estimates = approximate total parameters × bytes per weight × 1.2, in decimal GB.
        The 20% allowance is a starting point; context length, KV cache, batching, and runtime allocations change actual fit.
        Counts round up to power-of-two candidates. Multi-GPU configurations also need supported parallelism and interconnects.</p>
        <details class="model-method">
          <summary>Precision, checkpoints, and sources</summary>
          <p>FP8 and INT4 compare memory footprints; they require an appropriate quantized checkpoint and kernels for your hardware.
          CUDA quantization implementations do not automatically work on AMD. Check the
          <a class="link" href="https://docs.vllm.ai/en/stable/features/quantization/">vLLM hardware compatibility table</a>
          for the exact format and backend.</p>
          <p>MoE memory uses all stored parameters, including inactive experts. Model names link to publisher cards with architecture,
          download access, and license details. DeepSeek's mixed-precision checkpoint can differ from these simplified format estimates.
          These are inference planning examples; they have not been benchmarked on every GPU.</p>
          <p>Catalog reviewed {MODELS_REVIEWED_LABEL}. <a class="link" href="/posts/llm-memory-capacity">How the memory estimates work</a>.</p>
        </details>
        <p class="model-end-link">{end_link}</p>
      </div>
    </div>
  </div>
</section>
"""
