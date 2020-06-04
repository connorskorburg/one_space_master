
var swiper = new Swiper('.swiper',
{
  spaceBetween: 30,
  loop: true,
  loopFillGroupWithBlank: true,
  centeredSlides: true,
  autoplay: {
    delay: 6500,
    disableOnInteraction: false,
},
pagination:
{
  el: '.swiper-pagination',
  clickable: true,
},
navigation:
{
  nextEl: '.swiper-button-next',
  prevEl: '.swiper-button-prev',
},
});
var swiper = new Swiper('.swiper-1',
{
slidesPerView: 9,
loop: true,
loopFillGroupWithBlank: true,
autoplay:
{
  delay: 2500,
  disableOnInteraction: false,
},
pagination:
{
  el: '.swiper-pagination-1',
  clickable: true,
},
navigation: {
  nextEl: '.next-1',
  prevEl: '.prev-1',
},
});



$(document).on("click", ".navbar-right .dropdown-menu", function(e){
  e.stopPropagation();
});
