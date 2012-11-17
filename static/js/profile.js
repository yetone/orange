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
});
