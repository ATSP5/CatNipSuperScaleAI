Plan dla jednego zdjęcia (`@dataclass`): obecny rozmiar, rozmiar docelowy, użyty model i liczba przejść sieci.

## side_scale_for
`side_scale_for(factor, factor_mode)` zamienia mnożnik na powiększenie boku. W trybie `pixels` to √mnożnik, w trybie `side` sam mnożnik.

## build
`build(width, height, factor, factor_mode, model_scale)` liczy rozmiar docelowy i liczbę przejść. Zawsze jest co najmniej jedno przejście, więc mnożnik 1 też poprawia jakość.

## pixel_gain
Ile razy więcej pikseli ma wynik.

## describe
Jedna linijka opisu planu do wydruku.
