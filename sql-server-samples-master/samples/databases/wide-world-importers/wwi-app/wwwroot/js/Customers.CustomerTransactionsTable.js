$(() => {
    $("#customerTransactions")
        .DataTable({
            ajax: {
                url: "/OData/CustomerTransactions?$top=0",
                dataSrc: "value"
            },
            columns: [
                { data: "TransactionDate" },
                { data: "TransactionAmount", defaultContent: "" },
                { data: "IsFinalized", defaultContent: "" },
                { data: "CustomerName", defaultContent: "", visible: false },
                { data: "TransactionTypeName", defaultContent: "" },
                { data: "PaymentMethodName", defaultContent: "" },
                {
                    data: "CustomerTransactionID",
                    sortable: false,
                    searchable: false,
                    render: function (data) {
                        return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalCustomerTransactionDialog"> Edit</button>';
                    },
                    width: "100px"

                }
            ]
        });
});