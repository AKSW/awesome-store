function openTab(evt, tab) {
  var i, tabs, projectDetail;

  projectDetail = document.getElementById("ProjectDetail")
  //projectDetail.style.backgroundColor = (tab === "Info")? "cornflowerblue" : "darkseagreen"

  tabs = document.getElementsByClassName("tabs");
  for (i = 0; i < tabs.length; i++) {
    tabs[i].className = tabs[i].className.replace(" active", "");
  }

  document.getElementById(tab).className += " active";
  evt.currentTarget.className += " active";
}