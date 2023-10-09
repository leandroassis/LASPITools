# Get-Hashes


# Requerimentos:

1. PowerShell com política de execução de script habilitada (i.e Set-ExecutionPolicy=Unrestricted)
3. A pasta que do arquivo Get-Hashes.ps1 deve estar no path.

# Execução

Para executar o CMDLets:

1. Abra o PowerShell
2. Execute o CMDLet `Get-Hashes -DirPath <path-da-pasta> -OutPath <path-do-arquivo-de-hashes>`
3. O arquivo de hashes será gerado no path especificado.
4. O último hash gerado será o hash do arquivo de hashes. Adicione esse hash no relatório.

# Exemplo

```` powershell

 Set-ExecutionPolicy Unrestricted

 PS C:\Users\assis> Get-Hashes.ps1 -DirPath C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master -OutPath C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\Hashes.out
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\.gitignore : F8ABF993511CA9BD1366336D76BFE5D86199B548408E641F8ABA6B19F6537379
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\CLA_4.vhd : 0A184151D0EFF5CF1BF9EAC854537BBEFBCC5A6F5777B3842F418BA54FAE5376
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\gerador_teste_vector.py : 9AAC506FAADCE994728D3D4AD0D59588B354D1E8DB88CE3B81714D7612A73A93
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\Makefile : 365382EB74C2BC4300D324CB6AA1FA91AD24631BE00719F2166AF8E4444E31B6
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\README.md : 01BA4719C80B6FE911B091A7C05124B64EEECE964E09C058EF8F9805DACA546B
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\somador.circ : D21676E54B0ED97C5D040B925B9E5A89C31A40A0A59DF4766FCB4D5AC01EDEC0
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\somador_vetorial.vhd : A324CD592325DEF0B6A0E589ECD99F13E655161A48DA1D8516D8D5CDC8266364
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\STA_teste.vhd : 60BEB5A83C741282E6CFB7E8644E9912CDD6BFBE3CF0A45D0FBE7498CC7684FA
C:\Users\assis\Downloads\AP_AVX-master\AP_AVX-master\teste_vector_somador.txt : 4669AB7FBB8627A1CD8E99C8972FDCFA40C8E587A3287CDC14E3D80F3BD41389
Hash do arquivo de hashes: 749FA2CDA3676AFCB8254B651433BA92029F87167503EC1267D5805A916B73C6

````