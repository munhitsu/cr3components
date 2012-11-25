jQuery( function($) {
    $('.inline-related.tabular .module table tbody:has(input[id$=sequence])').sortable({
        items: 'tr',
        update: function() {
            $(this).find('tr').each( function(i) {
                $(this).find('input[id$=sequence]').val(i+1);
            });
        }
    });
    $('.inline-related.tabular .module table tbody tr:has(input[id$=sequence])').css('cursor', 'move');
    $('.inline-related.tabular .module table tbody tr:has(input[id$=sequence])').find('input[id$=sequence]').hide();
    $('.inline-related.tabular .module table tbody tr:has(input[id$=sequence])').addClass( 'row1' ).removeClass('row2');
    $('.ui-sortable .add-row a[href]').click( function() {
        $('.inline-related.tabular .module table tbody tr:has(input[id$=sequence])').addClass( 'row1' ).removeClass('row2');
    });
});
