
  

function get_artwork_detail(url, value){
  let data = {keyword : value.toString(),
              indicator : "get_aw_detail"}
  res = request_ajax(url, data)
  if (res != 'error'){
      $('#modal_detail_artwork').replaceWith(res);
  }
  const modals = document.querySelector('#modal_detail_artwork');
  let modal = bootstrap.Modal.getOrCreateInstance(modals);
  modal.show()
}
    

function send_keyword(url, value){
    if (value.length >= 2) {
      data = {'keyword' : value,
              'indicator' : 'get_startswith'}
      res = request_ajax(url, data)
      if (res != 'error') {
        $('#search_list').replaceWith(res)
      }
    }
}


$(document).ready(function(){
    let sb = document.getElementById('service_banner');
    let mb = document.getElementById('mask_banner');
    fadeOutOnScroll(mb, sb);
})

function fadeOutOnScroll(element, element_o) {
  if (!element) {
    return;
  }
  let distanceToTop = window.pageYOffset + element.getBoundingClientRect().top;
  let elementHeight = element.offsetHeight;
  let scrollTop = document.documentElement.scrollTop;
  
  let opacity = 1;
  if (scrollTop > distanceToTop) {
    opacity = 1 - (scrollTop) / elementHeight;
  }
  element_o.style.opacity = opacity;
}

function scrollHandler() {
    let sb = document.getElementById('service_banner');
    let mb = document.getElementById('mask_banner');
    fadeOutOnScroll(mb, sb);
}

window.addEventListener('scroll', scrollHandler);


function rowOutFocus(element){
  let arr = element.parent().children(".artwork");
  [].forEach.call (arr, function (el, index) {
    arr.eq(index).addClass('outfocus');
  });
}

function rowSetFocus(element){
  let arr = element.parent().children(".artwork");
  [].forEach.call (arr, function (el, index) {
    arr.eq(index).removeClass('outfocus');
  });
}