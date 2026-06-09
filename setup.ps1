Write-Host "Building unbottlenecked Hermes Gemma 4 model alias..." -ForegroundColor Cyan

ollama create hermes-gemma-4-12b -f .\Modelfile

$ConfigPath = "$env:LOCALAPPDATA\hermes\config.yaml"
if (Test-Path $ConfigPath) {
    Write-Host "Updating Hermes configuration to use the new model..." -ForegroundColor Cyan
    (Get-Content $ConfigPath) -replace 'default: igorls/gemma-4-12B-it-heretic-GGUF:latest', 'default: hermes-gemma-4-12b' -replace 'model: qwen3:14b', 'model: hermes-gemma-4-12b' | Set-Content $ConfigPath
    Write-Host "Configuration successfully updated!" -ForegroundColor Green
} else {
    Write-Host "Hermes config.yaml not found at $ConfigPath. Please configure the default and delegation models manually." -ForegroundColor Yellow
}

Write-Host "Setup complete!" -ForegroundColor Green
