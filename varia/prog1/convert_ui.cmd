@echo off

pyuic5 main_form.ui -o main_form.py
if errorlevel 1 goto err


exit

:err
pause
exit
