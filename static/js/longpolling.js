function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
var updater = {
  errorSleepTime: 500,

  poll: function() {
    var args = {"_xsrf": getCookie("_xsrf")};
    $.ajax({url: "/longpolling",
           type: "POST",
           data: $.param(args),
           dataType: "text",
           success: updater.onSuccess,
           error: updater.onError
    });
  },
  onSuccess: function(data, dataStatus){
    try{
      if(parseInt(data) != 0){
        var loaditem = $('#loadunread');
        var inner = "<li id='loadunread'><a class='loadunread' href='#;'><span id='count'>" + data + "</span>条新推文</a></li>";
        var loadcount = $('#count');
        if(loadcount.length != 0){
          loadcount.html(data);
        } else if (loaditem.length == 0){
          $(inner).clone().hide().prependTo('.twitter-items').slideDown();
        }
      } else {
        var loaditem = $('#loadunread');
        if(loaditem.length != 0){
          loaditem.remove();
        }
      }
    } catch (e) {
      updater.onError();
      return;
    }
    updater.errorSleepTime = 500;
    window.setTimeout(updater.poll, 0);
  },
  onError: function(){
    updater.errorSleepTime *= 2;
    console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
    window.setTimeout(updater.poll, updater.errorSleepTime);
  }
};
updater.poll();
