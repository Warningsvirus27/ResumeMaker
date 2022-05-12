function myFunction(current_element, name, target, placeholder="Custom Degree") {
  //var x = document.getElementById("mySelect").value;
  var x = current_element.value;

  if (x == 'Custom')
  {

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

   input_tag = document.getElementById(name)
   if (input_tag)
   {
        input_tag.remove();
   }
   }
}