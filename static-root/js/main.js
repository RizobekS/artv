$(document).ready(function () {
  $('.filter-content a.title').on('click', function (e) {
    e.preventDefault();
    $(this).siblings('ul').slideToggle()
  })
  $('.slider-for').not('.slick-initialized').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.slider-nav'
  });
  $('.slider-nav').not('.slick-initialized').slick({
    slidesToShow: 5,
    slidesToScroll: 1,
    asNavFor: '.slider-for',
    focusOnSelect: true,
    dots: false,
    vertical:true,
    centerMode: false,
    responsive:[
      {
        breakpoint:600,
        settings:{
          vertical:false
        }
      }
    ]
  });
  $('.has-menu').on('click', function (e) {
      e.preventDefault()
  })
  $('.currency-list .selected').on('click', function (e) {
    e.preventDefault();
    $(this).siblings('ul').toggleClass('show')
  })
  $('.currency-list ul a').on('click', function (e) {
    e.preventDefault();
    const type = $(this).data('type');
    const lastClass = $('.selected').attr('class').split(' ').pop();
    $(this).parents('ul').siblings('.selected').removeClass(lastClass).addClass(type).text($(this).html());
    $('[name=currency]').val(type);
    $(this).parents('ul').removeClass('show')
  })
  $("#mygallery").justifiedGallery({
    rowHeight : 230,
    maxRowsCount:2,
    randomize:false,
    captions:false,
    lastRow:'hide',
    margins : 10
  });
  $('.home-slider').on('init', function(event){
    $('.no-slide').css('pointer-events', 'none')
  }).slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    dots:true,
    infinite:false,
    arrows: true,
    vertical:false,
    fade: false,
  });
  $('.home-slider-nav').on('init', function(event){
    $('.no-slide').css('pointer-events', 'none')
  }).slick({
    slidesToShow: 8,
    slidesToScroll: 1,
    infinite:false,
    asNavFor: '.home-slider',
    focusOnSelect: true,
    dots: false,
    vertical:true,
    centerMode: false,
  })
  let data = {};
  $('[data-filterbtn]').on('click', function (e) {
    e.preventDefault();
    let type = $(this).data('type');
    let value = $(this).data('value');
    let div = $('#cards-main');
    let url = $(this).data('url');
    data[type] = value;
    $('[data-filterBtn]').removeClass('active');
    $(this).addClass('active')
    $.ajax({
      url:url,
      data:data,
      beforeSend:function () {
        div.addClass('loading')
      },
      success:function (res) {
        div.empty();
        div.append(res);
        div.removeClass('loading')
      }
    })
  });
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');
  $('[data-favorite]').on('click',function(e){
    e.preventDefault()
    const $this = $(this);
    let url = '';
    let method = 'GET';
    const id = $(this).data('id');
    const div = document.createElement('div');

    if($this.hasClass('active')){
      url = $(this).data('remove-url')
      method = 'DELETE';
    }else{
      url = $(this).data('add-url')
    }
    $.ajax({
      url: url,
      type:method,
      headers:method === 'DELETE' ? {
        'X-CSRFToken': csrftoken
      } : null,
      dataType: 'json',
      success: function(res, text, status){
        if(status.status == 200 || status.status === 201){
          ['alert','alert-success','show'].forEach(item => div.classList.add(item));
          if($this.data('favoritebtn')){
            div.innerHTML = 'Вы добавили товар в избранные';
          }else{

            div.innerHTML = 'Вы добавили товар в корзину';
            $('.header-actions .counter').html(res.cart_items)
          }
        }
        else{
          ['alert','alert-danger','show'].forEach(item => div.classList.add(item));
          if($this.data('favoritebtn')){
            div.innerHTML = 'Вы удалили товар из избранных';
          }else{
            div.innerHTML = 'Вы удалили товар из корзины';
            $('.header-actions .counter').html(parseInt($('.header-actions .counter').html()) - 1)
          }
        }
        $this.toggleClass('active');
        $('.wrapper').append(div);
        setTimeout(()=>{
          $('.wrapper .alert').removeClass('show').remove();
        }, 3000)
      }
    });
  });
  $('.search form input').on('input', function (e) {
    const {value} = e.target;
    data['q'] = value;
    const url = $(this).parent('form').attr('action')
    let div = $(this).parent('form').siblings('.result');
    $.ajax({
      url:url,
      data:data,
      success:function (res) {
        div.empty();
        res.forEach(item => {
          div.append(`<li>${item}</li>`);
        });
        div.addClass('show');
      }
    })
  })
  $('.home-slider-nav .slide').on('click', function () {
    if($(this).hasClass('no-slide')) return;
  })
  $( "#slider-range" ).slider({
    range: true,
    min: 130,
    max: 500,
    values: [ 130, 250 ],
    slide: function( event, ui ) {
      let url = $(this).data('url');
      data['price'] = `${ui.values[ 0 ]},${ui.values[ 1 ]}`;
      let div = $('#cards-main');
      $.ajax({
        url:url,
        data:data,
        beforeSend:function () {
          div.addClass('loading')
        },
        success:function (res) {
          div.empty();
          div.append(res);
          div.removeClass('loading')
        }
      })
    }
  });
  $('[data-loadMore]').off('click').on('click', function(e){
    e.preventDefault()
    let $this = $(this),
      url = $this.attr('data-url'),
      target = $this.attr('data-target'),
      start = parseInt($this.attr('data-start')),
      end = parseInt($this.attr('data-end'));
    $this.hide();
    $.ajax({
      url: url,
      method:'get',
      success: function (response) {
        const current = start += 5;
        $(target).append($.parseHTML(response));
        if (current < end) {
          $this.show();
          $this.attr('data-start', current);
        } else {
          $this.attr('data-start', end);
        }
      }
    })
  });
  $(".fancybox").fancybox({
    'overlayShow'	: false,
    'transitionIn'	: 'elastic',
    'transitionOut'	: 'elastic'
  });
  $('.mobile-slider').each(function(){
    if($(this).find('.card').length > 4){
      $(this).not('.slick-initialized').slick({
        slidesToShow:4,
        slidesToScroll: 1,
        focusOnSelect: true,
        dots: false,
        arrow:true,
        vertical:false,
        centerMode: false,
        responsive:[
          {
            breakpoint:600,
            settings:{
              slidesToShow:2,
              vertical:false
            }
          }
        ]
      });
      $(this).addClass('slider')
    }else{
      $(this).addClass('no-slide')
    }
  })
  $(window).resize(function () {
    if(this.innerWidth < 768){
      $('.mobile-slider').each(function(){
        if($(this).find('.card').length > 4){
          $(this).not('.slick-initialized').slick({
            slidesToShow:3,
            slidesToScroll: 1,
            focusOnSelect: true,
            dots: false,
            arrow:true,
            vertical:false,
            centerMode: false,
          });
        }else{
          $(this).addClass('no-slide')
        }
      })
    }
  })
  if(window.innerWidth < 768){
    $('.mobile-slider').each(function(){
      if($(this).find('.card').length > 2){
        $(this).not('.slick-initialized').slick({
          slidesToShow:2,
          slidesToScroll: 1,
          focusOnSelect: true,
          dots: false,
          arrow:true,
          vertical:false,
          centerMode: false,
        }).addClass('slide-mobile');
      }else{
        $(this).addClass('no-slide')
      }
    })
  }
  $('#burger').on('click', function(){
    $(this).toggleClass('open');
    $('nav').toggle()
  })

  $('.toggle-password').on('click', function (e) {
      e.preventDefault();
      $(this).children('svg').toggle()
     if($(this).siblings('input').attr('type') === 'password'){
       $(this).siblings('input').attr('type', 'text')
     }else{
       $(this).siblings('input').attr('type', 'password');
     }
  })
  $('.accordion .button').on('click', function(){
    $(this).siblings().slideToggle()
  })
  // $('[data-favorite]').on('click',function(e){
  //   e.preventDefault()
  //   const $this = $(this);
  //   let url = '';
  //   const id = $(this).data('id');
  //   if($this.hasClass('active')){
  //     url = $(this).data('remove-url')
  //   }else{
  //     url = $(this).data('add-url')
  //   }
  //   $.ajax({
  //     url: url,
  //     type:'GET',
  //     dataType: 'json',
  //     success: function(){
  //       $this.toggleClass('active');
  //     }
  //   });
  // });
  $('.filter').select2();
  function formatState (state) {
    if (!state.id) {
      return state.text;
    }
    const img = state.element.value === '1' ? '../img/down.png' : '../img/up.png';
    return $(
      '<span>' + state.text + '<img src="' + img + '" class="img-flag" /></span>'
    );
  };

  $(".sorting").select2({
    templateResult: formatState,
  });
  $('.plus').on('click', function (e) {
    e.preventDefault()
    let val = +$(this).siblings('input[type=text]').val() + 1;
    $(this).siblings('input[type=text]').val(val)
  })
  $('.minus').on('click', function (e) {
    e.preventDefault()
    if($(this).siblings('input').val() <= 0) return;
    let val = +$(this).siblings('input[type=text]').val() - 1;
    $(this).siblings('input[type=text]').val(val)
  })
  $(".phone").intlTelInput({
    onlyCountries: ["uz"],
  });
})
