
function check()
{
    var btn1=document.getElementById("slot9");
    var btn2=document.getElementById("slot10");
    btn1.checked=false;
    btn2.checked=false;
}

function alertFunction()
{
    var tempslot = document.getElementsByName('slotradio');
    var row_value=0;
    for(var i = 0; i < tempslot.length; i++)
    {
        if(tempslot[i].checked)
        {
            row_value = i+1;
        }
    }
    if(row_value==0)
        alert("Please select a Time Slot!");
}

function enable()
{
var eradios = document.getElementsByName("event");
if(eradios[0].checked || eradios[1].checked)
{
    document.getElementById("fielddiv").removeAttribute("disabled");
}
  else { alert("select event");}  
}

function validate()
{

    var regemail = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

         var phoneno = /^\d{10}$/; 
      var textbox=document.getElementById("phone"); 
      if(!(textbox.value.match(phoneno)) )   
            {  
            alert("Enter valid phone number");  
            }

    var emailField = document.getElementById("email");
        if (regemail.test(emailField.value) == false) 
        {
            alert('Invalid Email Address');
        }



}

function erase()
{
    document.getElementById("clash").checked=false;
    document.getElementById("rc").checked=false;
    document.getElementById("registrationno").value="";
    document.getElementById("phone").value="";
    document.getElementById("email").value="";
    document.getElementById("pswd").value="";

}

/*function addR1()
{
    //seats=[30,20,22,19,12,2,3,4,5,6,7];
    seats = {{slot9|safe}};
    var table = document.getElementById("myTable");
    var len=seats.length;
    var i;



    while(table.rows.length > 1) 
    {
        table.deleteRow(1);
    }//Doubt//////////////////////////////////////////////////////////////////

    var time = 8;
    for(i=1;i<=len;i++)
    {
        var radioElement=document.createElement("input");
        radioElement.setAttribute("type", "radio");
        radioElement.setAttribute("value", i);
        radioElement.setAttribute("name", "radiobtn");

        var r=table.insertRow(i);
        var c1=r.insertCell(0);
        var c2=r.insertCell(1);
        var c3=r.insertCell(2);
        c1.appendChild(radioElement);
        c3.innerHTML=seats[i-1];
        
        if(i%2!=1)
        {
            c2.innerHTML= time+":00 to "+time+":30";
        }
        else
        {
            c2.innerHTML= time+":30 to "+ (time+1) +":00";
            time++;
        }
    }
}

function addR2()
{
    //seats=[1,2,3,4,5,6,7,8,9,10,11];
    seats = {{slot10|safe}};
    var table = document.getElementById("myTable");
    var len=seats.length;
    var i;
   
    while(table.rows.length > 1) 
    {
        table.deleteRow(1);
    }
    
    var time=8;
    for(i=1;i<=len;i++)
    {
        var radioElement=document.createElement("input");
        radioElement.setAttribute("type", "radio");
        radioElement.setAttribute("value", i);
        radioElement.setAttribute("name", "radiobtn");

        var r=table.insertRow(i);
        var c1=r.insertCell(0);
        var c2=r.insertCell(1);
        var c3=r.insertCell(2);
        c1.appendChild(radioElement);
        c2.setAttribute("align","center");
        c3.innerHTML=seats[i-1];

        if(i%2!=1)
        {
            c2.innerHTML= time+":00 to "+time+":30";
        }
        else
        {
            c2.innerHTML= time+":30 to "+ (time+1) +":00";
            time++;
        }
    }
}*/