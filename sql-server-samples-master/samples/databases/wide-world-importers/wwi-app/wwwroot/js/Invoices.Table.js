$(() => {
    $("#invoices")
        .DataTable({
            ajax: "/Table/Invoices",
            serverSide: true,
            processing: true,
            columns: [
                { data: "InvoiceDate" },
                { data: "CustomerPurchaseOrderNumber", defaultContent: "" },
                { data: "CustomerName", defaultContent: "" },
                { data: "SalesPersonName", defaultContent: "" },
                { data: "ContactName", defaultContent: "" },
                { data: "ContactPhone", defaultContent: "" },
                {
                    data: "InvoiceID",
                    sortable: false,
                    searchable: false,
                    render: function (data) {
                        return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalInvoiceDialog"> Edit</button>';
                    }
                }
            ]
        });
});