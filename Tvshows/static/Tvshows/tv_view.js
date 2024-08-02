$(document).ready(function() {
    function initializeCarousel(selector) {
  
      if(selector == "#videos"){
        var owl = $(selector + " .owl-carousel").owlCarousel({
          loop: false,
          margin: 10,
          nav: false,
          items: 5,
          navText: false,
          dots: false,
          lazyLoad: true
        });
      }else{
        var owl = $(selector + " .owl-carousel").owlCarousel({
          loop: false,
          margin: 10,
          nav: false,
          items: 7,
          navText: false,
          dots: false,
          lazyLoad: true
        });
    
      }
      
      function toggleNavigationButtons() {
        var itemCount = $(selector + " .owl-carousel .owl-item").length;
        var visibleItems = owl.find('.owl-item.active').length;
  
        if (itemCount <= visibleItems) {
          $(selector + " .owl-next, " + selector + " .owl-prev").hide();
        } else {
          $(selector + " .owl-next, " + selector + " .owl-prev").show();
        }
      }
  
      
      toggleNavigationButtons();
  
      
      $(selector + " .owl-next").click(function() {
        owl.trigger("next.owl.carousel");
      });
      $(selector + " .owl-prev").click(function() {
        owl.trigger("prev.owl.carousel");
      });
    }
  
    
    initializeCarousel("#cast");
    initializeCarousel("#crew");
    initializeCarousel("#videos");
    initializeCarousel("#Recomendations");
    initializeCarousel("#season");
  });
  