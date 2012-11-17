var updater = {
  poll: function() {
    args = {"hello": "word"}
    args._xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
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
          $('.items').prepend(inner);
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
    interval = window.setTimeout(updater.poll, 0);
  },
  onError: function(){
    console.log("Poll error;");
  }
};
updater.poll();
