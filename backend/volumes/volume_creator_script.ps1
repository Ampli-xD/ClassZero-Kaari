param(
    [string]$BackupPath = "."
)
$ContainersVolumes = @{
    "n8n" = @("n8n_data") 
    "postgresql" = @("pgdata_vector")
    "minio" = @("minio-data")
}


$backupDir = $BackupPath

try {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    Write-Host "Starting backup to $backupDir..." -ForegroundColor Green
    
    foreach ($container in $ContainersVolumes.Keys) {        
        $volumes = $ContainersVolumes[$container]
        foreach ($volume in $volumes) {
            Write-Host "    Processing volume: $volume"
            
            # Check if volume exists
            $volumeExists = docker volume ls --format "{{.Name}}" | Where-Object { $_ -eq $volume }
            if (-not $volumeExists) {
                Write-Host "      Warning: Volume '$volume' does not exist - skipping" -ForegroundColor Yellow
                continue
            }
            
            Write-Host "      creating volume: $volume"
            
            # Create volume 
            $volumeFile = "$volume.tar.gz"
            docker run --rm -v "${volume}:/data:ro" -v "${backupDir}:/backup" ubuntu:latest tar czf "/backup/$volumeFile" -C /data .
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "      Volume backup completed: $volumeFile" -ForegroundColor Green
            } else {
                Write-Host "      Error: Failed to backup volume $volume" -ForegroundColor Red
            }
        }
        
        Write-Host "  Completed processing volume for : $container" -ForegroundColor Green
    }
    
    Write-Host "`n=== VOLUMES PROCESS COMPLETED ===" -ForegroundColor Green
    Write-Host "volumes directory: $backupDir"
    Write-Host "`nFiles created:"
    
    if (Test-Path $backupDir) {
        $files = Get-ChildItem $backupDir
        $files | Format-Table Name, Length, LastWriteTime -AutoSize
        
        $totalSize = ($files | Measure-Object Length -Sum).Sum
        $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
        
        Write-Host "`nSummary:" -ForegroundColor Cyan
        Write-Host "  Total files: $($files.Count)"
        Write-Host "  Total size: $totalSizeMB MB"
        Write-Host "  Location: $backupDir"
    } else {
        Write-Host "No backup directory created - check for errors above" -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error during backup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}


