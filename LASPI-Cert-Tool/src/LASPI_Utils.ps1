function Get-RNGSamples(){
    param(
        [Parameter()]
        [int]$Bytes=25MB,
        [Parameter()]
        [int]$BatchSize=32,
        [Parameter()]
        [int]$Files=10,
        [Parameter(Mandatory=$true)]
        [String]$Module,
        [Parameter(Mandatory=$true)]
        [String]$Path,
        [Parameter()]
        [String]$Slot=0
    )

    $sample_sz = $Bytes
    $batch_sz = $BatchSize
    $total_files = $Files
    $module_dll = $Module
    $output_path = $Path

    if(($total_files -le 0)){
        throw "A opcao Files DEVE ser maior que zero."
    }
    elseif ($batch_sz -le 0) {
        throw "BatchSize DEVE ser maior que zero."
    }
    elseif ($sample_sz -le 0){
        throw "Bytes DEVE ser maior que zero."
    }

    $iterations = $sample_sz/($total_files*$batch_sz)
    $total_batches = $iterations*$total_files

    for($file = 0; $file -lt $total_files; $file++) {
        # creates the output file by merging $output_path and the sequential file's number
        New-Item -Path "$output_path$file" -Force > $null
        
        # for each iteration generates $batch_sz random numbers
        for($idx=0; $idx -lt $iterations; $idx++){
            $random_bytes = pkcs11-tool.exe --generate-random $batch_sz --slot-index $Slot --module $module_dll

            if(($random_bytes.Length -gt $batch_sz) -or ($random_bytes.Length -eq 0)){
                throw "Ocorreu um erro durante a extracao da samples. Verifique se o equipamento ensaiado esta conectado e disponivel. Verifique se a DLL foi passada corretamente e esta no PATH."
            }

            Add-Content -Path "$output_path$file" -Value $random_bytes -NoNewline

            $current_batch = ($file+1)*($idx+1)

            # to do: fixar batch size e deixar usuário escolher bytes totais e num arquivos
            $percentage = ($current_batch*100/$total_batches)
            if($percentage -gt 100){
                $percentage = 100
            }
            Write-Progress -Activity "Extraindo $sample_sz numeros aleatorios" -Status "Progresso" -CurrentOperation "Extraindo batch $current_batch de $total_batches." `
            -PercentComplete $percentage
        }

        Write-Host "Arquivo $output_path$file terminado."
    }

    Write-Host "A extracao de samples do RNG terminou."
}

function Merge-RNGSamples(){
    param(
        [Parameter(Mandatory=$true)]
        [String]$LikeName,
        [Parameter(Mandatory=$true)]
        [String]$Path,
        [Parameter()]
        [bool]$Remove=$false
    )

    $path = $Path
    $common_name = $LikeName
    $remove = $Remove

    $outpath = "$path\output_merged"
    $sample_files = Get-ChildItem $path -Recurse | Where-Object -Property Name -Like "$common_name*"

    New-Item -Path $outpath -Force > $null

    foreach($file in $sample_files){
        $sample = Get-Content $file
        Add-Content -Path $outpath -Value $sample -NoNewline
    }

    Write-Host "Arquivo concatenado gerado."

    if($remove -eq $true){
        Remove-Item $sample_files
        Write-Host "Arquivos intermediários removidos"
    }
}

function Initialize-Module(){
    param(
        [Parameter()]
        [String]$PIN="1234",
        [Parameter()]
        [String]$PUK="12345678",
        [Parameter()]
        [String]$Name="ensaios",
        [Parameter(Mandatory=$true)]
        [String]$Module,
        [Parameter()]
        [array]$Slots=@(0)
    )

    $log_file = ".\Logs\Initialize-Module.log"

    New-Item -Path $log_file -Force > $null
    
    foreach ($slot in $Slots) {
        Add-Content -Path $log_file -Value "Inicializando módulo no $slot com nome $Name$slot; pin $PIN; e puk $PUK."
        pkcs11-tool.exe --module $Module --slot-index $slot --init-token  --init-pin --login --pin $PIN --so-pin $PUK --label "$Name$slot" | Add-Content -Path $log_file 
        pkcs11-tool.exe --module $Module --slot-index $slot -I | Add-Content -Path $log_file
    }

    Add-Content -Path $log_file -Value "Fim da função de inicialização"
}