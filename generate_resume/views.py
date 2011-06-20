# Create your views here.
#''' will make comments which can auto-document this whole projects

'''import data models '''
from student_info.models import student;
from generate_resume.models import resume; 

''' import generator helpers '''
from django.template import Context, loader
from django.http import HttpResponse;
from django.shortcuts import render_to_response;

''' import vars '''
from laresumex.settings import RESUME_STORE,RESUME_FORMAT

''' import process helpers '''
from subprocess import call #avail from python 2.6

def latex(request,prn):
    '''generates the resume and puts it into the resume store for version control'''
    user = 'laresumex' #the current user from session;
    if prn is not None:
        s = student.objects.get(pk=prn);
        if s is not None:
            #pass the student object with all his entered info to the template generator
            t = loader.get_template('%s/template.tex' % RESUME_FORMAT);
            c = Context({ 's' : s });
            
            resume_file = '%s%s.tex' % (RESUME_STORE,prn);

            #now store the person's generated resumecode
            f = file(resume_file,'w'); #if the file exists, overwrite it ELSE  create it.
            f.write(t.render(c));
            f.close();
            
            #now add this file to version control
            try:
                hg_command = "cd %s; hg add %s; hg commit -u laresumex -m 'updated by %s' " % (RESUME_STORE,resume_file,user);
                return_status = get_done(hg_command);
            except Exception as e:
                print 'Exception was ', e;
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
    if prn is not None:
        #compare generate_resume.models.resume.last_tex_generated with student_info.models.student_last_updated and decide!
        #is it fresher ?
            #oh no! it isn't. generate it again!
        
        #ok, it is no need to regenerate
            #call the generate_latex function with the prn

        #if no record of this prn exists anywhere, tell the idiot!
    
    #generate it's pdf
        pdf_file = "/tmp/%s.pdf" % (prn);
        #find the tex file
        try:
          #generate the pdf 
          pdf_generation_command = "cd %s; pdflatex -output-directory=/tmp %s.tex" % (RESUME_STORE,prn);
          return_status = get_done(pdf_generation_command)
        except Exception as e:
          print 'Exception was ', e;
        finally:
          if return_status is not 0:
             output = "<h3>Couldn't generate your .PDF file! Return code was %s </h3>" % return_status;
          else:
             output = "<h3>Done!</h3>";
    else:
       output = "<h3>Hey, pass me a PRN man!</h3>";

    return HttpResponse(output);

def get_done(cmd):
    '''handles all panga of executing a command on linux shell'''
    print "Got total --> ", cmd
    cmds = cmd.split(';'); #split multiple commands
    for c in cmds:
        try:
           print 'Executing ',c
           r = call(c);
           if r is not 0:
               return False;    #no need of executing further commands
        except Exception as e:
          print 'Exception was ', e
          return False;

    return True;

