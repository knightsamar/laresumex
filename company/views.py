# Create your views here

''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response, redirect;

''' import vars '''
from laresumex.settings import RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH

def search(request):
    c=RequestContext(request,{})
    t=loader.get_template('company/search.html')
    return HttpResponse(t.render(c))
def getResume(request):
    print str(request.POST)
    print "====Now we'l process the post fields..==="
    final_string=""
    for k,v in request.POST.iteritems():
        if k == 'csrfmiddlewaretoken':
            continue
        s=k.split('_')
        #print "==Table name..", s[0],
        #print "Field name ...",s[1]
        if s[2] == "count":
            final_string+="select primary_table from "+ s[0] +" where "+s[1]+" < "+v+"\n";
        else:
            final_string+="select primary_table from "+s[0]+" where "+s[1]+" like %"+v+"% \n";

    print final_string
    return HttpResponse("Please wait till i fetch the resumes...\n\n"+final_string);
