@echo on 
for /f "delims=" %%i in (list.txt) do call :procedure %%i
pause& exit
 
:procedure
 xcopy "Launcher.exe"	 "\\%1\c$\Program Files\" /y
 xcopy "kkt_time_fix.exe" "\\%1\c$\Program Files\" /y
exit /b