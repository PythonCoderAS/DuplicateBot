@echo off
SET /P somevar= Username:
echo %somevar%>>blockusers.txt
updateblockedusers.bat
