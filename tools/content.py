"""Editorial source for the site's completed study and project case study."""

STUDY_TITLE = "What fits in GPU memory? A reproducible capacity study"
STUDY_DESC = "A transparent LLM memory-planning study: five model sizes, three weight precisions, seven GPUs, and 105 calculated scenarios. Download the Python, inputs, and CSV."
STUDY_BODY = """
<p class="article-intro">A GPU's hourly price only tells part of the story. First, the model has to fit. This study makes that first calculation explicit, with every input and result available to download.</p>
<div class="study-label"><strong>Calculated capacity study</strong><span>105 scenarios · Python standard library · Published Nov 17, 2026</span></div>
<p>These are memory and rental-cost estimates. They do not measure throughput, latency, model quality, or a successful deployment.</p>

<h2>The question</h2>
<p>How does changing weight precision affect the memory budget and the number of GPUs needed for the same parameter count? I compare 8B, 32B, 70B, 123B, and 405B models at FP16, FP8, and INT4 across the seven GPUs in the <a href="/gpu-guide">GPU guide</a>.</p>

<h2>A small model with visible assumptions</h2>
<p>The starting calculation uses decimal gigabytes:</p>
<pre class="code-block"><code>weights_GB = parameters_in_billions × bytes_per_parameter
planning_memory_GB = weights_GB × 1.20
estimated_hourly_cost = candidate_GPU_count × listed_GPU_hourly_rate</code></pre>
<p>I use 2 bytes per parameter for FP16, 1 for FP8, and 0.5 for INT4. The extra 20% is a planning allowance for runtime memory. It is an assumption, not a calculation of the KV cache. Quantization scales, metadata, mixed-precision layers, activations, and framework allocations can change the real requirement.</p>
<p>Candidate GPU counts round up to powers of two: 1, 2, 4, 8, and so on. This keeps the worksheet consistent with the calculator's candidate configurations. It does not prove that a particular model supports that tensor-parallel degree, or that several GPUs will perform well together.</p>

<h2>One 70B model, three memory budgets</h2>
{{study_chart}}
<p>For the 70B example, the FP16 weight estimate is 140 GB, followed by a 28 GB allowance. Changing the weight format to FP8 halves those two numbers in this model. INT4 halves them again. A smaller weight budget leaves more room, but says nothing about the quality or speed of that quantized model.</p>

<h2>Why capacity changes the hourly comparison</h2>
<p>At FP16, this worksheet budgets 168 GB for the 70B example. Here are three rows from the downloadable results:</p>
{{study_table}}
<p>The H100 candidate rounds from a three-GPU memory minimum to four GPUs under the worksheet's power-of-two rule. A different parallelism strategy could change that choice. The rates are the site's {{price_date}} snapshot; node minimums, availability, networking, and utilization are outside this calculation.</p>

<h2>Reproduce all 105 scenarios</h2>
<p>Download these three small files into one folder. The configuration records the model sizes, bytes per parameter, headroom, GPU capacities, and dated prices. The CSV contains the full scenario matrix.</p>
<div class="download-links">
  <a class="btn solid" href="/downloads/memory-study.py" download>Python script</a>
  <a class="btn" href="/downloads/memory-study-config.json" download>Inputs · JSON</a>
  <a class="btn" href="/downloads/memory-study-results.csv" download>Results · CSV</a>
</div>
<pre class="code-block"><code>python3 memory-study.py --output reproduced.csv
# No packages, API key, or GPU required.</code></pre>
<p>With the supplied inputs, the generated CSV matches the published results. Change the headroom or a rental rate in the JSON and rerun it to explore a different assumption. The <a href="https://github.com/Ankycritica/Datatalkwithankit/blob/main/tools/memory_study.py">source lives in this website's repository</a>.</p>

<h2>What to measure before renting for production</h2>
<p>The next step is a serving experiment with the actual model, quantization implementation, prompt lengths, output lengths, and expected concurrency. Record time to first token, inter-token latency, completed requests, memory use, and any failed requests under that workload.</p>
<p>vLLM's documentation explains how KV-cache pressure can cause preemption and how concurrency and parallelism affect that pressure. That workload-dependent behavior is why this worksheet's flat 20% allowance cannot guarantee a deployment will fit.</p>
<p>Check the capacity in your runtime's units too: this worksheet uses decimal GB, while tools may report binary GiB. Hardware support for a weight format and the availability of appropriate kernels also need verification.</p>
<div class="callout"><p>Use the <a href="/#fit-section">interactive calculator</a> to shortlist configurations. Use measured serving results to choose between them.</p></div>

<h2>Inputs and references</h2>
<ul class="references">
  <li><a href="/gpu-guide">GPU guide</a>: the capacities and dated rental-price snapshot used in the worksheet.</li>
  <li><a href="https://getdeploying.com">getdeploying.com</a>: source of the listed on-demand prices, checked {{price_date}}.</li>
  <li><a href="https://docs.vllm.ai/en/latest/configuration/optimization/">vLLM: Optimization and Tuning</a>: runtime memory, preemption, and parallelism considerations.</li>
</ul>
"""

PIPELINE_TITLE = "From a sourced story to a published video"
PIPELINE_DESC = "A project case study of Ankit Dongare's Python video workflow: source checks, narration, rendering, captions, quality checks, and publishing."
PIPELINE_BODY = """
<p class="article-intro">A video workflow has a lot of repeated work: choosing a story, checking the script, preparing audio, rendering scenes, adding captions, and publishing the result. I built a Python pipeline to connect those steps.</p>
<p class="kicker-line">Project case study · Python, FFmpeg, Whisper, YouTube Data API</p>
<h2>The problem</h2>
<p>Automating one step is easy. Keeping the whole sequence consistent is harder. A correct script can still produce an unreadable caption, a mismatched visual, or a render that should never reach the upload queue.</p>
<h2>The workflow</h2>
<ol class="workflow-list">
  <li><strong>Source and select.</strong><span>Start with a story supported by identifiable sources. Keep the supporting facts with the script.</span></li>
  <li><strong>Write and check.</strong><span>Turn those facts into narration, then check the claims before making media.</span></li>
  <li><strong>Render and caption.</strong><span>Generate narration, build the video with FFmpeg, and align captions with Whisper.</span></li>
  <li><strong>Review and publish.</strong><span>Check the completed output before passing it to the YouTube publishing workflow.</span></li>
</ol>
<h2>Where the engineering matters</h2>
<p>The useful part is the handoff between stages. Keeping source information, scripts, audio, and rendering outputs organized makes a failed step easier to inspect and repeat. Quality checks belong before publishing, where they can stop a problem from becoming a public video.</p>
<p>The system handles repetitive production work. Editorial judgment still matters: a functioning render does not tell you whether the story is interesting, the framing is fair, or the video will earn an audience.</p>
<h2>What this project demonstrates</h2>
<ul>
  <li>Orchestrating several media tools in a repeatable Python workflow.</li>
  <li>Carrying source-backed facts through script and production stages.</li>
  <li>Connecting rendering, captioning, and a publishing API with review points.</li>
</ul>
<p>This case study describes the workflow. The production repository is private, so there is no public source-code download for this project.</p>
<div class="callout"><p>Want to discuss a similar automation workflow? <a href="/#contact">Send me a note</a>.</p></div>
"""
