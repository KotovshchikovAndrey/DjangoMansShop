window.addEventListener('DOMContentLoaded',function(){
    let burger = document.querySelector('.header-burger-img')
    let burger_menu = document.querySelector('.header-burger-nav')
    let burger_close = document.querySelector('.header-burger-close-img')
    let search_btn = document.querySelectorAll('.search')
    let serch_form = document.querySelector('.header-search-form')
    
    burger.addEventListener('click',function(){
        burger_menu.classList.add('burger-active')
    })

    burger_close.addEventListener('click',function(){
        burger_menu.classList.remove('burger-active')
    })

    search_btn.forEach(function(e){
        e.addEventListener('click',function(){
            serch_form.classList.toggle('active-search-form')
        })
    })
})