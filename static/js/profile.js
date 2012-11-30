$(function(){
  $('.profile-action .btn').click(function(){
    var origin_url = $(this).attr('href');
    var url = origin_url.substr(0,origin_url.lastIndexOf('/'));
    var followeder_count = $('.stats li:eq(1) strong');
    var user_item = $('.user-item');
    if($(this).html()==='关注'){
      url = url + '/follow';
      $.get(url);
      $(this).removeClass('unfo');
      $(this).html('已关注');
      if(user_item.length){
        count = parseInt(followeder_count.html()) + 1
        followeder_count.html(count)
        return false;
      }
      return false;
    } else if ($(this).html()==='已关注'){
      url = url + '/unfollow';
      $.get(url);
      $(this).addClass('unfo');
      $(this).html('关注');
      if(user_item.length > 0){
        count = parseInt(followeder_count.html()) - 1;
        followeder_count.html(count);
        return false;
      }
      return false;
    }
  });
  $('.profile-nav li').live('click', function(){
    $('.active').removeClass('active');
    $(this).addClass('active');
    var url = $(this).children('a').attr('href');
    $.get(url, function(data){
      $('#mainbar section ul').html('');
      //$(data).clone().hide().appendTo('#mainbar section ul').fadeIn();
      if($.browser.webkit){
        $(data).clone().hide().appendTo('#mainbar section ul').fadeIn();
      } else {
        $(data).appendTo('#mainbar section ul');
      }
      $('.loadmore').attr('href', url + '/page/2').html('更多');
      if(data.length <= 2){
        $('#loadmore').remove();
      }
    });
    return false;
  });
});
