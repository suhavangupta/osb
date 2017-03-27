$(document).ready(function(){
    $("#submitbtn").click(function(){

      var tempslot = document.getElementsByName('slotradio');
    var row_value=0;
    for(var i = 0; i < tempslot.length; i++)
    {
        if(tempslot[i].checked)
        {
            row_value = i+1;
        }
    }
    var ns= document.getElementById("myTable").rows[row_value].cells[2].innerHTML;
    if(row_value==0){
        alert("Please select a Time Slot!");
        $("#myModal").modal({show: false});
      }
    
    else 
      {
        if(ns==0)
      {
      alert("Slots unavailable!");
      $("#myModal").modal({show: false});
      }
    else    
        $("#myModal").modal({show: true});
    }
    
});
  });

$(function () { $('#myModal').on('show.bs.modal', function () {
      var tempdate = document.getElementsByName('dateslot'),date_value;
if(tempdate[0].checked){
        date_value = tempdate[0].value;
        console.log(date_value)
    }
    else        
        date_value = tempdate[1].value;
    

var tempslot = document.getElementsByName('slotradio');
var row_value;
for(var i = 0; i < tempslot.length; i++){
    if(tempslot[i].checked){
        row_value = i+1;
    }
 }
 var tb=document.getElementById("myTable");
 var slot_value = tb.rows[row_value].cells[1].innerHTML;
      var slotindex=tempslot[row_value-1].value ;
     // console.log(tempslot[i].value);
    document.getElementById("modalSlot").value=slotindex;
    document.getElementById("date_hidden").value= date_value;
    document.getElementById("modalDate").value= date_value+" September 2016";
    document.getElementById("modalSlot1").value=slot_value;

      })
   });

