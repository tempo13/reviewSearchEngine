

class CreateEsIndex:

    def __init__(self):
        self.main_keyword = []
        self.synonym, self.exclude, self.multi_key, self.and_cond, \
        self.or_cond, self.woman, self.man, self.noun = [], [], [], [], [], [], [], []
        self.condition_map = {
            '-': self.exclude, '+': self.synonym, '|': self.or_cond, '&': self.and_cond,
            ',': self.multi_key, '^^': self.woman, '^~': self.man, '^&': self.noun
        }
        return

    @staticmethod
    def text_clear(keyword: str):
        rep_list = ['-', '+', '|', '&', ',', '^^', '^~', '^&']
        for r in rep_list:
            keyword = keyword.replace(r, '')
        return keyword

    def process_word(self, search_word: str):
        word_list = search_word.split(' ')
        for i in range(0, len(word_list)):
            w = word_list[i]
            if i == 0:
                self.main_keyword.append({"match": {"review": self.text_clear(w)}})
            [self.condition_map[s].append(self.text_clear(w)) if s in w else None for s in self.condition_map.keys()]

    def create_complex_query(self, search_word: str):
        self.process_word(search_word)
        q = {
            "query": {
                "bool": {
                    "must": self.main_keyword,
                    "must_not": [],
                    "should": []
                }
            }
        }
        bol = q['query']['bool']
        for k, v in self.condition_map.items():
            if not v:
                continue
            words = [{"match": {"review": w}} for w in v]
            if k == "+":
                bol['should'].extend(words)
            if k == "-":
                bol['must_not'].extend(words)
            if k == ",":
                bol['should'].extend(words)
            if k == "&":
                bol['must'].extend(words)
            if k == "|":
                bol['should'].extend(words)
            if k == "^^":
                boost = {"rank_feature": {"field": "genders.female", "boost": 4}}
                bol['should'].append(boost)
            if k == "^~":
                boost = {"rank_feature": {"field": "genders.male", "boost": 4}}
                bol['should'].append(boost)
            if k == "^&":
                words = [{"match": {"review.nori_noun": w}} for w in v]
                bol['should'].extend(words)
        return q

