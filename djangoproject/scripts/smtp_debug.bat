@ECHO OFF


:BEGIN
cd %~dp0
c:\python25\python.exe -m smtpd -n -c DebuggingServer 0.0.0.0:25
GOTO BEGIN
 
