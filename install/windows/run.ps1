if(-Not (Test-Path "$HOME/Anaconda2/python.exe")){
    Write-Host "we cannot found anaconda2" -ForegroundColor Red
    Write-Host "please run the install.exe again" -ForegroundColor Red
    Write-Host "make sure you follow the instruction that pops up when you beginning to install anaconda"
}
if(-Not (Test-Path "C:/Lexos-master/lexos.py")){
    Write-Host "we cannot found Lexos" -ForegroundColor Red
    Write-Host "please run the install.exe or update.exe" -ForegroundColor Red
}

Start-Process cmd.exe -ArgumentList "/K $HOME/Anaconda2/python.exe C:/Lexos-master/lexos.py"

Write-Host ' '
Write-Host 'Opening your defualt browser...'
Start-Sleep -Seconds 3
Start-Process 'http://localhost:5000'

Write-Host 'Lexos is successfulling running' -ForegroundColor Green
Write-Host 'if you want to close Lexos, just close the other command prompt' -ForegroundColor Green
Read-Host 'you can press enter to close this window now'