$(() => {
    var $table =
        $("#deals")
            .DataTable({
                "ajax": {
                    "url": "/OData/SpecialDeals",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "DealDescription", defaultContent: "" },
                    { data: "StartDate", defaultContent: "" },
                    { data: "EndDate", defaultContent: "" },
                    { data: "DiscountAmount", defaultContent: "" },
                    { data: "UnitPrice", defaultContent: "" },
                    { data: "BuyingGroupName", defaultContent: "" },
                    {
                        data: "SpecialDealID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        }
                    }
                ]
            });

    var $form = $("#EditForm");
    var $dlg = $("#modalDialog");

    o('CustomerCategories')
        .select('CustomerCategoryID,CustomerCategoryName')
        .get(categories => $("#CustomerCategoryID", $dlg).view(categories));

    o('BuyingGroups')
        .select('BuyingGroupID,BuyingGroupName')
        .get(buyingGroups => $("#BuyingGroupID", $dlg).view(buyingGroups));


    $("button#add").on("click", e => $form[0].reset());

    $table.on("click", "button.edit",
        e => {
            $form[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('SpecialDeals')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the special deal.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('SpecialDeals')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The special deal is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the special deal.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#SpecialDealID", $form).val();
            var state = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true, useNullAsEmptyString: true });

            o('SpecialDeals')
                .find(id)
                .put(state)
                .save()
                .then(model => {
                    $table.ajax.reload();
                    $dlg.modal('hide');
                    $form[0].reset();
                    toastr.success('The deal is successfully saved.');
                })
                .fail(e =>
                    toastr.error('An error occured while trying to save the deal.')
                );
        }
    );

    $("button#cancel").on("click", e => $dlg.modal('hide') );
});