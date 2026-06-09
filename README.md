# Local Hermes with Gemma-4 Build

This repository configures the optimal, unbottlenecked local environment for pairing the **Hermes AI Agent** with the **Gemma-4-12B Uncensored** model via Ollama. 

## The Problem
By default, Hermes connects to Ollama via the OpenAI-compatible `/v1/chat/completions` endpoint. Because of how Ollama handles this endpoint, it strips out context window overrides (`num_ctx`), artificially bottlenecking the context window to 4096 tokens, causing unexpected generation truncations on long tasks.

## The Solution
We circumvent this by compiling a custom Ollama Modelfile alias that forces the context length and removes all resource bottlenecks at the model layer natively, bypassing the API's limitations.

This Modelfile:
- Increases context window strictly to `65536`
- Sets `num_predict` to `-1` (unlimited generation)
- Forces maximum layers to VRAM (`num_gpu 999`)

## Installation

Run the included PowerShell setup script to automatically compile the alias model and configure Hermes to use it.

```powershell
.\setup.ps1
```

Once installed, Hermes (both the CLI and the Windows Desktop App) will natively use `hermes-gemma-4-12b` without any truncation limits.
