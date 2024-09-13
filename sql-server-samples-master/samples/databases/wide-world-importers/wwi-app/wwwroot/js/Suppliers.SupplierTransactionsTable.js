$(() => {
    $("#supplierTransactions")
        .DataTable({
            ajax: { url: "/OData/SupplierTransactions?$top=0", dataSrc: "value" },
            columns: [
                { data: "TransactionDate" },
                { data: "TransactionAmount", defaultContent: "" },
                { data: "IsFinalized", defaultContent: "" },
                { data: "SupplierName", defaultContent: "", visible: false },
                { data: "TransactionTypeName", defaultContent: "" },
                { data: "PaymentMethodName", defaultContent: "" },
                {
                    data: "SupplierTransactionID",
                    sortable: false,
                    searchable: false,
                    render: function (data) {
                        return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalSupplierTransactionDialog"> Edit</button>';
                    }
                }
            ]
        });
});