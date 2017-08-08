$(document).ready(function () {

    setup_datatables();

});


function setup_datatables(){
    $datatables = $('table.datatable');

    if($datatables.length){
        $datatables.DataTable({
            "paging": false,
            "info":   false
        });
    }
}