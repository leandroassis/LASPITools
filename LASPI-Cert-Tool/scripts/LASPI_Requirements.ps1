$ErrorActionPreference='Stop'

function RII_7(){
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
        [String]$Slot=0,
        [Parameter()]
        [String]$asm_key_type="rsa:1024",
        [Parameter()]
        [String]$sm_key_type="aes:32"
        # todo: um dia fazer asm e sm serem listas e gerar uma chave de cada tipo para TODOS os mecanismos no módulo
    )

    $log_file = ".\Logs\REQUISITO_II_7.log"

    New-Item -Path $log_file -Force > $null

    $key_name = "MCREII.7"
    Add-Content -Path $log_file -Value "====== Requisito MC II.7 ======"

    # loga como usuario e cria uma chave privada, um CSP e uma chave simetrica
    Add-Content -Path $log_file -Value "Gerando chave privada autenticado como user."
    pkcs11-tool.exe --slot-index $Slot --module $Module --login-type 'user' --pin $PIN --keypairgen --key-type $asm_key_type -a "$key_name-assimetrica" | Add-Content -Path $log_file
    Add-Content -Path $log_file -Value "Gerando chave simétrica autenticado como user."
    pkcs11-tool.exe --slot-index $Slot --module $Module --login-type 'user' --pin $PIN --keygen --key-type $sm_key_type -a "$key_name-simetrica" | Add-Content -Path $log_file

    # loga como PUK e tenta listar as chaves
    Add-Content -Path $log_file -Value "Tentando acesso de leitura autenticado com SO."
    pkcs11-tool.exe --slot-index $Slot --module $Module --login-type 'so' --puk $PUK -O | Add-Content -Path $log_file

    # não loga e tenta acessar
    Add-Content -Path $log_file -Value "Tentando acesso de leitura sem realizar autenticação."
    pkcs11-tool.exe --slot-index $Slot --module $Module -O | Add-Content -Path $log_file

    Add-Content -Path $log_file -Value "Requisito MC II.7 finalizado."
    pkcs11-tool.exe --slot-index $Slot --module $Module --pin $PIN --delete-object -a "$key_name-simetrica"
    pkcs11-tool.exe --slot-index $Slot --module $Module --pin $PIN --delete-object -a "$key_name-assimetrica"
}

function RII_8(){
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
        [String]$Slot=0,
        [Parameter()]
        [String]$asm_key_type="rsa:1024"
        # todo: um dia fazer asm e sm serem listas e gerar uma chave de cada tipo para TODOS os mecanismos no módulo
    )

    $log_file = ".\Logs\REQUISITO_II_8.log"

    New-Item -Path $log_file -Force > $null

    $key_name = "MCREII.8"
    Add-Content -Path $log_file -Value "====== Requisito MC II.8 ======"
    # loga como usuario e cria uma chave pública
    Add-Content -Path $log_file -Value "Gerando chave privada autenticado como user."
    pkcs11-tool.exe --slot-index $Slot --module $Module --login-type 'user' --pin $PIN --keypairgen -y pubkey --key-type $asm_key_type -a "$key_name-assimetrica" | Add-Content -Path $log_file

    # loga como PUK e tenta listar as chaves
    Add-Content -Path $log_file -Value "Tentando acesso de leitura autenticado com SO."
    pkcs11-tool.exe --slot-index $Slot --module $Module --login-type 'so' --puk $PUK -O | Add-Content -Path $log_file

    # não loga e tenta acessar
    Add-Content -Path $log_file -Value "Tentando acesso de leitura sem realizar autenticação."
    pkcs11-tool.exe --slot-index $Slot --module $Module -O | Add-Content -Path $log_file

    Add-Content -Path $log_file -Value "Requisito MC II.8 finalizado."
    # loga com um usuario e cria uma chave publica
    # loga como PUK e tenta listar as chaves
    # não loga e tenta acessar
}

function RII_9(){
    # chama o RNG 
}

function RII_11(){
    # lista todos os mecanismos no módulo
}

