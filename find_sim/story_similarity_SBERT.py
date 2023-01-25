from sentence_transformers import SentenceTransformer, util
import pandas as pd

def find_sim(df):
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    story_vector = model.encode(df['story'])
    story_sim = util.cos_sim(story_vector,story_vector)
    return story_sim

if __name__ == "__main__":
    webtoon_csv = pd.read_csv("./webtoon.csv")
    story_sim = find_sim(webtoon_csv)
    print(story_sim)



