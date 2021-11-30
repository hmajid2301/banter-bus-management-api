from app.game.game_exceptions import GameNotFound
from app.question.question_exceptions import (
    InvalidLanguageCode,
    QuestionExistsException,
    QuestionNotFound,
)

add_question_data = [
    (
        {"content": "this is a question?", "round": "pair", "game_name": "quibly"},
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "quibly",
            "round": "pair",
            "enabled": True,
            "content": {"en": "this is a question?"},
        },
    ),
    (
        {
            "content": "what is the funniest thing ever told?",
            "round": "answer",
            "language_code": "de",
            "game_name": "quibly",
        },
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "quibly",
            "round": "answer",
            "enabled": True,
            "content": {"de": "what is the funniest thing ever told?"},
        },
    ),
    (
        {"content": "what does ATGM stand for?", "round": "group", "game_name": "quibly"},
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "quibly",
            "round": "group",
            "enabled": True,
            "content": {"en": "what does ATGM stand for?"},
        },
    ),
    (
        {"content": "pencil", "game_name": "drawlosseum"},
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {"en": "pencil"},
        },
    ),
    (
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
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
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
        {
            "content": "bikes are super cool",
            "round": "opinion",
            "game_name": "fibbing_it",
            "group": {
                "name": "bike",
                "type": "answer",
            },
        },
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "fibbing_it",
            "enabled": True,
            "round": "opinion",
            "content": {"en": "bikes are super cool"},
            "group": {
                "name": "bike",
                "type": "answer",
            },
        },
    ),
    (
        {
            "game_name": "fibbing_it",
            "content": "what is the fastest horse?",
            "round": "free_form",
            "group": {
                "name": "horse",
            },
        },
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "fibbing_it",
            "enabled": True,
            "round": "free_form",
            "content": {"en": "what is the fastest horse?"},
            "group": {
                "name": "horse",
            },
        },
    ),
    (
        {
            "game_name": "fibbing_it",
            "content": "to never eat a vegetable again?",
            "round": "likely",
        },
        {
            "question_id": "5ecd5827-b6ef-4067-b5ac-3ceac07dde9f",
            "game_name": "fibbing_it",
            "enabled": True,
            "round": "likely",
            "content": {"en": "to never eat a vegetable again?"},
        },
    ),
]

add_question_data_fail = [
    (
        {
            "game_name": "quibly",
            "content": "hello",
            "round": "invalid",
        },
        ValueError,
    ),
    (
        {
            "game_name": "quibly",
            "content": "hello",
        },
        ValueError,
    ),
    (
        {
            "game_name": "drawlosseum",
        },
        ValueError,
    ),
    (
        {
            "game_name": "fibbing_it",
            "content": "What is the fastest horse?",
            "round": "invalid",
            "group": {"name": "horse"},
        },
        ValueError,
    ),
    (
        {
            "game_name": "fibbing_it",
            "content": "super love",
            "round": "opinion",
            "group": {"name": "horse", "type": "invalid"},
        },
        ValueError,
    ),
    (
        {
            "game_name": "fibbing_it",
            "content": "super love",
            "round": "opinion",
        },
        ValueError,
    ),
    (
        {
            "game_name": "fibbing_it",
            "content": "super love",
            "round": "opinion",
            "group": {"name": "horse", "type": "answer"},
            "language_code": "enda",
        },
        InvalidLanguageCode,
    ),
    (
        {
            "game_name": "fibbing_it_v3",
            "content": "super love",
            "round": "opinion",
            "group": {"name": "horse", "type": "answer"},
        },
        GameNotFound,
    ),
    ({"game_name": "quibly", "round": "pair", "content": "this is a question?"}, QuestionExistsException),
    ({"game_name": "quibly", "round": "answer", "language_code": "de", "content": "german"}, QuestionExistsException),
    (
        {"game_name": "quibly", "round": "group", "language_code": "fr", "content": "this is a another question?"},
        QuestionExistsException,
    ),
    (
        {
            "game_name": "fibbing_it",
            "round": "opinion",
            "language_code": "en",
            "content": "What do you think about horses?",
            "group": {
                "name": "horse_group",
                "type": "question",
            },
        },
        QuestionExistsException,
    ),
    (
        {
            "game_name": "fibbing_it",
            "round": "free_form",
            "content": "A funny question?",
            "group": {
                "name": "bike_group",
            },
        },
        QuestionExistsException,
    ),
    (
        {
            "game_name": "fibbing_it",
            "round": "likely",
            "content": "to eat ice-cream from the tub",
        },
        QuestionExistsException,
    ),
    (
        {
            "game_name": "drawlosseum",
            "content": "spoon",
        },
        QuestionExistsException,
    ),
]


get_question_data = [
    (
        "4d18ac45-8034-4f8e-b636-cf730b17e51a",
        "quibly",
        {
            "question_id": "4d18ac45-8034-4f8e-b636-cf730b17e51a",
            "game_name": "quibly",
            "round": "pair",
            "enabled": True,
            "content": {"en": "this is a question?", "ur": "this is a question?", "de": "this is a question?"},
        },
    ),
    (
        "7799e38a-758d-4a1b-a191-99c59440af76",
        "fibbing_it",
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
        "101464a5-337f-4ce7-a4df-2b00764e5d8d",
        "drawlosseum",
        {
            "question_id": "101464a5-337f-4ce7-a4df-2b00764e5d8d",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {"en": "spoon"},
        },
    ),
]

update_enabled_status_question_data = [
    ("quibly", "a9c00e19-d41e-4b15-a8bd-ec921af9123d"),
    (
        "quibly",
        "4d18ac45-8034-4f8e-b636-cf730b17e51a",
    ),
]

add_question_translation_data = [
    (
        "quibly",
        "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
        "en",
        "english question",
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
        "hello",
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
        "german question",
        {
            "question_id": "101464a5-337f-4ce7-a4df-2b00764e5d8d",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {"en": "spoon", "de": "german question"},
        },
    ),
]

add_question_translation_fail_data = [
    ("quibly_v3", "815464a5-337f-4ce7-a4df-2b00764e5c6c", "en", "hello", GameNotFound),
    ("quibly", "81546-337f-4ce7-a4df-2b00764e5c6c", "en", "hello", QuestionNotFound),
    ("quibly", "bf64d60c-62ee-420a-976e-bfcaec77ad8b", "en", "hello", QuestionExistsException),
    ("quibly", "815464a5-337f-4ce7-a4df-2b00764e5c6c", "ena", "hello", InvalidLanguageCode),
]


get_question_translation_data = [
    (
        "quibly",
        "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
        "fr",
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
        "quibly",
        "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
        "en",
        {
            "question_id": "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
            "game_name": "quibly",
            "language_code": "en",
            "round": "pair",
            "enabled": False,
            "content": "this is also question?",
        },
    ),
    (
        "fibbing_it",
        "7799e38a-758d-4a1b-a191-99c59440af76",
        "en",
        {
            "question_id": "7799e38a-758d-4a1b-a191-99c59440af76",
            "game_name": "fibbing_it",
            "round": "opinion",
            "language_code": "en",
            "group": {"type": "question", "name": "horse_group"},
            "enabled": True,
            "content": "What do you think about camels?",
        },
    ),
    (
        "fibbing_it",
        "580aeb14-d907-4a22-82c8-f2ac544a2cd1",
        "en",
        {
            "question_id": "580aeb14-d907-4a22-82c8-f2ac544a2cd1",
            "game_name": "fibbing_it",
            "round": "free_form",
            "language_code": "en",
            "group": {"name": "bike_group"},
            "enabled": True,
            "content": "Favourite bike colour?",
        },
    ),
    (
        "fibbing_it",
        "714464a5-337f-4ce7-a4df-2b00764e5c5b",
        "en",
        {
            "question_id": "714464a5-337f-4ce7-a4df-2b00764e5c5b",
            "game_name": "fibbing_it",
            "round": "likely",
            "language_code": "en",
            "enabled": False,
            "content": "to get arrested",
        },
    ),
    (
        "drawlosseum",
        "815464a5-337f-4ce7-a4df-2b00764e5c6c",
        "en",
        {
            "question_id": "815464a5-337f-4ce7-a4df-2b00764e5c6c",
            "game_name": "drawlosseum",
            "language_code": "en",
            "enabled": True,
            "content": "horse",
        },
    ),
]

get_question_translation_fail_data = [
    ("quibly_v3", "815464a5-337f-4ce7-a4df-2b00764e5c6c", "en", GameNotFound),
    ("quibly", "81546-337f-4ce7-a4df-2b00764e5c6c", "en", QuestionNotFound),
    ("quibly", "815464a5-337f-4ce7-a4df-2b00764e5c6c", "ena", InvalidLanguageCode),
]


remove_question_translation_data = [
    (
        "quibly",
        "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
        "fr",
        {
            "question_id": "4b4dd325-04fd-4aa4-9382-2874dcfd5cae",
            "game_name": "quibly",
            "round": "group",
            "enabled": True,
            "content": {},
        },
    ),
    (
        "quibly",
        "a9c00e19-d41e-4b15-a8bd-ec921af9123d",
        "en",
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
        "7799e38a-758d-4a1b-a191-99c59440af76",
        "en",
        {
            "question_id": "7799e38a-758d-4a1b-a191-99c59440af76",
            "game_name": "fibbing_it",
            "round": "opinion",
            "group": {"type": "question", "name": "horse_group"},
            "enabled": True,
            "content": {},
        },
    ),
    (
        "fibbing_it",
        "580aeb14-d907-4a22-82c8-f2ac544a2cd1",
        "en",
        {
            "question_id": "580aeb14-d907-4a22-82c8-f2ac544a2cd1",
            "game_name": "fibbing_it",
            "round": "free_form",
            "group": {"name": "bike_group"},
            "enabled": True,
            "content": {},
        },
    ),
    (
        "fibbing_it",
        "714464a5-337f-4ce7-a4df-2b00764e5c5b",
        "en",
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
        {
            "question_id": "815464a5-337f-4ce7-a4df-2b00764e5c6c",
            "game_name": "drawlosseum",
            "enabled": True,
            "content": {},
        },
    ),
]

remove_question_translation_fail_data = [
    ("quibly_v3", "815464a5-337f-4ce7-a4df-2b00764e5c6c", "en", GameNotFound),
    ("quibly", "81546-337f-4ce7-a4df-2b00764e5c6c", "en", QuestionNotFound),
    ("quibly", "815464a5-337f-4ce7-a4df-2b00764e5c6c", "ena", InvalidLanguageCode),
]
