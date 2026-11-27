
init -10 python:

    class StoryCharacter:
        def __init__(self, character_id, name, image):
            self.character_id = character_id
            self.name = name
            self.image = image


    class StoryEvent:
        def __init__(
            self,
            event_id,
            character_id,
            day_number,
            label,
            comments
        ):
            self.event_id = event_id
            self.character_id = character_id
            self.day_number = day_number
            self.label = label
            self.comments = comments

        def get_interaction_comment(character, result, story_comments):
            if isinstance(character, Client):
                return character.get_comment(result)

            if isinstance(character, StoryCharacter):
                if isinstance(result, MiniGameResult):
                    result = result.name.lower()

                return story_comments.get(result, '')

            return ''


    class StoryManager:
        def __init__(self, characters, events):
            self.characters = {
                character.character_id: character
                for character in characters
            }
            self.events = events

        def get_events(self, day_number, completed_events):
            return [
                event for event in self.events
                if event.day_number == day_number
                and not completed_events.get(event.event_id, False)
            ]

        def complete_event(self, event, completed_events):
            completed_events[event.event_id] = True

        def apply_result(self, event_id, result, story_flags):
            event_rules = STORY_RESULT_RULES.get(event_id, {})
            result_rules = event_rules.get(result, {})

            story_flags.update(result_rules)
    
    def get_interaction_comment(character, result, story_comments):

        if isinstance(character, Client):
            return character.get_comment(result)

        if isinstance(character, StoryCharacter):
            return story_comments.get(result, '')

        return ''
