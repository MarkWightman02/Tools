@echo off
set source_folder=path
set destination_folder=path

echo Moving files from %source_folder% to %destination_folder%...

for /r "%source_folder%" %%f in (*) do (
    move "%%f" "%destination_folder%"
)

echo Done.
