#!/usr/bin/env pwsh

Start-Process -FilePath "python" -ArgumentList "demo_modality_plot.py" -NoNewWindow -Wait
# Write-Host "Press any key to exit..."
# Read-Host