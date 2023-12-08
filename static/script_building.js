function getBuildingName() {
    // Get the selected text from localStorage
    let selectedText = localStorage.getItem('selectedBuildingText');
  
    // Display the selected text
    document.getElementById('selectedBuildingText').textContent = selectedText;
  }

document.getElementById('button_room').addEventListener('click', function () {
    // Get the select element
    let selectElement = document.getElementById('select_room');
  
    // Get the selected option's value
    let selectedValue = selectElement.options[selectElement.selectedIndex].value;
    let selectedText = selectElement.options[selectElement.selectedIndex].textContent;
  
    // Save to localStorage
    localStorage.setItem('selectedRoomValue', selectedValue);
    localStorage.setItem('selectedRoomText', selectedText);
  
    console.log('Selected room: ' + selectedValue);
    console.log('Selected text: ' + selectedText);
  
    // Redirect to the other page
    // location.href = "overview.html";
  });
