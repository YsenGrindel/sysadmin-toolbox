<#
.SYNOPSIS
  Diagnostic indicatif Windows avec verdicts lisibles (lecture seule).
.DESCRIPTION
  Vérifie la mémoire disponible, l'espace disque, quelques services et BitLocker.
  N'affirme pas que le système est entièrement sain ou sécurisé.
.EXAMPLE
  .\Windows-HealthCheck.ps1
.EXAMPLE
  .\Windows-HealthCheck.ps1 -Language en -OutputPath .\health.json
.NOTES
  PowerShell 5.1+ sur Windows. Validation manuelle en laboratoire nécessaire.
#>
[CmdletBinding()]
param(
    [ValidateSet('fr', 'en')][string]$Language = 'fr',
    [string]$OutputPath,
    [switch]$Pause
)

$ErrorActionPreference = 'Stop'
$script:Checks = New-Object 'System.Collections.Generic.List[object]'
$translations = @{
    fr = @{
        Title = 'WINDOWS HEALTHCHECK - bilan indicatif'
        OK = 'OK'; WARN = 'ATTENTION'; FAIL = 'PROBLEME'
        UNKNOWN = 'NON EVALUE'; INFO = 'INFO'
        Summary = 'BILAN'; Disclaimer = 'Un resultat OK ne constitue pas un audit complet de sante ou de securite.'
        Clean = 'Aucune anomalie detectee parmi les controles evaluables.'
        Attention = 'Des controles demandent une verification.'
        Host = 'Poste'; OS = 'Systeme'; Uptime = 'Demarrage'
        Memory = 'Memoire disponible'; Disk = 'Disque'
        EventLog = 'Journal des evenements'; W32Time = 'Service de temps Windows'
        Defender = 'Service Microsoft Defender'; BitLocker = 'Protection BitLocker'
        NoData = 'Impossible de lire cette information'
        NotAvailable = 'Commande indisponible'; ThirdParty = 'Peut etre normal avec un antivirus tiers'
        Policy = 'Peut dependre de la politique de chiffrement'
        NoDisk = 'Aucun disque local detecte'
        Saved = 'Rapport JSON enregistre'
    }
    en = @{
        Title = 'WINDOWS HEALTHCHECK - indicative status'
        OK = 'OK'; WARN = 'WARNING'; FAIL = 'PROBLEM'
        UNKNOWN = 'NOT CHECKED'; INFO = 'INFO'
        Summary = 'SUMMARY'; Disclaimer = 'An OK result is not a complete health or security audit.'
        Clean = 'No anomalies detected among the evaluated checks.'
        Attention = 'Some checks need attention.'
        Host = 'Computer'; OS = 'Operating system'; Uptime = 'Last startup'
        Memory = 'Available memory'; Disk = 'Disk'
        EventLog = 'Windows Event Log'; W32Time = 'Windows Time service'
        Defender = 'Microsoft Defender service'; BitLocker = 'BitLocker protection'
        NoData = 'Unable to read this information'
        NotAvailable = 'Command unavailable'; ThirdParty = 'May be normal with third-party antivirus'
        Policy = 'May depend on the encryption policy'
        NoDisk = 'No local fixed disks detected'
        Saved = 'JSON report saved'
    }
}
$T = $translations[$Language]

function Add-Check {
    param([string]$Name, [ValidateSet('OK','WARN','FAIL','UNKNOWN','INFO')][string]$Status, [string]$Details)
    $script:Checks.Add([pscustomobject]@{ Name=$Name; Status=$Status; Details=$Details })
}

Write-Host ""
Write-Host "=== $($T.Title) ===" -ForegroundColor Cyan
try {
    $os = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
    Write-Host "$($T.Host): $env:COMPUTERNAME | $($T.OS): $($os.Caption)" 
    Write-Host "$($T.Uptime): $($os.LastBootUpTime)"
} catch {
    Add-Check -Name $T.OS -Status UNKNOWN -Details $T.NoData
    $os = $null
}

if ($null -ne $os -and $os.TotalVisibleMemorySize -gt 0) {
    $freePct = [math]::Round(100 * $os.FreePhysicalMemory / $os.TotalVisibleMemorySize, 1)
    $freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    $status = if ($freePct -lt 5) { 'FAIL' } elseif ($freePct -lt 15) { 'WARN' } else { 'OK' }
        $memoryDetails = if ($Language -eq "fr") { "{0} Go libres ({1} %)" -f $freeGB, $freePct } else { "{0} GB free ({1}%)" -f $freeGB, $freePct }
    Add-Check -Name $T.Memory -Status $status -Details $memoryDetails
} else {
    Add-Check -Name $T.Memory -Status UNKNOWN -Details $T.NoData
}

try {
    $disks = @(Get-CimInstance -ClassName Win32_LogicalDisk -Filter 'DriveType=3' -ErrorAction Stop)
    if ($disks.Count -eq 0) { Add-Check -Name $T.Disk -Status UNKNOWN -Details $T.NoDisk }
    foreach ($disk in $disks) {
        if ($disk.Size -le 0) {
            Add-Check -Name "$($T.Disk) $($disk.DeviceID)" -Status UNKNOWN -Details $T.NoData
            continue
        }
        $freePct = [math]::Round(100 * $disk.FreeSpace / $disk.Size, 1)
        $freeGB = [math]::Round($disk.FreeSpace / 1GB, 2)
        $status = if ($freePct -lt 5) { 'FAIL' } elseif ($freePct -lt 15) { 'WARN' } else { 'OK' }
                $diskDetails = if ($Language -eq "fr") { "{0} Go libres ({1} %)" -f $freeGB, $freePct } else { "{0} GB free ({1}%)" -f $freeGB, $freePct }
        Add-Check -Name "$($T.Disk) $($disk.DeviceID)" -Status $status -Details $diskDetails
    }
} catch {
    Add-Check -Name $T.Disk -Status UNKNOWN -Details $T.NoData
}

foreach ($item in @(
    @{ Code='EventLog'; Label=$T.EventLog; Critical=$true },
    @{ Code='W32Time'; Label=$T.W32Time; Critical=$false },
    @{ Code='WinDefend'; Label=$T.Defender; Critical=$false }
)) {
    try {
        $svc = Get-Service -Name $item.Code -ErrorAction Stop
        if ($svc.Status -eq 'Running') {
            Add-Check -Name $item.Label -Status OK -Details 'Running'
        } elseif ($item.Critical) {
            Add-Check -Name $item.Label -Status FAIL -Details "$($svc.Status)"
        } else {
            $detail = if ($item.Code -eq 'WinDefend') { $T.ThirdParty } else { "$($svc.Status)" }
            Add-Check -Name $item.Label -Status INFO -Details $detail
        }
    } catch {
        Add-Check -Name $item.Label -Status UNKNOWN -Details $T.NotAvailable
    }
}

if (Get-Command Get-BitLockerVolume -ErrorAction SilentlyContinue) {
    try {
        $vol = Get-BitLockerVolume -MountPoint $env:SystemDrive -ErrorAction Stop
        $state = "$($vol.ProtectionStatus)"
        $status = if ($state -eq 'On') { 'OK' } elseif ($state -eq 'Off') { 'WARN' } else { 'UNKNOWN' }
        $details = "$($vol.VolumeStatus) / $state"
        if ($status -eq 'WARN') { $details += " ($($T.Policy))" }
        Add-Check -Name $T.BitLocker -Status $status -Details $details
    } catch {
        Add-Check -Name $T.BitLocker -Status UNKNOWN -Details $T.NoData
    }
} else {
    Add-Check -Name $T.BitLocker -Status UNKNOWN -Details $T.NotAvailable
}

$colors = @{ OK='Green'; WARN='Yellow'; FAIL='Red'; UNKNOWN='DarkGray'; INFO='Cyan' }
Write-Host ""
foreach ($check in $script:Checks) {
    $label = $T[$check.Status]
    Write-Host ("[{0}] {1}: {2}" -f $label, $check.Name, $check.Details) -ForegroundColor $colors[$check.Status]
}

$counts = [ordered]@{}
foreach ($status in @('OK','WARN','FAIL','UNKNOWN','INFO')) {
    $counts[$status] = @($script:Checks | Where-Object { $_.Status -eq $status }).Count
}
Write-Host ""
Write-Host ("=== {0}: OK={1} | {2}={3} | {4}={5} | {6}={7} | INFO={8} ===" -f $T.Summary, $counts.OK, $T.WARN, $counts.WARN, $T.FAIL, $counts.FAIL, $T.UNKNOWN, $counts.UNKNOWN, $counts.INFO) -ForegroundColor Cyan
if ($counts.WARN -eq 0 -and $counts.FAIL -eq 0) {
    Write-Host $T.Clean -ForegroundColor Green
} else {
    Write-Host $T.Attention -ForegroundColor Yellow
}
Write-Host $T.Disclaimer -ForegroundColor DarkGray

if ($OutputPath) {
    $report = [pscustomobject]@{
        GeneratedAt = (Get-Date).ToString('o')
        Computer = $env:COMPUTERNAME
        Language = $Language
        Checks = @($script:Checks)
        Summary = [pscustomobject]$counts
    }
    try {
        $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding UTF8 -ErrorAction Stop
        Write-Host "$($T.Saved): $OutputPath"
    } catch {
        Write-Error "Impossible d'enregistrer le rapport : $($_.Exception.Message)"
    }
}

# Optional interactive hold for "Run with PowerShell" / mode interactif.
# A dedicated .cmd launcher also pauses after PowerShell exits, including on error.
if ($Pause) {
    Write-Host ""
    $prompt = if ($Language -eq 'en') { 'Press Enter to close this window' } else { 'Appuyez sur Entree pour fermer cette fenetre' }
    Read-Host $prompt | Out-Null
}
