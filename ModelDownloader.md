Pobiera wagi modelu do `models/` przy pierwszym użyciu (~64 MB na model). Używa tylko biblioteki standardowej. Przerwane pobieranie jest wznawiane (HTTP Range, do 20 prób), a gotowy plik musi się zgadzać z sumą SHA-256. Uszkodzony plik jest pobierany od nowa.

## config
`SuperScaleConfig`.

## ensure_model
`ensure_model(spec)` zwraca ścieżkę do pliku wag. Najpierw pobiera go, jeśli go nie ma albo jest uszkodzony.

## verify
`verify(path, sha256)` sprawdza, czy plik ma oczekiwaną sumę SHA-256.

## fetch_file
`fetch_file(url, target)` pobiera jeden plik z wznawianiem.
