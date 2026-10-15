Zbiera zdjęcia wskazane we **wszystkich** blokach File content projektu. Jeden blok to jedno zdjęcie, a kolejność wynika z numerów bloków. Ścieżki czyta wprost z `SuperScaleAI.catnip`, bo ręcznie pisany main nie dostaje ich z *Generate Blueprint*.

W Dockerze ścieżka `C:\...` nie istnieje, więc plik jest wtedy szukany po nazwie obok projektu i w `Inputs/`. Zdjęcia do uruchomień w Dockerze trzymaj w `Inputs/` albo użyj opcji *Copy to source*.

## config
`SuperScaleConfig`.

## picked_photos
Lista istniejących plików obrazów, bez duplikatów. Brakujące pliki i pliki niebędące obrazami są pomijane z komunikatem.

## paths_from_blocks
Ścieżki zapisane w blokach File content.

## resolve
Ścieżka z bloku, a gdy plik nie istnieje, ten sam plik szukany po nazwie.

## find_project
Plik `.catnip` w folderze projektu.
