jQuery(function($) {
    $('.inline-related.tabular .module table tbody:has(input[id$=weight])').sortable({
        items: 'tr',
        update: function() {
            $(this).find('tr').each(function(i) {
                $(this).find('input[id$=weight]').val(i+1);
            });
        }
    });
    $('.inline-related.tabular .module table tbody tr:has(input[id$=weight])').css('cursor', 'move');
    $('.inline-related.tabular .module table tbody tr:has(input[id$=weight])').find('input[id$=weight]').hide();
    $('.inline-related.tabular .module table tbody tr:has(input[id$=weight])').addClass( 'row1' ).removeClass('row2')
});