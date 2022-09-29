console.log(organization);

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
  
/*
var xhr1 = new XMLHttpRequest();
// Setup our listener to process completed requests
xhr1.onreadystatechange = function () {
    // Only run if the request is complete
    if (xhr1.readyState !== 4) return;
    // Process our return data
    if (xhr1.status >= 200 && xhr1.status < 300) {
        // What to do when the request is successful
        var response = JSON.parse(xhr1.responseText);
        //var image = MEDIA  + response['resource_obj']['artworks'][1]['src'];
        //document.getElementById("testpic").setAttribute('src',image );
        console.log(response);
    } else {
        console.log('error', xhr1);
    }
};
// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
xhr1.open('GET', '/web_app/artworks/student_list', true);
xhr1.setRequestHeader('Authorization', 'Bearer ' + getCookie("access_tkn"));
xhr1.send();
*/