@goto restart

:restart
@taskkill /f /im python.exe >nul
@timeout /t 2 /nobreak >nul
@start goldy.py >nul
@echo restart complete
@goto exit

:exit
EXIT