# Create your views here.
#''' will make comments which can auto-document this whole projects

'''import data models '''
from student_info.models import student;
from generate_resume.models import resume;
''' import generator helpers '''
from django.template import Context, loader, RequestContext
from django.http import HttpResponse;
from django.shortcuts import render_to_response;

''' import vars '''
from laresumex.settings import RESUME_STORE,RESUME_FORMAT

''' import process helpers '''
from subprocess import call #avail from python 2.6

def index(request):
    # see whether user has logged in....
    # if yes, see whether the user has already filled resume, then remove the create button.
    # if no.. then remove the edit and the viw resume button.
    '''
    s=student.objects.filter(pk=prn);
    if len(s) is 0:
        it means there is no entry
        create_form=True;
    else:
        Form already exists
        create_form=False
    c=Context({'create_form':create_form})
    '''
    t=loader.get_template('index.html')
    c=Context();
    return HttpResponse(t.render(c));


def latex(request,prn):
    '''generates the resume and puts it into the resume store for version control'''
    user = '10030142056' #the current user from session;
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
                response = HttpResponse("Some problem!");
            finally:
                if return_status is False:
                    output = "<h3>Couldn't generate your .TEX file! Return code was %d </h3>" % return_status;
                else:
                    output = "<h3>Done!</h3>";
        else:
            output = "<h3>Student details for PRN %s not found!</h3>" % (prn);
    else:
       output = "<h3>Hey, pass me a PRN man!</h3>";
   
    return response;


def pdf(request,prn):
    if prn is not None:
        s = student.objects.get(pk=prn);
        if s is None:
            output = "<h3>Student details for PRN %s not found!</h3>" % (prn);
            response = HttpResponse(output);
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
          pdf_generation_command = "pdflatex --interaction=nonstopmode -etex -output-directory=/tmp %s%s.tex" % (RESUME_STORE,prn);
          print str(pdf_generation_command).split();
          return_status = call(pdf_generation_command.split())
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


def get_done(cmd):
    '''handles all panga of executing a command on linux shell'''
    print "Got total --> ", cmd
    cmds = cmd.split(';'); #split multiple commands
    for c in cmds:
        try:
           cmd_with_arguments=c.split();
           print 'Executing ',cmd_with_arguments
           r = call(cmd_with_arguments);
           if r is not 0:
               return False;    #no need of executing further commands
        except Exception as e:
          print 'Exception was ', e
          return False;

    return True;

