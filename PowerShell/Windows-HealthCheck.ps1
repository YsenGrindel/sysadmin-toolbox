# Windows HealthCheck - read-only preview; test on a Windows lab machine.
[CmdletBinding()]
param([string]$OutputPath)
$ErrorActionPreference = 'Stop'
try {
  $os = Get-CimInstance Win32_OperatingSystem
  $disks = @(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object {
    [pscustomobject]@{ Drive=$_.DeviceID; SizeGB=[math]::Round($_.Size/1GB,2); FreeGB=[math]::Round($_.FreeSpace/1GB,2) }
  })
  $services = @('EventLog','W32Time','WinDefend') | ForEach-Object {
    $svc=Get-Service -Name $_ -ErrorAction SilentlyContinue
    [pscustomobject]@{Name=$_; Status=if($svc){"$($svc.Status)"}else{'Unavailable'}}
  }
  $bitlocker='Unavailable'
  if(Get-Command Get-BitLockerVolume -ErrorAction SilentlyContinue){
    try {$vol=Get-BitLockerVolume -MountPoint $env:SystemDrive -ErrorAction Stop; $bitlocker="$($vol.VolumeStatus) / $($vol.ProtectionStatus)"}
    catch {$bitlocker='Unable to read'}
  }
  $report=[pscustomobject]@{
    GeneratedAt=(Get-Date).ToString('o'); Computer=$env:COMPUTERNAME
    OS=$os.Caption; Version=$os.Version
    UptimeDays=[math]::Round(((Get-Date)-$os.LastBootUpTime).TotalDays,1)
    AvailableMemoryGB=[math]::Round($os.FreePhysicalMemory/1MB,2)
    Disks=$disks; Services=@($services); BitLocker=$bitlocker
  }
  $report | Format-List
  if($OutputPath){$report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $OutputPath -Encoding UTF8}
} catch { Write-Error $_; exit 1 }
