$(() => {
    $("#supplierTransactions")
        .DataTable({
            ajax: "/Table/SupplierTransactions",
            serverSide: true,
            processing: true,
            columns: [
                { data: "TransactionDate" },
                { data: "TransactionAmount", defaultContent: "" },
                { data: "IsFinalized", defaultContent: "" },
                { data: "SupplierName", defaultContent: "" },
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