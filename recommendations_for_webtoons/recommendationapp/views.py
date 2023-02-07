from django.shortcuts import render
# import pymongo


def testpage(request):
    dict = {"data_set_1" : [1,2,3,4,5],
            'data_set_2' : "STRING",
            'data_set_3' : 12345}
    
    return render(request, "./testpage/sample.html", dict) # app 내의 templete 폴더 참조


def home(request):
    # conn = pymongo.MongoClient("mongodb://172.30.1.15:27017/?authMechanism=DEFAULT&authSource=webtoon_db")
    # webtoon_db = conn.webtoon_db
    # webtoon_collection = webtoon_db.webtoon_collection
    # if request.POST:
    #     webtoon_title = request.POST['webtoon_title']
    #
    #     similarity = webtoon_collection.find_one({'title':webtoon_title},{'_id':0,'similarity':1})['similarity']
    #     return render(request, "recommendationapp/base.html",{"similarity":similarity,'post':True})
    return render(request, "recommendationapp/base.html")



