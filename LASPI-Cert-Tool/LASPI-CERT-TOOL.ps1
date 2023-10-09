Write-Output "LASPI-CERT-TOOL"
$key = 1
while ($key -eq 1){
    $dll = Read-Host -Prompt 'Insira o nome da dll do modulo criptografico'
    Write-Output "DLL name:'$dll'"
    $var = Read-Host -Prompt 'Prosseguir:[s][n]'
    if ($var -eq 's'){
        $key = 2
    }
}
while ($key -eq 2){
    $pin = Read-Host -Prompt 'Insira o PIN do modulo criptografico'
    Write-Output "PIN:'$pin'"
    $var = Read-Host -Prompt 'Prosseguir:[s][n]'
    if ($var -eq 's'){
        $key = 3
    }
}
while ($key -eq 3){
    $puk = Read-Host -Prompt 'Insira o PUK do modulo criptografico'
    Write-Output "PUK:'$puk'"
    $var = Read-Host -Prompt 'Prosseguir:[s][n]'
    if ($var -eq 's'){
        $key = 4
    }
}
$var = Read-Host -Prompt 'Executar testes de papel de acesso Usuario: [s][n]'
if ($var -eq 's'){
    #gerar chave assimetrica
    pkcs11-tool.exe --module $dll --login --pin $pin --keypairgen --key-type rsa:1024 -a rsaUser
    #listar objetos
    pkcs11-tool.exe --module $dll --login --pin $pin -O
    #exportar chave publica
    pkcs11-tool.exe --module $dll --login --pin $pin -r --type pubkey -a rsaUser -o rsaUser.der
    #deletar chave publica
    pkcs11-tool.exe --module $dll --login --pin $pin --delete-object --type pubkey -a rsaUser
    #listar objetos
    pkcs11-tool.exe --module $dll --login --pin $pin -O
    #importar chave publica
    pkcs11-tool.exe --module $dll --pin $pin -w rsaUser.der -y pubkey -a rsaUser
    #listar objetos
    pkcs11-tool.exe --module $dll --login --pin $pin -O
    #deletando objetos
    pkcs11-tool.exe --module $dll --login --pin $pin --delete-object --type pubkey -a rsaUser
    pkcs11-tool.exe --module $dll --login --pin $pin --delete-object --type privkey -a rsaUser
    #listar objetos
    pkcs11-tool.exe --module $dll --login --pin $pin -O
}

$var = Read-Host -Prompt 'Executar testes de papel de acesso Oficial de seguranca: [s][n]'
if ($var -eq 's'){
    #gerar chave assimetrica de usuario para testes
    pkcs11-tool.exe --module $dll --login --pin $pin --keypairgen --key-type rsa:1024 -a rsaSO
    #tentando gerar chave assimetrica de oficial de seguranca para testes
    pkcs11-tool.exe --module $dll --login --pin $pin --keypairgen --key-type rsa:1024 -a rsaSO  
    #listar objetos
    pkcs11-tool.exe --module $dll --login --pin $pin -O
    #exportar chave publica
    pkcs11-tool.exe --module $dll --login --puk $puk -r --type pubkey -a rsaUser -o rsaSO.der
    #deletar chave publica
    pkcs11-tool.exe --module $dll --login --puk $puk --delete-object --type pubkey -a rsaSo
    #listar objetos
    pkcs11-tool.exe --module $dll --login --puk $puk -O
    #importar chave publica
    pkcs11-tool.exe --module $dll --puk $puk -w rsaSO.der -y pubkey -a rsaSO
    #listar objetos
    pkcs11-tool.exe --module $dll --login --puk $puk -O
    #deletando objetos
    pkcs11-tool.exe --module $dll --login --puk $puk --delete-object --type pubkey -a rsaSO
    pkcs11-tool.exe --module $dll --login --puk $puk --delete-object --type privkey -a rsaSO
    #listar objetos
    pkcs11-tool.exe --module $dll --login --puk $puk -O
}


$var = Read-Host -Prompt 'Executar testes de papel de acesso Nao Autenticado: [s][n]'
if ($var -eq 's'){
    #gerar chave assimetrica de nao autenticado para testes
    pkcs11-tool.exe --module $dll --login --pin $pin --keypairgen --key-type rsa:1024 -a rsaNA
    #listar objetos
    pkcs11-tool.exe --module $dll -O
    #tentando criar chave sem autenticacao
    pkcs11-tool.exe --module $dll  --keypairgen --key-type rsa:1024 -a rsaNA2
    #exportar chave publica
    pkcs11-tool.exe --module $dll -r --type pubkey -a rsaNA -o rsaNA.der
    #deletar chave publica
    pkcs11-tool.exe --module $dll --delete-object --type pubkey -a rsaNA
    #listar objetos
    pkcs11-tool.exe --module $dll -O
    #importar chave publica
    pkcs11-tool.exe --module $dll -w rsaNA.der -y pubkey -a rsaNA
    #listar objetos
    pkcs11-tool.exe --module $dll  -O
    #deletando objetos
    pkcs11-tool.exe --module $dll --delete-object --type pubkey -a rsaNA
    pkcs11-tool.exe --module $dll --delete-object --type privkey -a rsaNA
    #listar objetos
    pkcs11-tool.exe --module $dll  -O
}