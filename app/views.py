
from json import load
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template import loader



jobTtitle=[
   "First Job",
   "Second job",
   "Third job"
] 

JobDescription=[
   "First job Description",
   "Second Job Description",
   "Third job Description"
]

# Create your views here.
# def hello(request):
#    print("Shanto")
#    return HttpResponse("<h1>Hello world</h1>") 

class Tempclass:
   x=5

def hello(request):
   # template=loader.get_template('app/hello.html')
   temp=Tempclass()
   mylist=["Alpha","Beta","Gamma"]
   is_authenticated=False
   context={"age":24,"username":"ShahSultan","tempObject":temp,"myFirstList":mylist,"is_authenticated":is_authenticated}
   # return HttpResponse(template.render(context,request))
   return render(request,"app/hello.html",context)

def job_list(request):
   list_of_job="<ul>"
   for j in jobTtitle:
      job_id=jobTtitle.index(j)
      # print(reverse('jobs-detail',args=(job_id,)))
      detailsUrl=(reverse('jobs-detail',args=(job_id,)))
      
      list_of_job+=f"<li><a href='{detailsUrl}'>{j}</a></li>"
      
   list_of_job+="</ul>"
   return HttpResponse(list_of_job)

def jobDetails(request,id):
   print(type(id))
   try:
      if id==0:
         reverseUrl=reverse("job-home")
         # print(reverseUrl)
         return redirect(reverseUrl)
      
      html_retn=f"<h1>{jobTtitle[int(id)]}</h1> <h3>{JobDescription[int(id)]}</h3>"
      return HttpResponse(html_retn)
   except:
      return HttpResponseNotFound("NOT FOUND")