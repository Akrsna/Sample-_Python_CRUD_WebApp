function required()
{
var x = document.getElementById("first_name").value;
var y = document.getElementById("last_name").value;
var z = document.getElementById("email").value;
if (x === "") || (y === "") || (z === "")
{
alert("All fields are required");
return false;
}
