$(document).ready(function(){const csrftoken=getCookie('csrftoken');$('.slider-for').not('.slick-initialized').slick({slidesToShow:1,slidesToScroll:1,arrows:!1,fade:!0,asNavFor:'.slider-nav'});$('.slider-nav').not('.slick-initialized').slick({slidesToShow:5,slidesToScroll:1,asNavFor:'.slider-for',focusOnSelect:!0,dots:!1,vertical:!0,centerMode:!1,responsive:[{breakpoint:600,settings:{vertical:!1}}]});$('.has-menu').on('click',function(e){e.preventDefault()})
$.fn.datepicker.languages['zh-CN']={format:'yyyy年mm月dd日',days:['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],daysShort:['周日','周一','周二','周三','周四','周五','周六'],daysMin:['日','一','二','三','四','五','六'],months:['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],monthsShort:['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],weekStart:1,startView:0,yearFirst:!0,yearSuffix:'年'};$.fn.datepicker.languages['ru-RU']={days:["Воскресенье","Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"],daysShort:["Вск","Пнд","Втр","Срд","Чтв","Птн","Суб"],daysMin:["Вс","Пн","Вт","Ср","Чт","Пт","Сб"],months:["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"],monthsShort:["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"],today:"Сегодня",clear:"Очистить",format:"dd.mm.yyyy",weekStart:1,monthsTitle:"Месяцы"};$.fn.datepicker.languages['uz']={days:'Якшанба_Душанба_Сешанба_Чоршанба_Пайшанба_Жума_Шанба'.split('_'),daysShort:'Якш_Душ_Сеш_Чор_Пай_Жум_Шан'.split('_'),daysMin:'Як_Ду_Се_Чо_Па_Жу_Ша'.split('_'),months:'январ_феврал_март_апрел_май_июн_июл_август_сентябр_октябр_ноябр_декабр'.split('_'),monthsShort:'янв_фев_мар_апр_май_июн_июл_авг_сен_окт_ноя_дек'.split('_'),today:"Бугун",clear:"Тозалаш",format:"dd.mm.yyyy",weekStart:1,monthsTitle:"Ойлар"};$("#datepicker").datepicker({autoHide:!0,format:'DD.MM.YYYY',language:$('html').attr('lang')}).on('pick.datepicker',function(e){$('[name=date_of_birth]').val(dayjs(e.date).format('YYYY-DD-MM'))})
$('.currency-list.selected').on('click',function(e){e.preventDefault();$(this).siblings('ul').toggleClass('show')})
$('.remove-item').off('click').on('click',function(e){e.preventDefault();const $this=$(this);const url=$this.attr('href');$.ajax({url,method:'DELETE',headers:{'X-CSRFToken':csrftoken},success:function(){$this.parents('.bordered').addClass($this.data('animation-class'));$this.parents('.bordered').bind('animationend animationend webkitAnimationEnd',function(){$this.parents('.bordered').remove();const div=document.createElement('div');['alert','alert-success','show'].forEach(item=>div.classList.add(item));div.innerHTML='Вы успешно Удалили товар';$('.wrapper').append(div)})}})})
$('.tabs-link').on('click',function(e){e.preventDefault();const index=$(this).data('index');$('.tabs').removeClass('active');$(`.tab-${index}`).addClass('active');$('.tabs-link').removeClass('active');$(this).addClass('active')})
$(document).on('click',function(e){var $target=$(event.target);if(!$target.closest('.currency-list').length&&$('.currency-list').is(":visible")){$('.currency-list ul').removeClass('show')}})
$('.currency-list ul a').on('click',function(e){e.preventDefault();const type=$(this).data('type');const lastClass=$('.currency-list.selected').attr('class').split(' ').pop();$(this).parents('ul').siblings('.selected').removeClass(lastClass).addClass(type.toLowerCase()).text($(this).html());$('[name=currency]').val(type);$(this).parents('ul').removeClass('show')})
$("#mygallery").justifiedGallery({rowHeight:230,maxRowsCount:2,randomize:!1,captions:!1,lastRow:'hide',margins:10});$('.home-slider').on('init',function(event){$('.no-slide').css('pointer-events','none')}).slick({slidesToShow:1,slidesToScroll:1,dots:!0,infinite:!1,arrows:!0,vertical:!1,fade:!1,});$('.home-slider-nav').on('init',function(event){$('.no-slide').css('pointer-events','none')}).slick({slidesToShow:8,slidesToScroll:1,infinite:!1,asNavFor:'.home-slider',focusOnSelect:!0,dots:!1,vertical:!0,centerMode:!1,})
function getCookie(name){let cookieValue=null;if(document.cookie&&document.cookie!==''){const cookies=document.cookie.split(';');for(let i=0;i<cookies.length;i++){const cookie=cookies[i].trim();if(cookie.substring(0,name.length+1)===(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break}}}
return cookieValue}
$('#id_password1').on('change,input',function(e){const{value}=e.target;if(!/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}/.test(value)){$(this).siblings('.helper-text2').show()}else{$(this).siblings('.helper-text2').hide()}})
function validate(inputs){inputs.forEach(function(input){$(input).parents('label').removeClass('error').find('.helper-text').hide()
if($(input).attr('id')==='id_email'){if(!/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test($('#id_email').val())){$(input).parents('label').addClass('error').find('.helper-text2').show()}else{$(input).parents('label').removeClass('error').find('.helper-text2').hide()}}
if($(input).attr('id')==='id_checkbox'){if(!$(input).is(':checked')){$(input).parents('label').addClass('error').find('.helper-text').show()}}
if($(input).attr('id')==='id_password2'){if($(input).val()!==$('#id_password1').val()){$(input).parents('label').addClass('error').find('.helper-text2').show()}else{$(input).parents('label').removeClass('error').find('.helper-text2').hide()}}
if(!$(input).val()){$(input).parents('label').addClass('error').find('.helper-text').show()}});if(!/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test($('#id_email').val())){return!0}
if($('#id_checkbox').is(':visible')){return!$('#id_checkbox').is(':checked')}
if($('#id_password2').val()!==$('#id_password1').val()||!/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}/.test($('#id_password1').val())){return!0}
return inputs.filter(item=>!item.value).length>0};$('.registration-form').on('submit',function(e){const inputs=$(this).find('input[required]');const selects=$(this).find('select[required]');const result=validate([...Array.from(selects),...Array.from(inputs)]);if(result){return!1}})
if($('.alert-content').children().length){const childrens=$('.alert-content').children();Array.from(childrens).forEach((item)=>{window.setTimeout($.proxy(function(){$(item).fadeTo(200,0).slideUp(200,function(){$(item).remove()})},item),1500)})}
$.mask.definitions['9']=!1;$.mask.definitions['5']="[0-9]";$('.profile-info form').on('submit',function(){document.profileForm.birth_date.value=document.profileForm.birth_date.value.split('.').reverse().join('-')
return!0})
$('.registration-form').on('submit',function(){document.profileForm.birth_date.value=document.profileForm.birth_date.value.split('.').reverse().join('-')
return!0})
$('.year').text($('.year').text().replace(/[^0-9 ]/g,''))
$('[data-favorite]').on('click',function(e){e.preventDefault()
const $this=$(this);if($(this).data('popup')){$('.popup').addClass('show');$('.wrapper,body').addClass('popup-show');return!1}
let url='';let method='GET';const id=$(this).data('id');const div=document.createElement('div');if($this.hasClass('active')){url=$(this).data('remove-url')
method='DELETE'}else{url=$(this).data('add-url')}
$.ajax({url:url,type:method,headers:method==='DELETE'?{'X-CSRFToken':csrftoken}:null,dataType:'json',success:function(res,text,status){$this.toggleClass('active');if($this.hasClass('active')){['alert','alert-success','show'].forEach(item=>div.classList.add(item));if($this.data('favoritebtn')){div.innerHTML='Вы добавили товар в избранные'}else{div.innerHTML='Вы добавили товар в корзину';$('.header-actions.counter').html(parseInt($('.header-actions.counter').html())+1)}}
else{['alert','alert-danger','show'].forEach(item=>div.classList.add(item));if($this.data('favoritebtn')){div.innerHTML='Вы удалили товар из избранных'}else{div.innerHTML='Вы удалили товар из корзины';$('.header-actions.counter').html(parseInt($('.header-actions.counter').html())-1)}}
$('.wrapper').append(div);setTimeout(()=>{$('.wrapper.alert').removeClass('show').remove()},3000)}})});$('.search form input').on('input',function(e){const{value}=e.target;data['q']=value;const url=$(this).parent('form').attr('action')
let div=$(this).parent('form').siblings('.result');$.ajax({url:url,data:data,success:function(res){div.empty();res.forEach(item=>{div.append(`<li>${item}</li>`)});div.addClass('show')}})})
$('.home-slider-nav.slide').on('click',function(){if($(this).hasClass('no-slide'))return})
$("#slider-range").slider({range:!0,min:130,max:500,values:[130,250],slide:function(event,ui){let url=$(this).data('url');data['price']=`${ui.values[0]},${ui.values[1]}`;let div=$('#cards-main');$.ajax({url:url,data:data,beforeSend:function(){div.addClass('loading')},success:function(res){div.empty();div.append(res);div.removeClass('loading')}})}});let data={page:1};const lang=$('html').attr('lang')
$('[data-loadMore]').off('click').on('click',function(e){e.preventDefault()
let $this=$(this),url=$this.attr('data-url');let div=$('#cards-main');$this.hide();$('.filters.title').each(function(){if($(this).data('value')){data.page=1;data[$(this).data('type').toLowerCase()]=$(this).data('value')}});data.page+=1;$.ajax({url:`/${lang}${url}/`,method:'get',data:{...data},beforeSend:function(){div.empty();div.addClass('loading')},success:function(response){div.removeClass('loading')
if(response.page.has_next){$this.show()}
generateCards(response.data)}})});const trans={en:{title:'Description',more:'Read more',lot:'Lot Number'},"zh-cn":{title:'描述',more:'閱讀全文',lot:'批號'},ru:{title:'Описание',more:'Подробнее',lot:'Номер лота'},uz:{title:'Tavsifi',more:"Ko'proq",lot:'Lot raqami'}}
Fancybox.bind("[data-fancybox]",{groupAll:!0,infinite:!1});function generateCards(items){items.forEach(item=>{const card=`<div class="card-auction">
                <a href="https://${item.url}" class="img">
                  ${status === 'sold' ? `<div class="badge">Продано</div>` : ''}
                  <span></span>
                  <img src="${item.photo}" alt="">
                </a>
                <div class="caption">
                  <div class="top">
                    <div class="title">
                      <a href="https://${item.url}">${trans[lang].title}</a>
                      <strong>${item.name}</strong>
                    </div>
                    <span>${trans[lang].lot} <strong>${item.lot}</strong></span>
                  </div>
                  <div class="bottom">
                    <span>
                      <svg width="13" height="20" viewBox="0 0 13 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6.49998 4.00015C7.16302 4.00015 7.7989 4.26355 8.26775 4.73239C8.73659 5.20123 8.99998 5.83711 8.99998 6.50015C8.99998 7.16319 8.73659 7.79908 8.26775 8.26792C7.7989 8.73676 7.16302 9.00015 6.49998 9.00015C5.83694 9.00015 5.20105 8.73676 4.73221 8.26792C4.26337 7.79908 3.99998 7.16319 3.99998 6.50015C3.99998 5.83711 4.26337 5.20123 4.73221 4.73239C5.20105 4.26355 5.83694 4.00015 6.49998 4.00015ZM6.49998 5.00015C6.10215 5.00015 5.72062 5.15819 5.43932 5.43949C5.15801 5.7208 4.99998 6.10233 4.99998 6.50015C4.99998 6.89798 5.15801 7.27951 5.43932 7.56081C5.72062 7.84212 6.10215 8.00015 6.49998 8.00015C6.8978 8.00015 7.27933 7.84212 7.56064 7.56081C7.84194 7.27951 7.99998 6.89798 7.99998 6.50015C7.99998 6.10233 7.84194 5.7208 7.56064 5.43949C7.27933 5.15819 6.8978 5.00015 6.49998 5.00015ZM1.79998 9.35715L6.49998 17.0872L11.2 9.35715C11.7069 8.52316 11.9827 7.5693 11.9992 6.59348C12.0157 5.61767 11.7722 4.65504 11.2938 3.80439C10.8154 2.95375 10.1192 2.24573 9.27675 1.753C8.43431 1.26027 7.47593 1.00058 6.49998 1.00058C5.52402 1.00058 4.56564 1.26027 3.7232 1.753C2.88076 2.24573 2.1846 2.95375 1.70617 3.80439C1.22774 4.65504 0.984277 5.61767 1.00076 6.59348C1.01725 7.5693 1.29309 8.52316 1.79998 9.35715ZM12.054 9.87715L6.49998 19.0122L0.945977 9.87715C0.347098 8.8915 0.0212576 7.76425 0.00189306 6.61109C-0.0174714 5.45792 0.270337 4.32037 0.835785 3.31517C1.40123 2.30996 2.22395 1.47331 3.21952 0.891066C4.21509 0.308821 5.34765 0.00195313 6.50098 0.00195312C7.65431 0.00195312 8.78687 0.308821 9.78243 0.891066C10.778 1.47331 11.6007 2.30996 12.1662 3.31517C12.7316 4.32037 13.0194 5.45792 13.0001 6.61109C12.9807 7.76425 12.6549 8.8915 12.056 9.87715H12.054Z" fill="#102d6a"></path>
                      </svg>
                      ${item.country}
                    </span>
                    <a href="https://${item.url}" class="buy">${trans[lang].more}</a>
                  </div>
                </div>
              </div>`;$('#cards-main').append(card)})}
$('.mobile-slider').each(function(){if($(this).find('.card').length>4){$(this).not('.slick-initialized').slick({slidesToShow:4,slidesToScroll:1,focusOnSelect:!0,dots:!1,infinite:!1,arrow:!0,vertical:!1,centerMode:!1,responsive:[{breakpoint:600,settings:{slidesToShow:2,autoplay:!0,vertical:!1}}]});$(this).addClass('slider')}else{$(this).addClass('no-slide')}})
$(window).resize(function(){if(this.innerWidth<768){$('.mobile-slider').each(function(){if($(this).find('.card').length>4){$(this).not('.slick-initialized').slick({slidesToShow:3,slidesToScroll:1,focusOnSelect:!0,dots:!1,arrow:!0,vertical:!1,centerMode:!1,})}else{$(this).addClass('no-slide')}})}})
if(window.innerWidth<768){$('.mobile-slider').each(function(){if($(this).find('.card').length>2){$(this).not('.slick-initialized').slick({slidesToShow:2,slidesToScroll:1,focusOnSelect:!0,dots:!1,arrow:!0,vertical:!1,centerMode:!1,}).addClass('slide-mobile')}else{$(this).addClass('no-slide')}})}
$('#burger').on('click',function(){$(this).toggleClass('open');$('nav').toggle()})
$('.toggle-password').on('click',function(e){e.preventDefault();$(this).children('svg').toggle()
if($(this).siblings('input').attr('type')==='password'){$(this).siblings('input').attr('type','text')}else{$(this).siblings('input').attr('type','password')}})
$('.accordion.button').on('click',function(){$(this).siblings().slideToggle()})
$('.filter').select2();$('[type=tel]').on('input',function(e){let{value}=e.target;if(!/^[0-9+]+$/.test(value)){e.target.value=e.target.value.replace(/[^\d]/,'')}})
$('.searchHandler').on('input',function(e){if(e.target.value.length>3){$(this).parents('form').find('.helper').hide()
$(this).parent().siblings('button').attr('disabled',!1)}else{$(this).parents('form').find('.helper').show()
$(this).parent().siblings('button').attr('disabled',!0)}})
function formatCurrency(state){if(!state.id){return state.text}
const img=state.element.value==='$'?'/static/img/eng.png':state.element.value==='¥'?'/static/img/china.png':state.element.value==='₽'?'/static/img/russia.png':state.element.value==='UZS'?'/static/img/uzbekistan.png':'';return $('<span style="align-items:center;justify-content:flex-start;">'+state.text+'<img width="30px" height="30px" style="order:-1;margin-right:15px;" src="'+img+'" class="img-flag"/></span>')};$('[name=currency]').select2({templateResult:formatCurrency,});$('.search-btn').on('click',function(){$('.popup-search').addClass('show')
$('.wrapper,body').addClass('popup-show')});function formatState(state){if(!state.id){return state.text}
const img=state.element.value==='1'?'/static/img/down.png':'/static/img/up.png';return $('<span>'+state.text+'<img src="'+img+'" class="img-flag"/></span>')};$(".sorting").select2({templateResult:formatState,});$('.plus').on('click',function(e){e.preventDefault()
let val=+$(this).siblings('input[type=text]').val()+1;$(this).siblings('input[type=text]').val(val)})
$('.minus').on('click',function(e){e.preventDefault()
if($(this).siblings('input').val()<=0)return;let val=+$(this).siblings('input[type=text]').val()-1;$(this).siblings('input[type=text]').val(val)})
$('.overlay').on('click',function(){$(this).parent('.popup').removeClass('show')
$('.wrapper,body').removeClass('popup-show')});
$('.logoAocv').on('click', function(){
  $(this).parent().addClass('visibleBlockCharter')
$(this).addClass('visibleCharter')
$('body').css({
  'overflow':'hidden'
})
$('.exit').css({
  'display':'block'
})
$('.burger').css({
  'display':'none'
})
staticScroll=$(window).scrollTop()
$(window).scrollTop(0)
})
$(".charterAac").on("click",function(){
$(this).parent().addClass('visibleBlockCharter')
$(this).addClass('visibleCharter')
$('body').css({
  'overflow':'hidden'
})
$('.exit').css({
  'display':'block'
})
$('.burger').css({
  'display':'none'
})
staticScroll=$(window).scrollTop()
$(window).scrollTop(0)})
$(".exit").on("click",function(){
$('.blockCharterAac').removeClass('visibleBlockCharter')
$('.blockAocv').removeClass('visibleBlockCharter')
$('.charterAac').removeClass('visibleCharter')
$('.logoAocv').removeClass('visibleCharter')
$('body').css({'overflow':'visible'})
$(this).css({'display':'none'})
$('.burger').css({'display':'block'})
$(window).scrollTop(staticScroll)})})