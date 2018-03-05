

$(document).ready(function(){
    var $drops = $('.drop');


    $('.sidebar').on('click', 'a.drop', function(e){
        $this = $(e.target);
        if($this.hasClass('rotate'))
            $open = $this;
        else
            $open = $this.find('.rotate');

        $open.toggleClass('open');
        console.log("clicked");
        console.log($(this));
    });

    $(document).on('click', function(){
        $drops.removeClass('open');
    });
});

