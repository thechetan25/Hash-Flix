$(document).ready(function () {
    const myCarousel = document.getElementById("carouselExampleSlidesOnly");
    $(".indi img").eq(0).css({ filter: "brightness(100%)" });
    myCarousel.addEventListener("slide.bs.carousel", (event) => {
      $(".car_cont").css({ left: "0%", opacity: "0" }).animate(
        {
          left: "5%",
          opacity: "1",
        },
        1000
      );
  
      $(".crd").css({ bottom: "5%", opacity: "0" }).delay(250).animate(
        {
          bottom: "10%",
          opacity: "1",
        },
        800
      );
  
      var currentIndex = $(event.relatedTarget).index();
  
      $(".indi img").css({ filter: "brightness(50%)" });
      $(".indi img").removeClass("activef");
      $(".indi img").eq(currentIndex).addClass("activef");
      $(".indi img").eq(currentIndex).css({ filter: "brightness(100%)" });
    });
  
    $("#top_rated .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#top_rated .owl-next").click(function () {
      $("#top_rated .owl-carousel").trigger("next.owl.carousel");
    });
    $("#top_rated .owl-prev").click(function () {
      $("#top_rated .owl-carousel").trigger("prev.owl.carousel");
    });
  
    $("#people .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#people .owl-next").click(function () {
      $("#people .owl-carousel").trigger("next.owl.carousel");
    });
    $("#people .owl-prev").click(function () {
      $("#people .owl-carousel").trigger("prev.owl.carousel");
    });
  
    $("#upcomming .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#upcomming .owl-next").click(function () {
      $("#upcomming .owl-carousel").trigger("next.owl.carousel");
    });
    $("#upcomming .owl-prev").click(function () {
      $("#upcomming .owl-carousel").trigger("prev.owl.carousel");
    });
  
    $("#week_popular .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#week_popular .owl-next").click(function () {
      $("#week_popular .owl-carousel").trigger("next.owl.carousel");
    });
    $("#week_popular .owl-prev").click(function () {
      $("week_popular .owl-carousel").trigger("prev.owl.carousel");
    });
  
    $("#top_tv .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#top_tv .owl-next").click(function () {
      $("#top_tv .owl-carousel").trigger("next.owl.carousel");
    });
    $("#top_tv .owl-prev").click(function () {
      $("#top_tv .owl-carousel").trigger("prev.owl.carousel");
    });
  
    $("#all_trend .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#all_trend .owl-next").click(function () {
      $("#all_trend .owl-carousel").trigger("next.owl.carousel");
    });
    $("#all_trend .owl-prev").click(function () {
      $("#all_trend .owl-carousel").trigger("prev.owl.carousel");
    });
  
    $("#pop_show .owl-carousel").owlCarousel({
      loop: false,
      margin: 10,
      nav: false,
      items: 7,
      navText: false,
      dots: false,
      lazyLoad: true 
    });
    $("#pop_show .owl-next").click(function () {
      $("#pop_show .owl-carousel").trigger("next.owl.carousel");
    });
    $("#pop_show .owl-prev").click(function () {
      $("#pop_show .owl-carousel").trigger("prev.owl.carousel");
    });
  
  });
  