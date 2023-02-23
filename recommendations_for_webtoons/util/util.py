def get_labels(df):
    return df.iloc[:,2:].values

def find_sim(img1,img2):
    style_sims = util.cos_sim(img1,img2)
    return style_sims