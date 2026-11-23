init -10 python:

    class StoryCharacter:
        def __init__(self, character_id, name, image):
            self.character_id = character_id
            self.name = name
            self.image = image


    class StoryEvent:
        def __init__(self, event_id, character_id, day_number, label):
            self.event_id = event_id
            self.character_id = character_id
            self.day_number = day_number
            self.label = label


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