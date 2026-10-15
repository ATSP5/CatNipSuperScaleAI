Rekord jednego gotowego modelu super-rozdzielczości (`@dataclass`): nazwa, ile razy powiększa, skąd go pobrać i jaką ma sumę SHA-256. Lista modeli jest w bloku Config (`models`).

## name
Nazwa do wydruków, np. `Real-ESRGAN x4plus`.

## scale
Ile razy model powiększa bok w jednym przejściu (2 albo 4).

## url
Adres pliku wag.

## sha256
Suma kontrolna pliku. Pobrany plik musi się z nią zgadzać. Pusty tekst wyłącza sprawdzanie.

## file_name
Nazwa pliku w `models/`, wzięta z adresu.
