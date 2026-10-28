# AD bulk user creation: dry run by default; -Apply requires PowerShell confirmation.
# LAB ONLY / LABORATOIRE UNIQUEMENT
[CmdletBinding(SupportsShouldProcess=$true,ConfirmImpact='High')]
param([Parameter(Mandatory=$true)][string]$CsvPath,[switch]$Apply)
$ErrorActionPreference='Stop'
$users=@(Import-Csv -LiteralPath $CsvPath)
if($users.Count -eq 0){throw 'Empty CSV'}
foreach($column in @('SamAccountName','GivenName','Surname','OU','Groups')){
  if($column -notin $users[0].PSObject.Properties.Name){throw "Missing column: $column"}
}
$seen=@{}
foreach($user in $users){
  $sam=$user.SamAccountName
  if($sam -notmatch '^[A-Za-z0-9._-]{1,20}$' -or [string]::IsNullOrWhiteSpace($user.GivenName) -or [string]::IsNullOrWhiteSpace($user.Surname) -or [string]::IsNullOrWhiteSpace($user.OU)){throw "Invalid entry: $sam"}
  if($seen.ContainsKey($sam.ToLowerInvariant())){throw "Duplicate user: $sam"}
  $seen[$sam.ToLowerInvariant()]=$true
}
if(-not $Apply){
  foreach($user in $users){Write-Host "[DRY RUN] $($user.SamAccountName) -> $($user.OU)"}
  return
}
Import-Module ActiveDirectory -ErrorAction Stop
$password=Read-Host 'Initial password' -AsSecureString
foreach($user in $users){
  $sam=$user.SamAccountName
  if(Get-ADUser -Identity $sam -ErrorAction SilentlyContinue){Write-Warning "Existing account: $sam";continue}
  if($PSCmdlet.ShouldProcess($sam,'Create AD user')){
    New-ADUser -Name "$($user.GivenName) $($user.Surname)" -SamAccountName $sam -GivenName $user.GivenName -Surname $user.Surname -Path $user.OU -AccountPassword $password -Enabled $true -ChangePasswordAtLogon $true -ErrorAction Stop
    foreach($group in ($user.Groups -split '\|' | Where-Object {$_.Trim()})){
      if($PSCmdlet.ShouldProcess($sam,"Add to $group")){Add-ADGroupMember -Identity $group.Trim() -Members $sam -ErrorAction Stop}
    }
  }
}
