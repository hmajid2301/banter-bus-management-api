from fastapi import status

add_question_data = [
    (
        "quibly",
        {"content": "this is another question?", "round": "pair"},
        status.HTTP_201_CREATED,
        {
            "game_name": "quibly",
            "round": "pair",
            "enabled": True,
            "content": {"en": "this is another question?"},
        },
    ),
    (
        "drawlosseum",
        {"content": "pencil"},
        status.HTTP_201_CREATED,
        {
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {"en": "pencil"},
        },
    ),
    (
        "fibbing_it",
        {
            "content": "do you love bikes?",
            "language_code": "en",
            "round": "opinion",
            "game_name": "fibbing_it",
            "group": {
                "name": "bike",
                "type": "question",
            },
        },
        status.HTTP_201_CREATED,
        {
            "game_name": "fibbing_it",
            "enabled": True,
            "round": "opinion",
            "content": {"en": "do you love bikes?"},
            "group": {
                "name": "bike",
                "type": "question",
            },
        },
    ),
    (
        "invalid",
        {
            "game_name": "quibly",
            "content": "hello",
            "round": "invalid",
        },
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "quibly",
        {"game_name": "quibly", "round": "group", "language_code": "fr", "content": "this is a another question?"},
        status.HTTP_409_CONFLICT,
        {},
    ),
    (
        "fibbing_it",
        {
            "round": "opinion",
            "language_code": "en",
            "content": "What do you think about horses?",
            "group": {
                "name": "horse_group",
                "type": "question",
            },
        },
        status.HTTP_409_CONFLICT,
        {},
    ),
    (
        "drawlosseum",
        {
            "content": "spoon",
        },
        status.HTTP_409_CONFLICT,
        {},
    ),
    (
        "quibly",
        {
            "game_name": "quibly",
            "content": "hello",
            "round": "invalid",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
    ("drawlosseum", {}, status.HTTP_422_UNPROCESSABLE_ENTITY, {}),
    (
        "fibbing_it",
        {
            "game_name": "quibly",
            "content": "hello",
            "round": "invalid",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
    (
        "fibbing_it",
        {
            "content": "do you love bikes?",
            "language_code": "ena",
            "round": "opinion",
            "game_name": "fibbing_it",
            "group": {
                "name": "bike",
                "type": "question",
            },
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
]

get_question_data = [
    (
        "quibly",
        "4d18ac45-8034-4f8e-b636-cf730b17e51a",
        status.HTTP_200_OK,
        {
            "question_id": "4d18ac45-8034-4f8e-b636-cf730b17e51a",
            "game_name": "quibly",
            "round": "pair",
            "enabled": True,
            "content": {"en": "this is a question?", "ur": "this is a question?", "de": "this is a question?"},
        },
    ),
    (
        "fibbing_it",
        "7799e38a-758d-4a1b-a191-99c59440af76",
        status.HTTP_200_OK,
        {
            "question_id": "7799e38a-758d-4a1b-a191-99c59440af76",
            "game_name": "fibbing_it",
            "round": "opinion",
            "group": {"type": "question", "name": "horse_group"},
            "enabled": True,
            "content": {"en": "What do you think about camels?"},
        },
    ),
    (
        "drawlosseum",
        "101464a5-337f-4ce7-a4df-2b00764e5d8d",
        status.HTTP_200_OK,
        {
            "question_id": "101464a5-337f-4ce7-a4df-2b00764e5d8d",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {"en": "spoon"},
        },
    ),
    (
        "drawlosseum",
        "1101010",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "drawlosseum_v3",
        "101464a5-337f-4ce7-a4df-2b00764e5d8d",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
]


remove_question_data = [
    (
        "quibly",
        "4d18ac45-8034-4f8e-b636-cf730b17e51a",
        status.HTTP_200_OK,
    ),
    (
        "fibbing_it",
        "7799e38a-758d-4a1b-a191-99c59440af76",
        status.HTTP_200_OK,
    ),
    (
        "drawlosseum",
        "101464a5-337f-4ce7-a4df-2b00764e5d8d",
        status.HTTP_200_OK,
    ),
    (
        "drawlosseum",
        "1101010",
        status.HTTP_404_NOT_FOUND,
    ),
    (
        "drawlosseum_v3",
        "101464a5-337f-4ce7-a4df-2b00764e5d8d",
        status.HTTP_404_NOT_FOUND,
    ),
]

enabled_question_data = [
    (
        "quibly",
        "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
        status.HTTP_200_OK,
        {
            "question_id": "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
            "game_name": "quibly",
            "round": "pair",
            "enabled": True,
            "content": {"en": "this is also question?", "ur": "this is also question?", "de": "this is also question?"},
        },
    ),
    (
        "fibbing_it",
        "3e2889f6-56aa-4422-a7c5-033eafa9fd39",
        status.HTTP_200_OK,
        {
            "question_id": "3e2889f6-56aa-4422-a7c5-033eafa9fd39",
            "game_name": "fibbing_it",
            "round": "opinion",
            "group": {"type": "question", "name": "horse_group"},
            "enabled": True,
            "content": {"en": "What do you think about horses?"},
        },
    ),
    (
        "fibbing_it",
        "a-random-id",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "fibbing_it_v3",
        "3e2889f6-56aa-4422-a7c5-033eafa9fd39",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
]

disabled_question_data = [
    (
        "fibbing_it",
        "580aeb14-d907-4a22-82c8-f2ac544a2cd1",
        status.HTTP_200_OK,
        {
            "question_id": "580aeb14-d907-4a22-82c8-f2ac544a2cd1",
            "game_name": "fibbing_it",
            "round": "free_form",
            "group": {"name": "bike_group"},
            "enabled": False,
            "content": {"en": "Favourite bike colour?"},
        },
    ),
    (
        "fibbing_it",
        "aa9fe2b5-79b5-458d-814b-45ff95a617fc",
        status.HTTP_200_OK,
        {
            "question_id": "aa9fe2b5-79b5-458d-814b-45ff95a617fc",
            "game_name": "fibbing_it",
            "round": "free_form",
            "group": {"name": "bike_group"},
            "enabled": False,
            "content": {"en": "A funny question?"},
        },
    ),
    (
        "fibbing_it",
        "a-random-id",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "fibbing_it_v3",
        "3e2889f6-56aa-4422-a7c5-033eafa9fd39",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
]

add_question_translation_data = [
    (
        "quibly",
        "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
        "en",
        {"content": "english question"},
        status.HTTP_201_CREATED,
        {
            "question_id": "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
            "game_name": "quibly",
            "round": "group",
            "enabled": True,
            "content": {"fr": "this is a another question?", "en": "english question"},
        },
    ),
    (
        "fibbing_it",
        "3e2889f6-56aa-4422-a7c5-033eafa9fd39",
        "ur",
        {"content": "hello"},
        status.HTTP_201_CREATED,
        {
            "question_id": "3e2889f6-56aa-4422-a7c5-033eafa9fd39",
            "game_name": "fibbing_it",
            "round": "opinion",
            "group": {"type": "question", "name": "horse_group"},
            "enabled": True,
            "content": {"en": "What do you think about horses?", "ur": "hello"},
        },
    ),
    (
        "drawlosseum",
        "101464a5-337f-4ce7-a4df-2b00764e5d8d",
        "de",
        {"content": "german question"},
        status.HTTP_201_CREATED,
        {
            "question_id": "101464a5-337f-4ce7-a4df-2b00764e5d8d",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {"en": "spoon", "de": "german question"},
        },
    ),
    (
        "quibly_v3",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        {"content": "german question"},
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "quibly",
        "81546-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        {"content": "german question"},
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "quibly",
        "bf64d60c-62ee-420a-976e-bfcaec77ad8b",
        "en",
        {"content": "german question"},
        status.HTTP_409_CONFLICT,
        {},
    ),
    (
        "drawlosseum",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "ena",
        {"content": "german question"},
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
]

get_question_translation_data = [
    (
        "quibly",
        "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
        "fr",
        status.HTTP_200_OK,
        {
            "question_id": "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
            "game_name": "quibly",
            "round": "group",
            "language_code": "fr",
            "enabled": True,
            "content": "this is a another question?",
        },
    ),
    (
        "fibbing_it",
        "714464a5-337f-4ce7-a4df-2b00764e5c5b",
        "en",
        status.HTTP_200_OK,
        {
            "question_id": "714464a5-337f-4ce7-a4df-2b00764e5c5b",
            "game_name": "fibbing_it",
            "language_code": "en",
            "round": "likely",
            "enabled": False,
            "content": "to get arrested",
        },
    ),
    (
        "drawlosseum",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        status.HTTP_200_OK,
        {
            "question_id": "815464a5-337f-4ce7-a4df-2b00764e5c6c",
            "game_name": "drawlosseum",
            "language_code": "en",
            "enabled": True,
            "content": "horse",
        },
    ),
    (
        "quibly_v3",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "quibly",
        "81546-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "drawlosseum",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "ena",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
]


delete_question_translation = [
    (
        "quibly",
        "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
        "en",
        status.HTTP_200_OK,
        {
            "question_id": "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
            "game_name": "quibly",
            "round": "pair",
            "enabled": False,
            "content": {"ur": "this is also question?", "de": "this is also question?"},
        },
    ),
    (
        "fibbing_it",
        "714464a5-337f-4ce7-a4df-2b00764e5c5b",
        "en",
        status.HTTP_200_OK,
        {
            "question_id": "714464a5-337f-4ce7-a4df-2b00764e5c5b",
            "game_name": "fibbing_it",
            "round": "likely",
            "enabled": False,
            "content": {},
        },
    ),
    (
        "drawlosseum",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        status.HTTP_200_OK,
        {
            "question_id": "815464a5-337f-4ce7-a4df-2b00764e5c6c",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {},
        },
    ),
    (
        "quibly_v3",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "quibly",
        "81546-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        status.HTTP_404_NOT_FOUND,
        {},
    ),
    (
        "drawlosseum",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "ena",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        {},
    ),
]
