

function validate()
{
  var name=document.getElementById("name");

  if (name.value == null || name.value =="")
  {
    alert("Enter Name");
    return false;
    }

var cno=document.getElementById("cno");
  
  if (cno.value == null || cno.value =="")
  {
    alert("Enter Card Number");
    return false;
    }


/*Amex, mastercard, discover, visa */
  var cardno = /^(?:(3[47][0-9]{13})|(5[1-5][0-9]{14})|(6(?:011|5[0-9]{2})[0-9]{12})|(4[0-9]{12}(?:[0-9]{3})?))$/;
  while(!(cno.value.match(cardno)))
       
        {
        alert("Not a credit card number!");
        return false;
        }


var form = document.getElementById('form');
var expm = document.getElementById('expm');
var expy = document.getElementById('expy');

form.addEventListener('submit',ev => 
{
  ev.preventDefault();
  
  var month = expm.value;
  var year = expy.value;
  
  // Create a date object from month and year, on the first
  // of that month.
  var expiryDate = new Date(year + '-' + month + '-30');
  
  // You can compare date objects, this says if the expiryDate is
  // less than todays date, 
  if (expiryDate < new Date()) 
    // Fails validation, show some error message to user
     {
        alert("Card Expired");
        return false;
        }
}
)
    
    var cvv=document.getElementById("cvv");
  

  if (cvv.value == null || cvv.value == "" )
  {
    alert(" Please Enter CVV code from the back of your card");
    return false;
    }

  var cvvno = /^(?:[0-9]{3})$/;
  while(!(cvv.value.match(cvvno)))
        
        {
        alert(" Invalid CVV !");
        return false;
        }
	


}