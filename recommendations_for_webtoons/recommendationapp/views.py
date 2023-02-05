from django.shortcuts import render
import pymongo

def home(request):
    conn = pymongo.MongoClient()
    webtoon_db = conn.webtoon_db
    webtoon_collection = webtoon_db.webtoon_collection
    if request.POST:
        webtoon_title = request.POST['webtoon_title']

        similarity = webtoon_collection.find_one({'title':webtoon_title},{'_id':0,'similarity':1})['similarity']
        return render(request, "recommendationapp/base.html",{"similarity":similarity,'post':True})
    return render(request, "recommendationapp/base.html")