function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r?r[1]:undefined;
}
$(function(){
  $('.mention').live('mouseover', function(e){
    $('#floater').remove();
    var top = (e.pageY + 2) + "px";
    var left = (e.pageX + 2) + "px";
    var username = $(this).html();
    $.get(
      '/user/profile/' + username,
      function(data){
        data = eval("(" + data + ")");
        if (parseInt(data.f) == 1){
            var v = "<a class='btn mini-btn' href='/user/"+ data.username +"/unfollow'>已关注</a>";
        } else {
            var v = "<a class='btn mini-btn unfo' href='/user/"+ data.username +"/follow'>关注</a>";
        }
        var floater = "<div class='mention' id='floater'><a href='#;'><img class='avatar' src='" + data.avatar + "'></a><div class='floater-content'><div class='name'><strong>"+ data.username +"</strong></div></div><div class='profile-action'>"+ v +"</div></div>";
        $('body').append(floater);
        $('#floater').css({
          "padding": "6px 10px",
          "position":"absolute",
          "background-color":"#FFFFA5",
          "box-shadow":"0px 0px 10px rgba(0,0,0,0.8)",
          "min-width":"160px",
          "top":top,
          "left":left
        }).show("fast");
      }
    )
  });

  $('.item').live('hover',
    function(){
      $(this).find('.info .action ul').toggle();
    }
  );
  $('.reply').live('click',
    function(){
      $(this).parents('.item').find('.comment-wrap').toggle();
    }
  );
  $('.twitter-action .btn').live('click',function(){
    $(this).val('正在发布...');
    var content = $(this).parents('form').children('textarea').val();
    var args = {"content": content};
    args._xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
    $.post("/post/add", $.param(args), function(data){
        data = eval("(" + data + ")");
        var precontent = '<div class="item"><a href="/user/'+ data.username + '"><img class="avatar" src="' + data.avatar +'"></a><div class="twitter-content"><div class="name"><a href="/user/' + data.username + '"><strong>' + data.username + '</strong></a></div><div class="content">' + data.content + '</div><div class="info"><small>' + data.time + '</small><div class="action"><ul style="display: none;"><li><a class="reply" href="#;">reply</a></li><li><a class="retweet" href="#;">retweet</a></li><li><a class="fav" href="#;">fav</a></li></ul></div></div></div><div class="comment-wrap"><div class="twitter-comment-textbox"><form method="post" action="/post/' + data.id + '/comment/add"><input id="comment-editor type="text" name="comment-content" size="35"><input class="btn mini-btn" type="submit" value="发布"><input type="hidden" name="_xsrf" value="' + args._xsrf + '"></form></div><div class="twitter-comments"></div></div>';
        var loadunread = $('.loadunread');
        if(loadunread.length > 0){
          loadunread.click();
        } else {
          $('.items').prepend(precontent);
        }
    });
    $(this).val('发布');
    $(this).parents('form').children('textarea').val('');
    return false;
  });
  $('.twitter-comment-textbox .btn').live('click',
    function(){
      $(this).val('正在发布...');
      var items = $(this).parents('.twitter-comment-textbox').next();
      var url = $(this).parents('form').attr('action');
      var content = $(this).prev().val();
      var args = {"comment-content": content};
      args._xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
      $.post(url, $.param(args), function(data){
        data = eval("(" + data + ")");
        var precontent = "<div class='comment-iterm'><a href='/user/" + data.username + "'><img class='avatar' src='" + data.avatar + "'></a><div class='comment-content'><div class='name'><strong>" + data.username + "</strong></div><div class='content'>" + data.content + "</div><div class='info'><small>" + data.time +" </small></div></div>";
        items.prepend(precontent);
      });
      $(this).val('发布');
      $(this).prev().val('');
      return false;
  });
  $('.loadmore').click(function(){
    $(this).html('正在加载...');
    var page_url = $(this).attr('href');
    var page = page_url.substr(page_url.lastIndexOf('/')+1,page_url.length);
    var base_url = page_url.substr(0,page_url.lastIndexOf('/')+1);
    var url = base_url + page;
    var urled = base_url + (parseInt(page) + 1);
    var hi='nihao';
    $.get(url, function(data){
      var loadmore = $('.loadmore');
      loadmore.attr('href', urled);
      if(data.length<=2){
        loadmore.html('已加载完毕').css({'text-decoration': 'none'});
      } else {
        loadmore.html('更多');
      }
      $('.items').append(data);
      return false;
    });
    return false;
  });
  $('.loadunread').live('click', function(){
    $(this).html('正在加载...');
    $.get('/loadunread', function(data){
      $('.loadunread').remove();
      $('.items').prepend(data);
      return false;
    });
    $('.loadunread').html('已加载完毕');
    return false;
  });
});
