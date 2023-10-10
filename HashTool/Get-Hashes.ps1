param(
    [Parameter(Mandatory=$true)]
    [String]$DirPath,
    [Parameter(Mandatory=$true)]
    [String]$OutPath
)

$ErrorActionPreference = "Stop"

$check_file_exists = Test-Path $OutPath
if($check_file_exists -eq $true){
    Remove-Item $OutPath
}

$arquivos = Get-ChildItem $DirPath -File -Recurse

New-Item -Path $OutPath -Force > $null

foreach ($item in $arquivos.FullName ) {
    $hashItem = [string] (Get-FileHash -Algorithm SHA256 $item).Hash
    $hashItem = $hashItem.ToLower()
    $item = $item.Split("\")[-1]
    Add-Content -Path $OutPath -Value "$item    $hashItem"
    Write-Host "$item : $hashItem"
}

$hash_hashes_file = ([string] (Get-FileHash $OutPath).Hash).ToLower()

Write-Host "Hash do arquivo de hashes: $hash_hashes_file"

