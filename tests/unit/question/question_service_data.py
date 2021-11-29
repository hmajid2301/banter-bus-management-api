from app.game.game_exceptions import GameNotFound
from app.question.question_exceptions import QuestionExistsException

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
            "language": "de",
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
            "language": "en",
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
            "game_name": "fibbing_it_v3",
            "content": "super love",
            "round": "opinion",
            "group": {"name": "horse", "type": "answer"},
        },
        GameNotFound,
    ),
    ({"game_name": "quibly", "round": "pair", "content": "this is a question?"}, QuestionExistsException),
    ({"game_name": "quibly", "round": "answer", "language": "de", "content": "german"}, QuestionExistsException),
    (
        {"game_name": "quibly", "round": "group", "language": "fr", "content": "this is a another question?"},
        QuestionExistsException,
    ),
    (
        {
            "game_name": "fibbing_it",
            "round": "opinion",
            "language": "en",
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
