mkdir salai_data\foia_data
docker run -p 8080:8080 -v "%CD%\salai_data":/label-studio/data --name atc-transcriptions avandebrook/salai-data-labeling
