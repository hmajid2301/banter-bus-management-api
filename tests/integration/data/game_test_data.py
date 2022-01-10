from fastapi import status

add_game_data = [
    (
        {
            "name": "quiblyv2",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quibly",
            "description": "a game",
            "display_name": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
        status.HTTP_201_CREATED,
        {
            "name": "quiblyv2",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quibly",
            "description": "a game",
            "display_name": "Quibly",
            "enabled": True,
            "minimum_players": 4,
            "maximum_players": 16,
        },
    ),
    (
        {
            "nam": "quibly",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quibly",
            "description": "a game",
            "display_name": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
    (
        {
            "name": "fibbing_it",
            "rul_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quiblyv2",
            "description": "a game",
            "display_name": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
    (
        {
            "name": "fibbing_it",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quiblyv2",
            "desc": "a test",
            "display_name": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
    (
        {
            "name": "fibbing_it",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quiblyv2",
            "description": "a test",
            "disp": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
    (
        {
            "name": "quibly",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quibly",
            "description": "a game",
            "display_name": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
        status.HTTP_409_CONFLICT,
        {},
    ),
]
remove_game_data = [
    (
        "quibly",
        status.HTTP_200_OK,
    ),
    ("quiblyv2", status.HTTP_404_NOT_FOUND),
]

get_game_data = [
    (
        "quibly",
        status.HTTP_200_OK,
        {
            "name": "quibly",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/quibly",
            "enabled": True,
            "description": "A game about quibbing.",
            "display_name": "Quibly",
            "minimum_players": 4,
            "maximum_players": 16,
        },
    ),
    (
        "fibbing_it",
        status.HTTP_200_OK,
        {
            "name": "fibbing_it",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/fibbing_it",
            "enabled": True,
            "description": "A game about lying.",
            "display_name": "Fibbing IT!",
            "minimum_players": 4,
            "maximum_players": 10,
        },
    ),
    ("quiblyv2", status.HTTP_404_NOT_FOUND, {}),
]

get_game_names = [
    (
        "",
        status.HTTP_200_OK,
        [
            "quibly",
            "fibbing_it",
            "drawlosseum",
        ],
    ),
    (
        "all",
        status.HTTP_200_OK,
        [
            "quibly",
            "fibbing_it",
            "drawlosseum",
        ],
    ),
    (
        "enabled",
        status.HTTP_200_OK,
        [
            "quibly",
            "fibbing_it",
        ],
    ),
    (
        "disabled",
        status.HTTP_200_OK,
        [
            "drawlosseum",
        ],
    ),
    (
        "invalid",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        [],
    ),
]


enabled_game_data = [
    (
        "drawlosseum",
        status.HTTP_200_OK,
        {
            "name": "drawlosseum",
            "rules_url": "https://google.com/drawlosseum",
            "enabled": True,
            "description": "A game about drawing.",
            "display_name": "Drawlosseum",
            "minimum_players": 4,
            "maximum_players": 16,
        },
    ),
    (
        "fibbing_it",
        status.HTTP_200_OK,
        {
            "name": "fibbing_it",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/fibbing_it",
            "enabled": True,
            "description": "A game about lying.",
            "display_name": "Fibbing IT!",
            "minimum_players": 4,
            "maximum_players": 10,
        },
    ),
    (
        "quiblyv3",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
]

disabled_game_data = [
    (
        "fibbing_it",
        status.HTTP_200_OK,
        {
            "name": "fibbing_it",
            "rules_url": "https://gitlab.com/banter-bus/banter-bus-server/-/wikis/docs/rules/fibbing_it",
            "enabled": False,
            "description": "A game about lying.",
            "display_name": "Fibbing IT!",
            "minimum_players": 4,
            "maximum_players": 10,
        },
    ),
    (
        "drawlosseum",
        status.HTTP_200_OK,
        {
            "name": "drawlosseum",
            "rules_url": "https://google.com/drawlosseum",
            "enabled": False,
            "description": "A game about drawing.",
            "display_name": "Drawlosseum",
            "minimum_players": 4,
            "maximum_players": 16,
        },
    ),
    (
        "quiblyv3",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
]
