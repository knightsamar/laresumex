# Create your views here.
#''' will make comments which can auto-document this whole projects

'''import data models '''
from student_info.models import *;
from generate_resume.models import resume;
''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from student_info.utility import *; 
from pprint import pprint

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH

''' import process helpers '''
import subprocess 
from os import mkdir,chdir #for changing directories
from student_info.utility import our_redirect;
from time import sleep

    
def index(request):
    if 'username' not in request.session:
        print "from home to login as No session"
        return our_redirect('/ldap_login')
    # see whether user has logged in....
    # if yes, see whether the user has already filled resume, then remove the create button.
    # if no.. then remove the edit and the viw resume button.
    prn = request.session['username'] 
    s=student.objects.filter(pk=prn);
    if len(s) is 0:
        #it means there is no entry
        create_form=True;
    else:
        #Form already exists
        create_form=False
    
    t=loader.get_template('index.html')
    
    c=Context({
        'prn':request.session['username'],
        'create_form':create_form,
        'MEDIA_URL' : MEDIA_URL,
        'ROOT':ROOT
             }
        );
    return HttpResponse(t.render(c));


def latex(request,prn):
    if 'username' not in request.session:
            return our_redirect('/ldap_login/')
    '''generates the resume and puts it into the resume store for version control'''
    #the current user from session;
    if prn != request.session['username']:
        return HttpResponse('Please mind your own resume..')
    if prn is not None:
    	try:
	        s = student.objects.get(pk=prn)
        except Exception as e:
            output = "<h3>Student details for PRN %s not found! Can't generate a LaTeX file!</h3>" % (prn);
            return HttpResponse(output);
        
        if s is not None:
            #pass the student object with all his entered info to the template generator
            t = loader.get_template('%s/template.tex' % RESUME_FORMAT);
            
            pprint(tables);
            student_data = dict();
            pprint(tables.items());

            #get all related objects
            for tbl,v in tables.iteritems():
                print 'Getting for %s and %s' % (tbl,v)
                print "=========>>", v  ,"<<======="
                student_data[tbl]=eval(v).objects.filter(primary_table=s)

            #add the basic info wala original object also
            student_data['s'] = s;
            student_data['p'] = student_data['p'][0]; #because we hv only one personal info row.
            student_data['sw']=student_data['sw'][0]
            #do we have the photo ? if yes, then include it.
            student_data['photo'] = RESUME_STORE + "photos/" + prn + ".png"  
            #else, store None
            student_data['ROOT'] = ROOT

            pprint(student_data);
            c = Context(student_data);
             
            try:
                #every latex file goes into that prn's directory
                destination_dir = '%s/%s/' % (RESUME_STORE, prn)

                try:
                    chdir(destination_dir) #if we can't change into it, create it!
                except OSError:
                    mkdir(destination_dir);
                finally:
                    chdir(FULL_PATH);
                 
                resume_file = '%s/%s.tex' % (destination_dir, prn)
                #now store the person's generated resume-latex-code
                f = file(resume_file,'w'); #if the file exists, overwrite it ELSE  create it.
               
                f.write(t.render(c));
                f.close();
              
                """#for now postponed to next release
                #now add this file to version control

                hg_command = "hg add %s; hg commit -u laresumex -m 'updated by %s' " % (resume_file,user);
                return_status = get_done(hg_command);
                """
                return_status = True;
            except Exception as e:
               print 'Exception was ', e;
               return_status = False;
            finally:
                if return_status is False:
                    output = "<h3>Couldn't generate your .TEX file! Return code was %d </h3>" % return_status;
                else:
                    output = "<h3>Done!</h3>";
        else:
            output = "<h3>Student details for PRN %s not found!</h3>" % (prn);
    else:
       output = "<h3>Hey, pass me a PRN man!</h3>";
    
    return HttpResponse(output);


def pdf(request,prn):
    if 'username' not in request.session:
            return out_redirect('/ldap_login/')
    if prn != request.session['username']:
        return HttpResponse('Nor ur resume')
    if prn is not None:
        try:
           s = student.objects.get(pk=prn);
        except:
           output = "<h3>Student details for PRN %s not found! Can't generate a PDF!</h3>" % (prn);
           return HttpResponse(output);

        #compare generate_resume.models.resume.last_tex_generated with student_info.models.student_last_updated and decide!
        #is it fresher ?
            #oh no! it isn't. generate it again!
        
        #ok, it is no need to regenerate
            #call the generate_latex function with the prn

        #if no record of this prn exists anywhere, tell the idiot!
    
    #generate it's pdf
        pdf_file = "/tmp/%s.pdf" % (prn);
        return_status = False;
        #find the tex file
        try:
          #generate the pdf 
          pdf_generation_command = "pdflatex --interaction=nonstopmode -etex -output-directory=/tmp %s/%s/%s.tex" % (RESUME_STORE,prn,prn);
          for i in range(0,3): #run the pdflatex command min 2 and max 3 times -- Manjusha Mam, Bhaskaracharya Pratishthana
              return_status = get_done(pdf_generation_command)
                
          print "Return status is ",return_status;
          pdffile = "/tmp/%s.pdf" % prn;
          resume_pdf = open(pdffile);
          #prepare the file to be sent
          response = HttpResponse(resume_pdf.read(), mimetype="application/pdf");
          resume_pdf.close();
          #name the file properly
          response['Content-Disposition'] = "attachment; filename=SICSR_%s_resume.pdf" % s.fullname;
        
        except Exception as e:
          response = HttpResponse("Some problem!");
          print 'Exception was ', e;
    ################because pdflatex can return 1 or 0 and still generate the file
#          if return_status is not 0:
#             output = "<h3>Couldn't generate your .PDF file! Return code was %s </h3>" % return_status;
#          else:
#             output = "<h3>Done!</h3>";
    else:
       output = "<h3>Hey, pass me a PRN man!</h3>";
    
    return response;

def html(request,prn):
    if 'username' not in request.session:
           return our_redirect('/ldap_login')
    if prn != request.session['username']:
          return HttpResponse('Not urs..!!')
    if prn is not None:
        try:
           s = student.objects.get(pk=prn);
        except:
           output = "<h3>Student details for PRN %s not found! Can't give you HTML</h3>" % (prn);
           return HttpResponse(output);

    #is the html file current and updated?
    html_file = 'STORE/%s/%s.html' % (prn, prn);

    #if yes, just show it 

    #otherwise generate again and show it

    try:
        cmd = "yes Q | htlatex %s.tex" % (prn);
        done = get_done(cmd,"%s/%s/" % (RESUME_STORE,prn));
    
        return our_redirect('%s/%s' % (MEDIA_URL, html_file));
    except Exception as e:
        #tell them can't do it.
        return HttpResponse("Boss! Can't generate HTML for resume of %s because we got %s" % (prn,e));
        
def get_done(cmd,path=RESUME_STORE):
    '''handles all panga of executing a command on linux shell'''
    #where do we want to execute this ?
    print "changing path to %s", path
    chdir(path);

    print "Got total --> ", cmd
    cmds = cmd.split(';'); #split multiple commands
    print 'total ',len(cmds);
    for c in cmds:
        try:
           #cmd_with_arguments=c.split();
           print 'Executing ',c

           #connect the pipes in the processes and make the stdin and stdout flow through them properly
           #because Popen doesn't handle pipes properly itself

           sleep(3);
           r = subprocess.Popen(c,shell=True,stdout=None);
           if r is not 0:
               chdir(FULL_PATH); #so that no stupid problem are caused
               return False;    #no need of executing further commands
        except Exception as e:
          print 'Exception was ', e
          chdir(FULL_PATH);
          return False;

    return True;

