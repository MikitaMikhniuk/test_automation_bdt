Feature: Catalog TV Filter
    As a regular user
    I want to navigate to TV's catalog page and filter them
    based on some params

    Scenario: Filter TV's based on params
        Given website "https://www.onliner.by/"
        When "Каталог" page is opened
        And navigate to "Электроника" -> "Телевидение и видео" -> "Телевизоры"
        Then apply following filters and verify results
            |   Filter     |   Value               |
            |   vendor     |   Samsung             |
            |   max_price  |   2000                |
            |   resolution |   1920x1080 (Full HD) |
            |   min_size   |   400                 |
            |   max_size   |   500                 |