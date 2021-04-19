class Entry():
    def __init__(self, id, date, concept, text, mood_id):
        self.id = id
        self.date = date
        self.concept = concept
        self.text = text
        self.mood_id = mood_id
        self.mood = None