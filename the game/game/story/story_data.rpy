init 0 python:

    STORY_CHARACTERS = [
        StoryCharacter(
            "ofela",
            "Офеля",
            "sad_client",
        )
    ]

    STORY_EVENTS = [
        StoryEvent(
            "ofela_day_1", #id
            "ofela", #character_id
            1, #day_number
            "ofela_day_1", #label
            { #comments
                "bad": "...Это все? Ну... Ладно. Пока.",
                "medium": "Спасибо! Пока.",
                "good": "Господи, ты меня спас!! Спасибо большое, я обязательно тебе отплачу."
            }
        ),

        StoryEvent(
            "ofela_day_3",
            "ofela",
            3,
            "ofela_day_3",
            {
                "bad": "Я ожидала от тебя большего.",
                "medium": "Уже лучше, спасибо.",
                "good": "Вот это работа! Ты меня впечатлил."
            }
        ),
    ]

    STORY_RESULT_RULES = {
        "ofela_day_1": {
            MiniGameResult.GOOD: {
                "ofela_helped": True
            },
            MiniGameResult.MEDIUM: {
                "ofela_helped": True
            },
            MiniGameResult.BAD: {
                "ofela_helped": False
            }
        },

        "ofela_day_2": {
            MiniGameResult.GOOD: {
                "ofela_trust": True
            }
        }
    }
