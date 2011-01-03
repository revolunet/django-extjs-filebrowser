@ECHO OFF

SET PORT=8003

:BEGIN
cd %~dp0
c:\pythoN25\python.exe manage.py runconcurrentserver 0.0.0.0:%PORT%
GOTO BEGIN
 
