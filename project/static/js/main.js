


$(document).ready(function(){
    $(window).on("scroll",function(){
        if($(this).scrollTop()>90){
            $(".navbar").addClass("navbar-shrink");
        }
        else{
            $(".navbar").removeClass("navbar-shrink");
        }
    });

    const videoSrc = $("#player-1").attr("src");
    $(".video-play-btn, .video-popup").on("click",function(){
        if($(".video-popup").hasClass("open")){
            $(".video-popup").removeClass("open");
            $("#player-1").attr("src","");
        }
        else{
            $(".video-popup").addClass("open");
                if($("#player-1").attr("src")==''){
                    $("#player-1").attr("src",videoSrc);
            }
        }
    });
    $('.features-carousel').owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
              
            },
            600:{
                items:2,
             
            },
            1000:{
                items:3,
             
            },
            1400:{
                items:4
             
            },
            1800:{
                items:5
             
            },
            2200:{
                items:6
             
            }
            
        }
    });
    $('.crypto-carousel').owlCarousel({
        loop:true,
        autoplay:true,
        margin:0,
        responsiveClass:false,
        responsive:{
            0:{
                items:1,
              
            },
            
            800:{
                items:4,
             
            }
            
        }
    });
    $('.screenshots-carousel').owlCarousel({
        loop:true,
        margin:0,
        autoplay:true,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
              
            },
            600:{
                items:2,
             
            },
            1000:{
                items:3,
             
            }
        }
        
    });
    $.scrollIt({
        topOffset: -50
    });

    $(".nav-link").on("click",function(){
        $(".navbar-collapse").collapse("hide");
    });
});
