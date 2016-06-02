Add-Type -AssemblyName System.IO.Compression.FileSystem
function Unzip
{
    param([string]$zipfile, [string]$outpath)

    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipfile, $outpath)
}
$curLocation = Get-Location

# downloading lexos
Write-Host ' '
Write-Host 'downloading lexos' -ForegroundColor Green
$lexosUrl = 'https://github.com/WheatonCS/Lexos/archive/master.zip'
Invoke-WebRequest $lexosUrl -OutFile 'master.zip'


# installing lexos
Write-Host ' '
Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
if(Test-Path 'C:\Lexos-master'){
    Write-Host 'you already have lexos installed'
    Remove-Item C:\Lexos-master -Recurse -Force -Confirm:$false
    Unzip "$curLocation\master.zip" "C:\"
    Write-Host 'your lexos is updated'
}
else {
    Write-Host "you don't seems to have lexos installed"
    Unzip "$curLocation\master.zip" "C:\"
    Write-Host "we have successfully installed lexos for you."
}

# clean up
Remove-Item -Force -Confirm:$false 'master.zip'

Write-Host 'we have cleaned up' -ForegroundColor Green
Read-Host 'you can press enter to close this windows now'