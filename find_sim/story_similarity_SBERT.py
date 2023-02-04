from sentence_transformers import SentenceTransformer, util
import pandas as pd

def find_sim(df):
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    story_vector = model.encode(df['story'])
    story_sims = util.cos_sim(story_vector,story_vector)
    return story_sims

if __name__ == "__main__":
    sim_df = pd.DataFrame()
    webtoon_csv = pd.read_csv("../webtoon/webtoon_story.csv")
    story_sims = find_sim(webtoon_csv)
    sim_df["title_id"] = webtoon_csv['title_id']
    for _id,story_sim in zip(webtoon_csv['title_id'],story_sims):
        sim_df[_id] = story_sim
    sim_df.to_csv("sim.csv")
    print(sim_df)


