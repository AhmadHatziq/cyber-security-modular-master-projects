
// chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
//     let url = tabs[0].url;
//     // use `url` here inside the callback because it's asynchronous!
// });

// calls the getCurrentTabUrl() function. 
let GetURL = document.getElementById('GetURL');  
GetURL.onclick = function(element) {  
  getCurrentTabUrl();  
};  

// gets the URL of the current tab and sends it as a GET request to the Flask API
function getCurrentTabUrl() {  
  var queryInfo = {  
    active: true,  
    currentWindow: true  
  };    
  chrome.tabs.query(queryInfo, (tabs) => {  
    var tab = tabs[0];  
    var url = tab.url;
    var mal;  
    document.getElementById('url').innerHTML = url;
    fetch('http://127.0.0.1:5000/api?url=' + url).then(function(response){return response.json();}).then(data =>document.getElementById('mal').innerHTML = data).then(() => console.log(mal))
  }); 
}  
