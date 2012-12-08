function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
var upnotifier = {
  errorSleepTime: 500,

  poll: function() {
    var args = {"_xsrf": getCookie("_xsrf")};
    $.ajax({url: "/notifierpolling",
           type: "POST",
           data: $.param(args),
           dataType: "text",
           success: upnotifier.onSuccess,
           error: upnotifier.onError
    });
  },
  onSuccess: function(data, dataStatus){
    try{
      if(parseInt(data) != 0){
        var content = "<div class='notifier'><a href='/notifier'>有<span class='notifier-count'>" + data + "</span>个新提醒</a></div>";
        var item = $('.notifier');
        var notifiercount = $('.notifier-count');
        var title = $('title');
        if(item.length != 0){
          notifiercount.html(data);
        } else if (item.length == 0) {
          $(content).clone().hide().prependTo('#mainbar section').slideDown();
        }
        var title_content = title.html();
        if(title_content.indexOf(')') == -1){
          title.html('(' + data + ')' + ' ' + title_content);
        } else {
          var t_c = title_content.substr(title_content.indexOf(')'), title_content.length);
          title.html('(' + data + t_c);
        }
      }
    } catch (e) {
      upnotifier.onError();
      return;
    }
    updater.errorSleepTime = 500;
    window.setTimeout(upnotifier.poll, 0);
  },
  onError: function(){
    updater.errorSleepTime *= 2;
    console.log("Notifier Poll error; sleeping for", updater.errorSleepTime, "ms");
    window.setTimeout(updater.poll, updater.errorSleepTime);
  }
};
upnotifier.poll();
