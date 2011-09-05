      
    /* Autofills the passed dropdown objet with contents based on it's value 
      
       For day, month and year, fills with values.
       For courses, fills with degrees.
    */
function validation(o,what)
{
    if (what == 'string')
    {
        isNAN(o.value)

    }
}

function fillOptions(o)
    {
        if (o.children.length>1) return false;
        //o=document.getElementById('month');
        if (o.name == 'month')
        {
            var months=new Array('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec');
          
            for (var i =0;i<12;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=months[i];
                 o.add(option,null)

            }
        }
        else if(o.name == 'date')
        {
             for (var i =1;i<=31;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=i;
                 o.add(option,null)

            }
        }
        else if(o.name == 'year')
            {
                if((o.prevElementSibling)&&(o.previousElementSibling.value=="")) o.previousElementSibling.focus()
                var d= new Date();

                if(o.id.split('_')[0] == 'birthdate')
                    { var i=d.getFullYear()-60; var j=(d.getFullYear()-18);} // need to be min 18 yrs old..!!
                else
                    {var i=d.getFullYear()-18; j=d.getFullYear()+2;}
                for (;i<=j;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=i;
                 o.add(option,null)

            }
           } 
        else  if (o.name == 'course-g')
        {
          var course=new Array('BCA','BCS','BSc','BE','B.Tech', 'BBA','B.Com');
            for (var i =0;i<course.length;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=course[i];
                 o.add(option,null)
            }
        } 
          else  if (o.name == 'course-pg')
        {
          var course=new Array('MSc(CA) SEM I','MSc(CA) SEM II','MSc(CA) SEM III','MSc(CA) SEM IV','MBA(IT) SEM I','MBA(IT) SEM II','MBA(IT) SEM III','MBA(IT) SEM IV');
            for (var i =0;i<course.length;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=course[i];
                 o.add(option,null)
            }
        } 
        else if (o.name == "strongAreas" || o.name == "weakAreas" )
        {
            var h=new Array('programming','database','os','web','packages');
            for( var i=0;i<h.length;i++)
            {
                c=document.getElementById(h[i]).children; //LI's
                
                for(var j=0;j<c.length;j++)
                {
                    if(c[j].children[0].value)
                    {
                        var option = document.createElement("option");
                        option.text=c[j].children[0].value
                        o.add(option,null)
                    }
               }
                
            }
        }
    }
     
    

 /* changes the sibling fields to suit the current value of the passed object.
    
    For Months, changes the Day according to the capacity of the month.
    For the Appearing/Result Awaiting, disables the marks field.
   
    TODO: for leap year, it should make February right.
 */
function change(o)
 {
     id0=o.id.split('_')[0];
     id1=o.id.split('_')[1];
     prev=o.previousElementSibling;
     if (id0 == 'marks')
     {
      if (o.value == 'Appearing' || o.value =='Result Awaiting')
      { 
         prev.value=o.value;
         prev.disabled=true;
         o.nextElementSibling.value=o.value;
         o.nextElementSibling.disabled=true;

         
       // o.parentNode.removeChild(o.previousElementSibling);
      }
      else
       {
         prev.disabled=false;
         prev.value="";
         prev.focus();
         o.nextElementSibling.disabled=false;
       }
     }
     else if (id1 =='month')
     {
         if (prev.value=="")
             prev.focus();
         if (o.value =='Feb')
             if((prev.value=='30')||(prev.value=='31'))
             {
                 prev.value='28';
                 prev.focus();
             }
          if((o.value == 'April')||(o.value =='June')||(o.value =='Sept')||(o.value =='Nov'))
              if(prev.value=='31')
              {
                  prev.value='30';
                  prev.focus();
              }
     }
      else if (id1 =='date')
     {
         
         if (o.nextElementSibling.value =='Feb')
             if((o.value=='30')||(o.value=='31'))
             {
                o.value='28';
                o.focus();
             }
          if((o.nextElementSibling.value == 'April')||(o.nextElementSibling.value =='June')||(o.nextElementSibling.value =='Sept')||(o.nextElementSibling.value =='Nov'))
              if(o.value=='31')
              {
                  o.value='30';

                  o.focus();
              }
     }
 }

 function concat(o)
 {
  var months=new Array('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec');
  var compulsory=new Array('personal','fullnam');
  id=o.id.split('_');
  hidden=document.createElement('input')
  hidden.type="hidden";
  if (id[1].indexOf("year")==0)
      id[1]="monthyear"
  else
      id[1]=id[1].substr(0,id[1].indexOf("year"))+"monthyear";
  
  hidden.name=id.join("_");
  hidden.id=hidden.name;

  H=document.getElementById(hidden.name);
  if ((o.previousElementSibling) && (o.previousElementSibling.id.indexOf('month') != -1))
      {
            var previousElementSiblingMonthKiValue=o.previousElementSibling.value
        if ((o.previousElementSibling.previousElementSibling) && (o.previousElementSibling.previousElementSibling.id.indexOf('date') != -1))
          var previousElementSiblingDateKiValue=o.previousElementSibling.previousElementSibling.value
        else 
             previousElementSiblingDateKiValue="01"

      }
  else 
  { 
      var previousElementSiblingMonthKiValue="Jan"
      var previousElementSiblingDateKiValue="01"
  }
 
  newDate= previousElementSiblingDateKiValue+","+(months.indexOf(previousElementSiblingMonthKiValue)+1) + "," + o.value
  hidden.value=newDate;
  if (H)
      H.value=hidden.value
  else    
      o.parentNode.appendChild(hidden);

 }


/* check whether mandatory values are filled or not */
function mandatoryCheck()
{ 
    //clientside mandatoriness checking
    var compulsory = new Array('personal', 'fullname','birthdate','sex','career','marks','companySpecific')
    input=document.getElementsByTagName('input');
    for (var i=0;i<input.length;i++)
    {
        
        if(input[i].id!="")
        {   
                input[i].name=input[i].id;
        }
        a=input[i].name.split('_')[0]
        if ((input[i].value=="")&&(compulsory.indexOf(a)>=0)&&(input[i].disabled==false) )
            {

                input[i].focus();
                //TODO: find out a way to retrieve the parent tab of the element and call it's select() method 
                alertmsg=input[i].name.split('_')
                alert( alertmsg[1] + ' in the ' + alertmsg[0] + '  section is not filled');
                return false;
            }
    }  
    var tables = new Array('marks','workex','certification','projects','academic','extracurricular')
    
    
    //dependency checking -- if content is filled and the month-year isn't OR if month-year is filled and content isn't.
    select=document.getElementsByTagName('select');
    for (var i=0;i<select.length;i++)
    {
        a=select[i].id.split('_')[0]
        if (tables.indexOf(a)>=0)
        {
            o=select[i].parentNode.parentNode.children;
            if (select[i].value)
               var filled=true;
            else
                var filled = false;
        
            for(var j=0;j<o.length;j++)
            {
                
                for (var k=0;k<o[j].children.length;k++)
                {
                    
                    if ((o[j].children[k].tagName=="INPUT" || o[j].children[k].tagName=="SELECT" || o[j].children[k].tagName=="TEXTAREA") && ((filled && !o[j].children[k].value)|| (!filled && o[j].children[k].value)))
                    {
                        alertmsg=o[j].children[k].id.split('_');
                        alert('Check your '+ alertmsg[0] +'  entry...' + alertmsg[1] +' is not filled properly'); return false;}

                }

            } 
        }
    }
    alert('returning true')
 return true;
}
/* replaces all name attributes of all input, select and textarea elements with their ids so that they can be successfull when the form is submitted. */
function changeName()
{
    //check mandatoriness!
    if (!mandatoryCheck())
    {
        return false;
    }
    select=document.getElementsByTagName('select');
    for (var i=0;i<select.length;i++)
    {
        //for all    eleemtns who are named 'month' OR 'year'
       if (select[i].id.indexOf('date') >= 0 || select[i].id.indexOf('year') >= 0 || select[i].id.indexOf('month') >= 0)
       {
           if (select[i].id.indexOf('year')>=0)
           {
               concat(select[i])
           }
         //thee shall deem them unsuccessfull
         select[i].name=null;
         continue;
       }
       select[i].name=select[i].id;
       
       if (select[i].value=="")
            {select[i].focus();return false;}
    }
    textarea=document.getElementsByTagName('textarea');
    for (var i=0;i<textarea.length;i++)
        //if(tablearea[i].value=="")
            textarea[i].name=textarea[i].id;
    //now tell in the form submission the secret
    document.getElementById('allok').value = 1;
    return true;
}

function remove(o)
{
    // IF extra fields can be entered as blank, then students have write to remove all their pre-wriiten fields
    if (o.tagName=='TD')
    {
        p=o.parentNode;
        if(p.parentNode.childElementCount == 2)
            return false
        p.parentNode.removeChild(p)
    }
    else
    {
        if (o.parentNode.childElementCount == 1)
        {
            alert('one element is required')
            return false
        }
        o.parentNode.removeChild(o)
    }    
}    
       
   
