var get_cookie = function(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r?r[1]:undefined;
}

var get_captcha = function(url) {
    var uri = url + '?t=' + String(Math.random()).slice(3,8);
    $("#captcha-image").attr('src', uri);
}

$(function(){
  $('#twitter-input').focus().click(function(){
    $(this).animate({'height':'4.8em'});
    $('.twitter-action').fadeIn(300);
  }).keyup(function(){
    if($(this).height() < 63 && $(this).val().length >= 2){
      $(this).triggerHandler('click');
    };
  });
  /*$('#twitter-input').mouseover(function(){
    $(this).focus();
  });*/
  $('input.comment-editor').live('mouseover', function(){
  //$('.item').delegate('.comment-editor', 'mouseover', function(){
    $(this).focus();
  });
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
          "background-color":"#fff",
          "box-shadow":"0px 0px 10px rgba(0,0,0,0.8)",
          "min-width":"160px",
          "top":top,
          "left":left
        }).show("fast");
      }
    )
  });

  $('.twitter-item').live('hover',
    function(){
      $(this).find('.info .action ul').toggle();
    }
  );
  $('.reply').live('click',
    function(){
      $(this).parents('.item').find('.comment-wrap').slideToggle();
    }
  );
  $('.del').live('click', function(){
    var idx = $(this).parents('.twitter-item').attr('id');
    var id = idx.substr(idx.indexOf('_') + 1, idx.length);
    $('.lightbox').remove();
    $('#confirm-box').remove();
    var item = $(this).parents('.twitter-item').html();
    var markup = [
      '<div class="lightbox"></div>',
      '<section id="confirm-box" class="box no-padding">',
      '<header>确定要删除这条推文吗?</header>',
      '<div class="confirm-content"></div>',
      '<div class="confirm-action"><a id="del_',
      id,
      '" class="ok btn mini-btn" href="#;">确认</a>',
      '<a class="cancle btn mini-btn" href="#;">取消</a></div>',
      '</section>'
    ].join('');
    $(markup).hide().appendTo('body').fadeIn();
    return false;
  });
  $('#confirm-box .ok').live('click', function(){
    var idx = $(this).attr('id');
    var id = idx.substr(idx.indexOf('_') + 1, idx.length);
    var url = '/post/' + id + '/del';
    $.get(url);
    var post_count_area = $('#sidebar .mini-profile .stats li:first a strong');
    var post_count = parseInt(post_count_area.html());
    post_count -= 1;
    post_count_area.html(post_count);
    $('.lightbox').fadeOut();
    $('#confirm-box').fadeOut();
    $('#post_' + id).fadeOut();
    return false;
  });
  $('.display').live('click', function(){
    $(this).next('.hide').toggle();
    $(this).remove();
    return false;
  });
  $('#confirm-box .cancle').live('click', function(){
    $('.lightbox').fadeOut();
    $('#confirm-box').fadeOut();
    return false;
  });
  $('input.comment-editor').live('keydown', function(e){
    if(e.ctrlKey && e.keyCode == 13){
      $(this).next('input.btn')[0].click();
      //alert($(this).next('input')[0].value);
      return false;
    }
  });
  $('.twitter-action .btn').live('click',function(){
    if($(this).parents('#twitter').children('#twitter-input').val() == ''){
      return false;
    }
    $(this).val('正在发布...');
    var content = $(this).parents('form').children('textarea').val();
    var args = {"content": content};
    args._xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
    $.post("/post/add", $.param(args), function(data){
      data = eval("(" + data + ")");
      var precontent = '<li id="post_' + data.id + '" class="item twitter-item"><a href="/user/'+ data.username + '"><img class="avatar" src="' + data.avatar +'"></a><div class="twitter-content"><div class="name"><a href="/user/' + data.username + '"><strong>' + data.username + '</strong></a></div><div class="content">' + data.content + '</div><div class="info"><a href="/post/' + data.id + '"><small>' + data.time + '</small></a><div class="action"><ul style="display: none;"><li><a class="reply" href="#;">reply</a></li><li><a class="del" href="/post/' + data.id + '/del">del</a></li><li><a class="fav" href="/post/' + data.id + '/fav">fav</a></li></ul></div></div></div><div class="comment-wrap"><div class="comment-textbox"><form method="post" action="/post/' + data.id + '/comment/add"><input class="comment-editor" type="text" name="comment-content" size="35"><input class="btn mini-btn comment-submit" type="submit" value="发布"><input type="hidden" name="_xsrf" value="' + args._xsrf + '"></form></div><div class="comments"></div></li>';
      //var precontent = data;
      var loadunread = $('.loadunread');
      if(loadunread.length > 0){
        loadunread.click();
      } else {
        $(precontent).clone().hide().prependTo('.twitter-items').slideDown();
      }
      $('.twitter-action .btn').val('发布');
      var post_count_area = $('#sidebar .mini-profile .stats li:first a strong');
      var post_count = parseInt(post_count_area.html());
      post_count += 1;
      post_count_area.html(post_count);
    });
    $(this).parents('form').children('textarea').val('');
    return false;
  });
  $('.comment-textbox .btn').live('click',
    function(){
      if($(this).parents('form').children('.comment-editor').val()==''){
        return false;
      }
      $(this).val('正在发布...');
      var idx = $(this).parents('.twitter-item').attr('id');
      var id = idx.substr(idx.indexOf('_') + 1, idx.length);
      var items = $(this).parents('.comment-textbox').next();
      var url = $(this).parents('form').attr('action');
      var content = $(this).prev().val();
      var args = {"comment-content": content};
      args._xsrf=document.cookie.match("\\b" + "_xsrf" + "=([^;]*)\\b")[1];
      $.post(url, $.param(args), function(data){
        data = eval("(" + data + ")");
        var precontent = "<li class='comment-item'><a href='/user/" + data.username + "'><img class='avatar' src='" + data.avatar + "'></a><div class='comment-content'><div class='name'><strong>" + data.username + "</strong></div><div class='content'>" + data.content + "</div><div class='info'><small>" + data.time +" </small></div></li>";
        $(precontent).clone().hide().prependTo(items).slideDown();
        $('#post_' + id + ' .comment-textbox .btn').val('发布');
      });
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
      if($.browser.webkit){
        $(data).clone().hide().appendTo('section > .items').slideDown();
      } else {
        $(data).appendTo('section > .items');
      }
      return false;
    });
    return false;
  });
  $('#loadunread').live('click', function(){
    $.get('/loadunread', function(data){
      $('.loadunread').html('正在加载...');
      if($.browser.webkit){
        //$(data).clone().hide().prependTo('section > .items').fadeIn();
        //$('#loadunread').after(data);
        $(data).insertAfter('#loadunread').hide().fadeIn();
      } else {
        //$(data).prependTo('section > .items');
        $(data).insertAfter('#loadunread');
      }
      $('.loadunread').html('加载完毕');
      $('#loadunread').hide();
    });
    return false;
  });
  $('.fav').live('click', function(){
    var url = $(this).attr('href');
    $.get(url);
    if($(this).html()=='fav'){
      $(this).html('faved').addClass('faved');
    } else {
      $(this).html('fav').removeClass('faved');
    }
    return false;
  });
  $('.retweet').live('click', function(){
    var url = $(this).attr('href');
    var post_count_area = $('#sidebar .mini-profile .stats li:first a strong');
    var post_count = parseInt(post_count_area.html());
    $.get(url);
    if($(this).html()=='retweet'){
      $(this).html('retweeted').addClass('retweeted');
      post_count += 1;
      post_count_area.html(post_count);
    } else {
      $(this).html('retweet').removeClass('retweeted');
      post_count -= 1;
      post_count_area.html(post_count);
    }
    return false;
  });
});
