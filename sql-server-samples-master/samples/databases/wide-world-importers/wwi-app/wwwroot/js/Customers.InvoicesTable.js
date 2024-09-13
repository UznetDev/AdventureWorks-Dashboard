$(() => {
    $("#invoices")
        .DataTable({
            ajax: {
                url: "/OData/Invoices?$top=0",
                dataSrc: "value"
            },
            columns: [
                { data: "InvoiceDate" },
                { data: "CustomerPurchaseOrderNumber", defaultContent: "" },
                { data: "CustomerName", defaultContent: "", visible: false },
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