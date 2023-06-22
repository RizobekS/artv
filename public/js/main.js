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
  $("#mygallery").justifiedGallery({
    rowHeight : 230,
    randomize:false,
    maxRowsCount:5,
    captions:false,
    lastRow:'justify',
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
  $(document).on('click', function (e) {
    var $target = $(event.target);
    if(!$target.closest('.currency-list').length && $('.currency-list').is(":visible")) {
      $('.currency-list ul').removeClass('show')
    }
  })

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
  });
  $('.remove-item').off('click').on('click', function (e) {
    e.preventDefault();
    const $this = $(this);
    const url = $this.attr('href');
    $.ajax({
      url,
      success:function (res) {
        $this.parents('tr').addClass($this.data('animation-class'));
        $this.parents('tr').bind('oanimationend animationend webkitAnimationEnd', function() {
          $this.parents('tr').remove();
          const div = document.createElement('div');
          ['alert','alert-success','show'].forEach(item => div.classList.add(item));
          div.innerHTML = 'Вы успешно Удалили товар';
          $('.wrapper').append(div);
        });
      }
    })
  })
  $('.tabs-link').on('click', function (e) {
    e.preventDefault();
    const index = $(this).data('index');
    $('.tabs').removeClass('active');
    $(`.tab-${index}`).addClass('active');
    $('.tabs-link').removeClass('active');
    $(this).addClass('active');
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
  Fancybox.bind("[data-fancybox]", {
    groupAll: true,
    infinite:false
  });
  $('.mobile-slider').each(function(){
    if($(this).find('.card').length > 4){
      $(this).not('.slick-initialized').slick({
        slidesToShow:4,
        slidesToScroll: 1,
        focusOnSelect: true,
        dots: false,
        infinite:false,
        arrow:true,
        vertical:false,
        centerMode: false,
        responsive:[
          {
            breakpoint:600,
            settings:{
              slidesToShow:2,
              autoplay:true,
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
  $('.searchHandler').on('input', function (e) {
    if(e.target.value.length > 3 ){
      $(this).parents('form').find('.helper').hide()
      $(this).parent().siblings('button').attr('disabled', false)
    }else{
      $(this).parents('form').find('.helper').show()
      $(this).parent().siblings('button').attr('disabled', true)
    }
  })
  $('.currency-list .selected').on('click', function (e) {
    e.preventDefault();
    $(this).siblings('ul').toggleClass('show')
  })
  $('.currency-list ul a').on('click', function (e) {
    e.preventDefault();
    const type = $(this).data('type');
    const lastClass = $('.currency-list .selected').attr('class').split(' ').pop();
    $(this).parents('ul').siblings('.selected').removeClass(lastClass).addClass(type).text($(this).html());
    $('[name=currency]').val(type);
    $(this).parents('ul').removeClass('show')
  })
  $('.overlay').on('click', function () {
    $(this).parent('.popup').removeClass('show')
    $('.wrapper, body').removeClass('popup-show')
  })
  $('.search-btn').on('click', function () {
    $('.popup-search').addClass('show')
    $('.wrapper, body').addClass('popup-show')
  });
  $.fn.datepicker.languages['zh-CN'] = {
    format: 'yyyy年mm月dd日',
    days: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
    daysShort: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
    daysMin: ['日', '一', '二', '三', '四', '五', '六'],
    months: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
    monthsShort: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
    weekStart: 1,
    startView: 0,
    yearFirst: true,
    yearSuffix: '年'
  };
  $.fn.datepicker.languages['ru-RU'] = {
    days: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
    daysShort: ["Вск", "Пнд", "Втр", "Срд", "Чтв", "Птн", "Суб"],
    daysMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
    months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    monthsShort: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
    today: "Сегодня",
    clear: "Очистить",
    format: "dd.mm.yyyy",
    weekStart: 1,
    monthsTitle: "Месяцы"
  };
  $.fn.datepicker.languages['uz'] = {
    days: 'Якшанба_Душанба_Сешанба_Чоршанба_Пайшанба_Жума_Шанба'.split('_'),
    daysShort: 'Якш_Душ_Сеш_Чор_Пай_Жум_Шан'.split('_'),
    daysMin:'Як_Ду_Се_Чо_Па_Жу_Ша'.split('_'),
    months: 'январ_феврал_март_апрел_май_июн_июл_август_сентябр_октябр_ноябр_декабр'.split(
      '_'
    ),
    monthsShort: 'янв_фев_мар_апр_май_июн_июл_авг_сен_окт_ноя_дек'.split('_'),
    today: "Бугун",
    clear: "Тозалаш",
    format: "dd.mm.yyyy",
    weekStart: 1,
    monthsTitle: "Ойлар"
  };
  function removeTag(arr){
    Array.from(arr).forEach(item => {
      $(item).removeAttr("style" );
      if(item.innerText === '' || item.innerText === String.fromCharCode(160)){
        item.remove()
      }
      if(item.children.length){
        removeTag(item.children)
      }

    })
  }
  removeTag($('.article').children())

  $( "#datepicker" ).datepicker({
    autoHide:true,
    format:'DD.MM.YYYY',
    language: $('html').attr('lang')
  }).on('pick.datepicker', function (e) {
    $('[name=date_of_birth]').val(dayjs(e.date).format('YYYY-DD-MM'))
  })
  function validate(inputs){
    inputs.forEach(function (input) {
      $(input).parents('label').removeClass('error').find('.helper-text').hide()
      if($(input).attr('id') === 'id_email'){
        if (!/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test($('#id_email').val())){
          $(input).parents('label').addClass('error').find('.helper-text2').show()
        }else{
          $(input).parents('label').removeClass('error').find('.helper-text2').hide()
        }
      }
      if($(input).attr('id') === 'id_checkbox'){
        if (!$(input).is(':checked')){
          $(input).parents('label').addClass('error').find('.helper-text').show()
        }
      }
      if($(input).attr('id') === 'id_password2'){
        if ($(input).val() !== $('#id_password1').val()){
          $(input).parents('label').addClass('error').find('.helper-text2').show()
        }else{
          $(input).parents('label').removeClass('error').find('.helper-text2').hide()
        }
      }
      if(!$(input).val()){
        $(input).parents('label').addClass('error').find('.helper-text').show()
      }
    });
    if (!/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test($('#id_email').val())){
      return true;
    }

    if($('#id_checkbox').is(':visible')){
      if (!$('#id_checkbox').is(':checked')){
        return true;
      }
    }
    if($('#id_password2').val() !== $('#id_password1').val() || !/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}/.test($('#id_password1').val())){
      return true;
    }
    return inputs.filter(item => !item.value).length > 0
  };
  $('.registration-form').on('submit', function () {
    const inputs = $(this).find('input[required]');
    const selects = $(this).find('select[required]');
    const result = validate([...Array.from(selects), ...Array.from(inputs)]);
    if(result) {
      return false
    }
  })
  let timer;
  if($('.alert-content').children().length){
    const childrens = $('.alert-content').children();
    Array.from(childrens).forEach((item) => {
      window.setTimeout($.proxy(function() {
        $(item).fadeTo(200, 0).slideUp(200, function(){
          $(item).remove();
        });
      }, item), 1500);
    })
  }
  $('[name=tel]').on('input', function (e) {
      let {value} = e.target;
      if(!/^[0-9+]+$/.test(value)){
        e.target.value = e.target.value.replace(/[^\d]/, '')
      }
  })
  $('.searchHandler').on('input', function (e) {
    if(e.target.value.length > 3 ){
      $(this).parent().siblings('button').attr('disabled', false)
    }else{
      $(this).parent().siblings('button').attr('disabled', true)
    }
  })
  $('.year').text($('.year').text().replace(/[^0-9 ]/g, ''))
  $.mask.definitions['9'] = false;
  $.mask.definitions['5'] = "[0-9]";
  $.fn.setCursorPosition = function(pos) {
    if (this.setSelectionRange) {
      this.setSelectionRange(pos, pos);
    } else if (this.createTextRange) {
      var range = this.createTextRange();
      range.collapse(true);
      if(pos < 0) {
        pos = $(this).val().length + pos;
      }
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  }
  $('#id_password1').on('change, input', function (e) {
    const {value} = e.target;
    if(!/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}/.test(value)){
      $(this).siblings('.helper-text2').show();
    }else{
      $(this).siblings('.helper-text2').hide();
    }
  })

  $('[data-favorite]').on('click',function(e){
    e.preventDefault()
    const $this = $(this);
    if($(this).data('popup')){
      $('.popup').addClass('show');
      $('.wrapper, body').addClass('popup-show');
      return false
    }
    let url = '';
    const id = $(this).data('id');
    const div = document.createElement('div');

    if($this.hasClass('active')){
      url = $(this).data('remove-url')
    }else{
      url = $(this).data('add-url')
    }
    $.ajax({
      url: url,
      type:'GET',
      dataType: 'json',
      success: function(res, text, status){
        if(status === 200 || status === 201){
          ['alert','alert-success','show'].forEach(item => div.classList.add(item));
          if($this.data('favoriteBtn')){
            div.innerHTML = 'Вы добавили товар в корзину';
          }else{
            div.innerHTML = 'Вы добавили товар в избранные';
          }
        }
        else{
          ['alert','alert-danger','show'].forEach(item => div.classList.add(item));
          if($(this).data('favoriteBtn')){
            div.innerHTML = 'Вы удалили товар из корзины';
          }else{
            div.innerHTML = 'Вы удалили товар из избранных';
          }
        }
        $this.toggleClass('active');
        $('.wrapper').append(div);
      }
    });
  });
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
  $(".select2").select2();
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
  $('.profile-info form').on('submit', function () {
    document.profileForm.birth_date.value = document.profileForm.birth_date.value.split('.').reverse().join('-')
    return true
  })

  // $('.profile-info form').on('beforeload', function () {
  //   document.profileForm.birth_date.value = document.profileForm.birth_date.value.split('-').reverse().join('.')
  // })
  $(".phone").on('input', function(e){
    e.target.value = e.target.value.replace(/([^+0-9\b]+)/gi, '');
  })
  // const input = document.querySelector(".phone");
  // window.intlTelInput(input, {
  //   utilsScript:
  //     "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
  // });
  // $('.payment').on('click', function () {
  //   $('.popup').addClass('show')
  //   $('.wrapper, body').removeClass('popup-show')
  // })
  // $('[data-numeric]').payment('restrictNumeric');
  // $('.cc-number').payment('formatCardNumber');
  // $('.cc-exp').payment('formatCardExpiry');
  // $('.cc-cvc').payment('formatCardCVC');
  //
  // $.fn.toggleInputError = function(erred) {
  //   this.parent('.form-group').toggleClass('has-error', erred);
  //   return this;
  // };
  //
  // $('.payment-form').submit(function(e) {
  //   e.preventDefault();
  //   var cardType = $.payment.cardType($('.cc-number').val());
  //   $('.cc-number').toggleInputError(!$.payment.validateCardNumber($('.cc-number').val()));
  //   $('.cc-exp').toggleInputError(!$.payment.validateCardExpiry($('.cc-exp').payment('cardExpiryVal')));
  //   $('.cc-cvc').toggleInputError(!$.payment.validateCardCVC($('.cc-cvc').val(), cardType));
  //   $('.cc-brand').text(cardType);
  // });
})
