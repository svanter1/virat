
// A FUNCTION FOR VALIDATING THE CREDIT CARD NUMBER
function cardNO(inputtxt)
{
	//FOR THIS INSTANCE WE ARE TAKING CARD NUMBER STARTING WITH 34 OR 37 AND HAVING 13 DIGITS
  var cardno = /^(?:3[47][0-9]{13})$/;
  if(inputtxt.value.match(cardno))
        {
      return true;
        }
      else
        {
        alert("Not a credit card number!");
        return false;
        }
}
