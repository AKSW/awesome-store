function openTab(evt, tab) {
  var i, tabs;

  tabs = document.getElementsByClassName("tabs");
  for (i = 0; i < tabs.length; i++) {
    tabs[i].className = tabs[i].className.replace(" active", "");
  }

  document.getElementById(tab).className += " active";
  evt.currentTarget.className += " active";
}