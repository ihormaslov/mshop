(function () {
    var $menu = $('#menu ul');
    $('.navbar.main-menu').after('<div class="_toggleMenu"><a class="toggleMenu" href="#">- MENU -</a><ul class="nav"></ul></div>');
    $('._toggleMenu .nav').html($menu.html());
})();

var ww = document.body.clientWidth;

$(document).ready(function () {
    $("._toggleMenu .nav li a").each(function () {
        if ($(this).next().length > 0) {
            $(this).addClass("parent");
        }
        ;
    })

    $("._toggleMenu .toggleMenu").click(function (e) {
        e.preventDefault();
        $(this).toggleClass("active");
        $("._toggleMenu .nav").toggle();
    });
    adjustMenu();
})

$(window).bind('resize orientationchange', function () {
    ww = document.body.clientWidth;
    adjustMenu();
});

var adjustMenu = function () {
    if (ww < 767) {
        $("._toggleMenu").css("display", "block");
        if (!$(".toggleMenu").hasClass("active")) {
            $("._toggleMenu .nav").hide();
        } else {
            $("._toggleMenu .nav").show();
        }
        $("._toggleMenu .nav li").unbind('mouseenter mouseleave');
        $("._toggleMenu .nav li a.parent").unbind('click').bind('click', function (e) {
            // must be attached to anchor element to prevent bubbling
            e.preventDefault();
            $(this).parent("li").toggleClass("hover");
        });
    }
    else if (ww >= 767) {
        $("._toggleMenu").css("display", "none");
        $("._toggleMenu .nav").show();
        $("._toggleMenu .nav li").removeClass("hover");
        $("._toggleMenu .nav li a").unbind('click');
        $("._toggleMenu .nav li").unbind('mouseenter mouseleave').bind('mouseenter mouseleave', function () {
            // must be attached to li so that mouseleave is not triggered when hover over submenu
            $(this).toggleClass('hover');
        });
    }
}

//Menu
$('#menu > ul').superfish({
    delay: 100,
    animation: {opacity: 'show', height: 'show'},
    speed: 'fast',
    arrowClass: false,
    autoArrows: true
});
/*

 // ajax filtration
 $(document).ready(function () {
 $('#filter-form').submit(function () {
 var form = $(this),
 error = false

 var prod_container = $('#products-container')

 form.find('input').each(function () {
 if ($(this).attr('checked') == false) {
 error = true
 }
 })

 if (!error) {
 var data = form.serialize()

 $.ajax({
 type: 'POST',
 url: '',
 dataType: 'json',
 data: data,
 success: function (resp_data) {
 prod_container.empty()
 console.log(resp_data)
 for (var i = 0; i < Object.keys(resp_data).length; i++) {
 var item_title = resp_data[i].title,
 item_image = resp_data[i].image + '.270x270_q85_crop.jpg',
 item_price = resp_data[i].price,
 item_url = resp_data[i].item_url;


 */
/*if (resp_data[i].props.length) {
 var result = '',
 result_list = ''

 for (var y = 0; y < resp_data[i].props.length; y++) {
 var props = resp_data[i].props[y].prop__propName,
 propValues = resp_data[i].props[y].propValue,
 vals = ''

 vals = '<li>' + props + ': ' + propValues + '</li>'
 result_list = result_list + vals
 }
 result = '<p>Свойства товара</p>' +
 '<ul>'+
 '' + result_list + '' +
 ' </ul>'
 }*//*


 prod_container.append(
 '<li class="span3">'+
 '<div class="product-box">'+
 '<span class="sale_tag"></span>'+
 '<a href="' + item_url + '"><img alt="" src="/media/' + item_image + '"></a><br/>'+
 '<a href="' + item_url + '" class="title">' + item_title + '</a><br/>' +

 '<p class="price">' + item_price + ' грн</p>' +
 '</div>' +
 '</li>'
 */
/*                                '<div class="col-xs-2">'+
 '<a href="' + item_url + '"> <span>' + item_title + '</span>'+
 '<img src="/media/' + item_image + '" alt=""/></a>' +
 '<p>Цена ' + item_price + ' грн</p></div>'*//*

 )
 }
 },

 error: function (xhr, ajaxOptions, thrownError) {
 console.log('status', xhr.status);
 console.log('error', thrownError);
 }

 })
 }
 return false
 })
 })*/
