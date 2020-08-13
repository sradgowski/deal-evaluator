""" Scoring Machine for Descriptions """

positive_words = ["recurring revenue", "repeat revenue", "b2b", "b2b service",\
    "business-to-business", "service", "customer retention", "retire", "retiring",\
    "stepping down", "retirement"]

negative_words = ["restaurant", "gas station", "minority-owned", "minority owned",\
    "minority owner", "woman-owned", "women-owned",  "woman owned", "women owned",\
    "women owner", "woman owner", "veteran-owned", "veteran owned", "veteran owner",\
    "convenience store", "cafe", "eatery", "dining establishment", "bistro", "diner",\
    "bar", "grill", "pub", "service-disabled", "franchise", "franchise", "franchisor",\
    "franchisor", "franchiser", "franchiser", "franchised", "franchize", "franchize",\
    "franchizor", "franchizor", "franchizer", "franchizer", "franchized", "oilfield",\
    "oil field", "swimming pool"]


def make_keywords(positive_inputs, negative_inputs):
    pos_plurals = [word+"s" for word in positive_inputs]
    neg_plurals = [word+"s" for word in negative_inputs]
    pos_full = positive_inputs + pos_plurals
    neg_full = negative_inputs + neg_plurals

    pos_keys = []
    neg_keys = []
    punctuation = [" ", ".", ",", ";", ":", "?", '"', "'", "+", "-", ")", "(", "{",\
        "}", "[", "]", "/", "#", "$", "%", "&", "*", "@", "<", ">", "?", "!", "\\",\
        "`", "^", "_", "|", "~"]

    for mark1 in punctuation:
        for mark2 in punctuation:
            for word in pos_full:
                pos_keys.append(mark1 + word + mark2)
            for word in neg_full:
                neg_keys.append(mark1 + word + mark2)

    return pos_full, neg_full, pos_keys, neg_keys

def score(description, positive_inputs=positive_words, negative_inputs=negative_words):
    pos_full, neg_full, pos_keys, neg_keys = make_keywords(positive_inputs, negative_inputs)

    ncs_description = description.lower() # Non-case-sensitive
    score = 0

    for word in pos_full:
        if word in ncs_description[:len(word) + 1]:
            score += 1
    for word in neg_full:
        if word in ncs_description[:len(word) + 1]:
            score -= 1

    for word in pos_keys:
        if word in ncs_description:
            score += 1
    for word in neg_keys:
        if word in ncs_description:
            score -= 1

    return score
