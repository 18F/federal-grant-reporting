function visuallyToggle(elem) {
  // This function uses the classList API, which was introduced in HTML5.
  // Supported by ~98% of user browsers: https://caniuse.com/#feat=classlist.
  // Fallback: menu tables are displayed automatically, so browers that do not
  // support the feature will show the menu with no toggleability.
  elem.classList.toggle("visually_hidden");
}

var notificationsMenu = document.getElementById("notifications_menu");
var toggleNotifications = document.getElementById("toggle_notifications_menu_visible");
var notificationsContent = document.getElementById("notifications_content");

var participantsMenu = document.getElementById("participants_menu");
var toggleParticipants = document.getElementById("toggle_participants_menu_visible");
var participantsContent = document.getElementById("participants_content");

// Hide menus on page load
visuallyToggle(notificationsMenu);
visuallyToggle(participantsMenu);

toggleNotifications.addEventListener("click", function() {
  visuallyToggle(notificationsMenu);
  visuallyToggle(notificationsContent)
});

toggleParticipants.addEventListener("click", function() {
  visuallyToggle(participantsMenu);
  visuallyToggle(participantsContent);
});

