  pushd sourcefolder
   for /r %%a in (*.docx) do (
     COPY "%%a" "destinationfolder"
   )
   popd