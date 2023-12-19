document.getElementById('button_building').addEventListener('click', function () {

  document.querySelector('.loading-container').style.display = 'block';

  // Get the select element
  let selectElement = document.getElementById('select_building');

  // Get the selected option's value
  let selectedValue = selectElement.options[selectElement.selectedIndex].value;
  let selectedText = selectElement.options[selectElement.selectedIndex].textContent;

  // Save to localStorage
  localStorage.setItem('selectedBuildingValue', selectedValue);
  localStorage.setItem('selectedBuildingText', selectedText);

  // console.log('Selected building: ' + selectedValue);
  // console.log('Selected text: ' + selectedText);

  // Redirect to the other page
  // window.location.href = "templates/building.html";
});