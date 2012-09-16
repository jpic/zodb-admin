$(document).ready(function() {
    // CSRF security
    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var enableUi = function() {
        $('.tab-new').remove();
        $('.inner').tabs('destroy');
        var $tabs = $('.inner').tabs();

        $tabs.find( '.ui-tabs-nav' ).sortable({
            axis: 'x',
            handle: '.handle',
            items: 'li:not(.tab-new)',
        });

        $('.fieldset').sortable('destroy');
        $('.fieldset').sortable({
            forcePlaceholderSize: true,
            placeholder: 'ui-state-highlight',
            items: '.field',
            handle: '.handle',
            start: function (event, ui) {
                ui.placeholder.html('<tr><td colspan="5"></td></tr>');
            },
        });

        var $tab_items = $( 'ul.tab-list li:not(.tab-new)', $tabs ).droppable({
            accept: '.field',
            hoverClass: 'ui-state-hover',
            drop: function( event, ui ) {
                var $item = $( this );
                var $list = $( $item.find( 'a' ).attr( 'href' ) );

                ui.draggable.hide( 'slow', function() {
                    $tabs.tabs( 'select', $tab_items.index( $item ) );
                    $( this ).appendTo( $list ).show( 'slow' );
                });
            }
        });

        $('.enabled-form .tab-list').append(
            '<li class="tab-new ui-state-default ui-corner-top"><a id="tab-new">+</a></li>');
    };

    $('.field .add').live('click', function() {
        var name = '';
        var re = /^[a-z][a-z\d_]+$/;
        var error = false;
        while (name == '' || error) {
            message = "{% trans 'Please enter a codename for this field. It will be invisible and you will not be able to change it. It must be unique per form. It must start with a lowercase letter, and only have lowercase letters or numbers or underscores' %}";
            message = error ? error + "\n\n" + message : message;

            name = prompt(message);
            if (name == null) {
                return;
            }
            
            name = $.trim(name);
            if (!name.length)
                error = "{% trans 'Please provide a code name for this field' %}";
            else if ($('.name-' + name).length)
                error = "{% trans 'There is already a field with this code name in this form' %}";
            else if (!name.match(re))
                error = "{% trans 'The provided code name contains a forbidden character' %}";
            else
                error = null;
        }

        field = $(this).parents('.field').clone();
        var verbose_name = name.replace('_', ' ');
        verbose_name = verbose_name.charAt(0).toUpperCase() + verbose_name.substring(1)
        field.find('.verbose-name').html(verbose_name).attr('contenteditable', true).show();
        field.data('name', name);
        field.find('.help-text').show();
        field.find('.help-icon').show();
        field.find('.required').show();
        field.find('.remove').show();
        field.find('.add').remove();
        field.find('.handle').show();
        field.addClass('name-' + name);
        $('.ui-tabs-panel:visible .fieldset').append(field);
        
        enableUi();
    });

    $('.help-icon').live('click', function() {
        var helpText = $(this).parents('.field').find('.help-text');
        if (!$.trim(helpText.html())) {
            helpText.html('{% trans 'Your help text here ...' %}');
        }
    })

    $('#tab-new').live('click', function() {
        var id = 1;
        while ($('#tab-new-' + id).length > 0) {
            id = id + 1;
        }

        var html = ['<li class="ui-state-default ui-corner-top">'];
        html.push('<a href="#tab-new-' + id + '">');
        html.push('<span class="handle ui-icon ui-icon-arrow-2-e-w"></span>');
        html.push('<span contenteditable="true" class="name">{% trans 'New tab' %}</span>');
        html.push('<span class="remove ui-icon ui-icon-circle-close"></span>');
        html.push('</a></li>');
        $(this).parent().before(html.join(''));

        $(this).parents('.inner').append(
            '<div id="tab-new-' + id + '"><table class="fieldset"></table></div>');

        enableUi();

        $('a[href="#tab-new-' + id + '"]').click();
    });

    $('.field .remove').click(function() {
        $field = $(this).parents('.field');
        var message = "{% trans 'Are you sure you want to remove field' %} ";
        message += $field.find('.verbose-name').html();
        message += ' {% trans 'with field code' %}: ';
        message += '"' + $field.data('name') + '" ?';
        message += "\n{% trans 'You cannot undo this action, however, this will not delete the data associated with this field in existing objects. You can create a new field with the same code name when you want.' %}";
        message += "\n{% trans 'To confirm, type the code name of the field' %}";

        var doDelete = null;
        while (doDelete != $field.data('name')) {
            doDelete = prompt(message);
            if (doDelete == null) {
                return;
            }
        }

        $field.remove();
    });

    $('.tab-list .remove').click(function() {
        var name = $(this).parents('li').find('.name').html();
        var message = "{% trans 'Are you sure you want to delete tab' %}";
        message += ' "' + name + '"';
    });

    $('.save-form').click(function() {
        var seen = [];
        var duplicate = false;
        $('.form .tab-list li').each(function() {
            var name = $(this).find('.name').html();
            if (seen.indexOf(name) >= 0) {
                duplicate = name;
            }
            seen.push(name);
        });

        if (duplicate != false) {
            alert("{% trans 'Each tab must have a unique name. Please rename one of the tabs called:' %} '"+ duplicate +"'");
            return;
        }

        var formData = {
            'name': $('#form-name').html(),
            'tabs': [],
        };

        $('.fieldset').each(function() {
            var id = $(this).parents('.ui-tabs-panel').attr('id');
            var name = $('a[href="#'+id+'"] .name').html();

            var tab = {
                name: name,
                fields: [],
            };

            $(this).find('.field').each(function() {
                tab.fields.push({
                    name: $.trim($(this).data('name')),
                    kind: $.trim($(this).data('kind')),
                    help_text: $.trim($(this).find('.help-text').html()),
                    verbose_name: $.trim($(this).find('.verbose-name').html()),
                    required: $(this).find('.required input').attr('checked') ? true : false,
                });
            });

            formData.tabs.push(tab);
        });

        console.log(formData)
        $.post(document.location.href, {form: JSON.stringify(formData)});
    });

    enableUi();
});
