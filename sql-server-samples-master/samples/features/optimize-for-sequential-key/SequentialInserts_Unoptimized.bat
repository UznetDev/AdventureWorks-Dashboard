ECHO OFF
rd /s /q %temp%\output
"ostress.exe" -E -S. -dAdventureWorks2016_EXT -Q"EXEC usp_InsertLogRecord" -mstress -quiet -n1 -r1 | FINDSTR "Cantfindthisstring"
rd /s /q %temp%\output
"ostress.exe" -E -S. -dAdventureWorks2016_EXT -Q"EXEC usp_InsertLogRecord" -mstress -quiet -n256 -r250 | FINDSTR "QEXEC Starting Creating elapsed"
