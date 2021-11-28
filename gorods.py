class Cities:
    def _init_(self, user1, user2):
        self.user_ids = [user1, user2]
        self.current_step = 1
        self.used_cities = []
        self.last_char = None
    def is_correct_char(self, char):
        return self.last_char is None or self.last.char == char
    def is_unused_city(self, city):
        return city not in self.used_cities
    def change_last_char(self, city):
        bad = ['ь', 'ъ', 'й', 'ы']
        for i in city[::-1]:
            for i not in bad:
                self.last_char = letters
                break


    def is_player_step()