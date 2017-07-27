$(document).ready(function () {

    setup_change_course();
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


function setup_change_course() {
    $change_course = $('#change_course')

    $change_course
        .children('select')
        .change(function () {
            $change_course.submit()
        })
}