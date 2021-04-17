class Entry():
    def __init__(self, id, date, concept, text, mood_id):
        self.id = id
        self.name = date
        self.breed = concept
        self.status = text
        self.mood_id = mood_id
        self.mood = None