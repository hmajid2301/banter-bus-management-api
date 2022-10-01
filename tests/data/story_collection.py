from app.core.models import DrawingPoint
from app.story.story_models import (
    CaertsianCoordinateColor,
    FibbingItAnswer,
    QuiblyAnswer,
    Story,
)

stories: list[Story] = [
    Story(
        story_id="1def4233-f674-4a3f-863d-6e850bfbfdb4",
        game_name="quibly",
        question="how many fish are there?",
        round_="pair",
        answers=[
            QuiblyAnswer(nickname="funnyMan420", answer="one", votes=12341),
            QuiblyAnswer(nickname="123456", answer="many", votes=0),
        ],
    ),
    Story(
        story_id="a4ffd1c8-93c5-4f4c-8ace-71996edcbcb7",
        game_name="drawlosseum",
        question="fish",
        nickname="i_cannotDraw",
        answers=[
            CaertsianCoordinateColor(start=DrawingPoint(x=100, y=-100), end=DrawingPoint(x=90, y=-100), color="#000")
        ],
    ),
    Story(
        story_id="479d0463-ed35-44bf-a976-801367be4246",
        game_name="fibbing_it",
        question="What do you think about horses?",
        round_="opinion",
        answers=[
            FibbingItAnswer(answer="tasty", nickname="!sus"),
            FibbingItAnswer(answer="lame", nickname="normal_guy1"),
            FibbingItAnswer(answer="lame", nickname="normal_girl1"),
            FibbingItAnswer(answer="lame", nickname="normal_person1"),
        ],
    ),
    Story(
        story_id="a5d158b5-7fc4-419b-8299-7363d1567840",
        game_name="fibbing_it",
        question="what do you think about horses?",
        round_="free_form",
        answers=[
            FibbingItAnswer(answer="tasty", nickname="!sus"),
            FibbingItAnswer(answer="hello", nickname="normal_guy1"),
            FibbingItAnswer(answer="what is a horse?", nickname="normal_girl1"),
            FibbingItAnswer(answer="is this a real game?", nickname="normal_person1"),
        ],
    ),
    Story(
        story_id="8a7e92a9-2bc2-43f1-be33-2ff8645b227c",
        game_name="fibbing_it",
        question="most likely to get arrested?",
        round_="likely",
        answers=[
            FibbingItAnswer(answer="normal_guy1", nickname="!sus"),
            FibbingItAnswer(answer="normal_girl1", nickname="normal_guy1"),
            FibbingItAnswer(answer="!sus", nickname="normal_girl1"),
            FibbingItAnswer(answer="normal_girl1", nickname="normal_person1"),
        ],
    ),
]
