function myFunction(current_element, name, target, placeholder="Custom Degree") {
  //var x = document.getElementById("mySelect").value;
  var x = current_element.value;
    console.log('yoho');
  if (x == 'Custom')
  {
    console.log('yes');
      var new_input = document.createElement("input")
      new_input.setAttribute('type', 'text');
      new_input.setAttribute('name', name);
      new_input.setAttribute('id', name);
      new_input.setAttribute('class', 'form-control')
      new_input.setAttribute('placeholder', placeholder);
     new_input.setAttribute('aria-label', 'division');
     new_input.setAttribute('autocomplete','off');
     new_input.setAttribute('style', 'margin-top:10px;')
      document.getElementById(target).appendChild(new_input);
   }
   else
   {
    console.log('no');
   input_tag = document.getElementById(name)
   if (input_tag)
   {
        input_tag.remove();
   }
   }
}

function validate(){
    var inp = document.getElementById('upload');
    var img_available = document.getElementById('img_available');

    if (img_available)
    {
    }
    else if(inp.files.length === 0){
        alert("Attachment Required");
        inp.focus();
        return false;
    }
}

/*function check_skill()
{
 var inp = document.getElementById('new_skill');
 var button = document.getElementById('add_another');

 if (!inp.value)
 {
    alert('Skill Name required');
    button.disabled = true;
    return false;
 }
}*/

function button_available(e)
{
var button = document.getElementById('add_another');
    if (e.value)
    {
        button.disabled = false;
    }
    else
    {
     button.disabled = true;
    }
}