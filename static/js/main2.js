var textWrapper1 = document.querySelector('.ml5 .letters1');
textWrapper1.innerHTML = textWrapper1.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml5 .letter',
        translateY: ["3em", 0],
        translateZ: 0,
        duration: 1000,
        delay: (el, i) => 50 * i
    })

$('.owl-carousel').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    dots: false,
    dotsEach: false,
    responsive:{
        0:{
            items:2
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
    }
})