function compareAdd(hash){ // Add it to cookie
  var cookieValue = Cookies.get("compare");
  cookieValue = cookieValue.replace("%20", ",");
  if(cookieValue){
    var splitCookie = cookieValue.split(",");
  }

  if(cookieValue && splitCookie.indexOf(hash) == -1){
    cookieValue += "," + hash;
    Cookies.set("compare", cookieValue);
    return("-");
  }else if(!cookieValue){ // Create cookie
    Cookies.set("compare", hash)
    return("-");
  }else{ // Remove it
    var newCookieValue = "";
    for(var i=0;i<splitCookie.length;i++){
      if(splitCookie[i] != hash){
        newCookieValue += splitCookie[i] + ",";
      }
    }

    newCookieValue = newCookieValue.substr(newCookieValue, newCookieValue.length-1);
    Cookies.set("compare", newCookieValue);
    return("+");
  }
}
