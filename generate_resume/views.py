# Create your views here.
#''' will make comments which can auto-document this whole projects

'''import data models '''
from student_info.models import *;
from generate_resume.models import resume;
''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from company.views import fetch_index;
from student_info.utility import *; 
from student_info import tables
from pprint import pprint

''' import vars '''
from laresumex.settings import ROOT,RESUME_STORE,RESUME_FORMAT,MEDIA_URL,FULL_PATH
from datetime import datetime

''' import process helpers '''
import subprocess 
from os import mkdir,chdir,path #for changing directories
from student_info.utility import our_redirect;
from time import sleep


def latex(request,prn):
    if 'username' not in request.session:
            return our_redirect('/ldap_login/')
    '''generates the resume and puts it into the resume store for version control'''
    #the current user from session;
    if prn != request.session['username']:
        return HttpResponse('Please mind your own resume...')
    if prn is not None:
    	try:
            s = student.objects.get(pk=str(prn))
            print "=============== inside Latex.. found S .....",s
        except Exception as e:
            print "======inside latex... exception",e
            output = "<h3>Student details for PRN %s not found! Can't generate a LaTeX file!</h3>" % (prn);
            return HttpResponse(output);
        
        if s is not None:
            print "==latex====s is not NOne"
            #pass the student object with all his entered info to the template generator
            t = loader.get_template('%s/template.tex' % RESUME_FORMAT);
            
            print "=====latex ===t ",t

            #add the basic info wala original object also
            student_data=tables.get_tables(s)
            #student_data['photo'] = RESUME_STORE + "photos/" + prn + ".png"  
            student_data['photo'] = "%s.png" % (prn);

            pprint(student_data);
            c = Context(student_data);
             
            try:
                print " =latex==== inside the try"
                #every latex file goes into that prn's directory
                destination_dir = '%s/%s/' % (RESUME_STORE, prn)

                try:
                    chdir(destination_dir) #if we can't change into it, create it!
                except OSError:
                    print "===latex === Os Error aya tha.. making dIr"
                    mkdir(destination_dir);
                finally:
                    print "=== inside chdir ka finally"
                    chdir(FULL_PATH);
                 
                resume_file = '%s/%s.tex' % (destination_dir, prn)
                #now store the person's generated resume-latex-code
                f = file(resume_file,'w'); #if the file exists, overwrite it ELSE  create it.
               
                f.write(t.render(c));
                f.close();
                
                #now update the .tex generation timestamp
                print "Updating the resume details timestamp with what has been done";
                print s;
                print "Now is ", datetime.now();
                r = resume.objects.get_or_create(prn=s);

                print "====latex======== resume made  ",r
                #because we called get_or_create, we will get a tuple containing the record and a bool value telling whether it was created or fetched
                r[0].last_tex_generated = datetime.now();
                print r[0].last_tex_generated
                r[0].save();

                """#for now postponed to next release
                #now add this file to version control

                hg_command = "hg add %s; hg commit -u laresumex -m 'updated by %s' " % (resume_file,user);
                return_status = get_done(hg_command);
                """
                return_status = True;
            except Exception as e:
               print '=====latex============ Exception was ', e;
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
            return our_redirect('/ldap_login/')
    if prn != request.session['username']:
        return HttpResponse('Not your resume!')
    if prn is not None:
        try:
           s = student.objects.get(pk=str(prn));
           print "We have got a student ",s
           try:
              r = resume.objects.get(prn=s);
           except Exception as e:
              #no resume was ever created for this user, hence we need to generate atleast latex once.
              print "====pdf==== Resume record doesn't exist...calling latex()";
              latex(request,prn);
           finally:
              r = resume.objects.get(prn=s);
              print "======pdf======= Ok, now we have ",r
        except Exception as e:
           output = "<h3>Student details for PRN %s not found! Can't generate a PDF!</h3>" % (prn);
           print "=======pdf ========", e;
           return HttpResponse(output);
        
        print "Last TEX generated ", r.last_tex_generated;
        print "Last PDF generated ", r.last_pdf_generated;
        #compare generate_resume.models.resume.last_tex_generated with student_info.models.student_last_updated and decide!
        tex_file = "%s/%s/%s.tex" % (RESUME_STORE,prn,prn);
        #do we have a fresher .TEX file compared to the infromation filled by the student ?
        if (r.last_tex_generated is not None) and (r.last_tex_generated < s.last_update) or (not(path.exists(tex_file))):
            #oh no! it isn't fresher! generate it again!
            print "we have got a stale .TEX file! regenerating it by calling latex"
            latex(request,prn);
        else:
            #ok, there is no need to regenerate latex
            pass; 
        
        #Now...is the pdf file fresher ?
        pdf_file = "%s/%s/%s.pdf" % (RESUME_STORE, prn, prn);
        if (r.last_pdf_generated is not None) and (r.last_pdf_generated > r.last_tex_generated) and (path.exists(pdf_file)):
            #the pdf file is fresher, so we don't need to regenerate it! let's just give it back.       
            print "PDF file for %s is already fresher, so giving it back directly!" % (r.prn);
        else:
            print "PDF file is stale!";
            #the pdf file is stale, get a fresh copy!
            #generate it's pdf
            pdf_file = "/tmp/%s.pdf" % (prn);
            return_status = False;
            #find the tex file
            try:
              #generate the pdf 
              copy_photo_command = "cp -v %s/photos/%s.* %s/%s/" % (RESUME_STORE,prn,RESUME_STORE,prn);
              get_done(copy_photo_command);
              pdf_generation_command = "pdflatex --interaction=nonstopmode -etex -output-directory=/tmp %s/%s/%s.tex" % (RESUME_STORE,prn,prn);
              for i in range(0,3): #run the pdflatex command min 2 and max 3 times -- Manjusha Mam, Bhaskaracharya Pratishthana
                   print "===========>PASS %d<===========" % (i);
                   return_status = get_done(pdf_generation_command)
                
              #print "Return status is ",return_status; #doesn't matter now...after get done.
              pdf_file = "/tmp/%s.pdf" % prn;
              copy_pdf_command = "cp -v /tmp/%s.pdf %s/%s/" % (prn, RESUME_STORE,prn); #copy the .pdf to the user's directory in STORE so that we can reuse it
              get_done(copy_pdf_command);
              print "Updating timestamp for the PDF generation in our records"
              r.last_pdf_generated = datetime.now();
              r.save();
            except Exception as e:
              response = HttpResponse("Some problem!");
              print 'Exception was ', e;
         
        #open the generated pdf file
        resume_pdf = open(pdf_file);
        #prepare the file to be sent
        response = HttpResponse(resume_pdf.read(), mimetype="application/pdf");
        resume_pdf.close();
        #name the file properly
        response['Content-Disposition'] = "attachment; filename=SICSR_%s_resume.pdf" % s.fullname;
    else:
        output = "<h3>Hey, pass me a PRN man!</h3>";
        response = HttpResponse(output);

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
           output = "<h3>Student details for PRN %s not found! <input type = 'button' value='Click to fill your details' onClick='%s/form'></h3>" % (prn,ROOT);
           return HttpResponse(output);

    data = tables.get_tables(s);
    t=loader.get_template('moderncv/htmlview.html')
    c=Context(data)
    return HttpResponse(t.render(c))
           
    
'''
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
        
'''
