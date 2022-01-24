function toDataTable(id) {
    $("#" + id).DataTable({
        aaSorting: [],
        paging: true,
        pagingType: "simple_numbers",
        pageLength: 25,
        scrollX: true,
        sScrollX: "100%",
    });
}

function redirectTo(id) {
    window.location = id
}