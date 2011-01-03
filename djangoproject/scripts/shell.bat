@ECHO OFF


:BEGIN
cd %~dp0
c:\python25\python.exe manage.py shell
GOTO BEGIN
 
