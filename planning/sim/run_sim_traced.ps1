# -----------------------------------------------------------------------------
# run_sim_traced.ps1 — run the 5FR oil-burn simulation and stream traces to Jaeger
# -----------------------------------------------------------------------------
# Prereq: Jaeger v2 running (UI http://localhost:16686, OTLP gRPC on 4317).
# Usage:  .\planning\sim\run_sim_traced.ps1
# -----------------------------------------------------------------------------

$py  = "C:\Workspace\.venv-wired\Scripts\python.exe"
$sim = "C:\Workspace\planning\sim\oil_burn_5fr_sim.py"

# 1. OpenTelemetry export profile (matches setup_env_wired.ps1)
$env:OTEL_SERVICE_NAME           = "wiredv2-oil-case"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "grpc"
$env:OTEL_TRACES_EXPORTER        = "otlp"

# 2. Ensure the OTel SDK + gRPC exporter are present in the venv
& $py -c "import opentelemetry.exporter.otlp.proto.grpc.trace_exporter" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing OpenTelemetry SDK + OTLP gRPC exporter into .venv-wired ..." -ForegroundColor Yellow
    & $py -m pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
}

# 3. Quick Jaeger health check
try {
    $r = Invoke-WebRequest -Uri "http://localhost:16686/" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    if ($r.StatusCode -eq 200) { Write-Host "Jaeger: ONLINE" -ForegroundColor Green }
} catch {
    Write-Host "Jaeger: OFFLINE — start jaeger.exe first (spans will be dropped)." -ForegroundColor Red
}

# 4. Run the simulation (emits one trace per case + writes JSON)
& $py $sim --json

# 5. Open the UI
Write-Host "`nOpen Jaeger -> service 'wiredv2-oil-case' -> Find Traces. 5 traces (oil_case_*)." -ForegroundColor Cyan
Start-Process "http://localhost:16686/"
