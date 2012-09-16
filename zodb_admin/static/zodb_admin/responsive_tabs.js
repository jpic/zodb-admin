function cookie_tab() {
    if ($.cookie != undefined) {
        // if path is /admin/art/artwork/add/ or /admin/art/artwork/1234/
        // then path should be just /admin/art/artwork
        var path = document.location.pathname.split('/').slice(0, -2).join('/');

        // jquery cookie plugin enabled
        $('input[name=_continue]').click(function() {
            $.cookie(
                'current_tab', 
                AdminHack.tabs.find('li.active').attr('class').match(/[a-z-]+_tab/)[0],
                {
                    path: path, 
                    expires: 1
                }
            );
        });
        $('input[name=_save], input[name=_addanother], a').click(function() {
            $.cookie('current_tab', null, { expires: -1, path: path });
        });
    }
}

function setup() {
    function enableAccordeon() {
        $('.responsive_tabs:not(.accordeon)').hide();
        $('.responsive_tabs.accordeon').show();
    }

    function enableTabs() {
        $('.responsive_tabs:not(.accordeon)').show();
        $('.responsive_tabs.accordeon').hide();
    }

    $(window).width() <= 760 ? enableAccordeon() : enableTabs();
}

$(document).ready(function() {
    // if path is /admin/art/artwork/add/ or /admin/art/artwork/1234/
    // then path should be just /admin/art/artwork
    var path = document.location.pathname.split('/').slice(0, -2).join('/');
    var path = document.location.pathname;


    $('.responsive_tabs li a').click(function() {
        var li = $(this).parent();
        
        if (li.is('.active')) {
            return;
        }

        $('[data-tab-name]:not([data-tab-name="'+li.data('tab-name')+'"])').removeClass('active');
        $('[data-tab-name]:not([data-tab-name="'+li.data('tab-name')+'"]):not(li)').hide();

        $.cookie('current_tab', li.data('tab-name'), { path: path, expires: 1 });
        li.addClass('active');
        $('[data-tab-name="'+li.data('tab-name')+'"]').show();
    });

    $(window).resize(setup);

    $('fieldset').each(function() {
        $(this).attr('data-tab-name', $(this).find('legend').html());
    });

    setup();
    $('.responsive_tabs:first li:first a').click();
});
