Odczyt, zapis i podgląd obrazów przez OpenCV, także dla ścieżek z polskimi znakami.

## read
`read(path)` zwraca obraz BGR `uint8` z uwzględnionym obrotem EXIF.

## write
`write(image, path)` zapisuje obraz. Format wynika z rozszerzenia.

## show
`show(title, image)` pokazuje obraz w zakładce Output CatNip (CatNip przechwytuje `cv2.imshow`, także w Dockerze).

## compare_detail
`compare_detail(title, original, result)` pokazuje wycinek 1:1 ze środka zdjęcia: po lewej zwykłe powiększenie (bicubic), po prawej wynik AI. Na pomniejszonym całym zdjęciu różnicy nie widać, dlatego porównanie jest w pełnej skali.
