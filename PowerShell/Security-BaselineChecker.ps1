# Read-only indicative checks; this is not a security audit.
[CmdletBinding()]
param()
$checks = @()
if(Get-Command Get-NetFirewallProfile -ErrorAction SilentlyContinue){
  try {$checks += Get-NetFirewallProfile | Select-Object Name,Enabled}
  catch {Write-Warning "Firewall status unavailable"}
}
if(Get-Command Get-MpComputerStatus -ErrorAction SilentlyContinue){
  try {$checks += Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled}
  catch {Write-Warning "Defender status unavailable"}
}
if(Get-Command Get-BitLockerVolume -ErrorAction SilentlyContinue){
  try {$checks += Get-BitLockerVolume -MountPoint $env:SystemDrive | Select-Object MountPoint,VolumeStatus,ProtectionStatus}
  catch {Write-Warning "BitLocker status unavailable"}
}
try {$checks += Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name EnableLUA -ErrorAction Stop | Select-Object EnableLUA}
catch {Write-Warning "UAC status unavailable"}
$checks | Format-List
Write-Host 'Indicative only / Contrôles indicatifs uniquement.'
