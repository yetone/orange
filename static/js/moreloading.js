
  $('.items').scrollPagination({
    'contentPage': '/data1',
    'contentData': {},
    'scrollTarget': $(window),
    'heightOffset': 2,
    'beforeLoad': function(){
      $('#loading').fadeIn();
    },
    'afterLoad': function(elementsLoaded){
      $('#loading').fadeOut();
      var i = 0;
      $(elementsLoaded).fadeInWithDelay();
      if($('.items').children('.item').size() > 16){
        $('#nomoreresults').fadeIn();
        $('.items').stopScrollPagination();
      }
    }
  })
