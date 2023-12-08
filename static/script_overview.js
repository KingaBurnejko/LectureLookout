function getBuildingRoomName() {
  // Get the selected text from localStorage
  let selectedBuilding = localStorage.getItem("selectedBuildingText");
  let selectedRoom = localStorage.getItem("selectedRoomText");

  // Display the selected text
  document.getElementById("selectedBuildingText").textContent =
    selectedBuilding;
  document.getElementById("selectedRoomText").textContent = selectedRoom;
}

function loadTimetable(event) {

  var date = document.getElementById('comp_select').value;

  fetch('/overview_timetable', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({date: date}),
  });


  // console.log(event.target.id);
  // fetch("/overview_timetable", {
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   body: JSON.stringify({
  //     building: localStorage.getItem("selectedBuildingText"),
  //     room: localStorage.getItem("selectedRoomText"),
  //   }),
  //   method: "POST",
  // })
  //   .then((response) => response.json())
  //   .then((text) => {
  //     console.log(text);
  //   });
}

document.getElementById("button_overview").addEventListener("click", loadTimetable);
