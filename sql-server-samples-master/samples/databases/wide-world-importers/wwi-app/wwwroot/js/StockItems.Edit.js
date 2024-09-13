$(() => {
    var $table = $("#stockItems").DataTable();
    var $form = $("#EditStockItemForm");
    var $dlg = $("#modalStockItemDialog");

    o('PackageTypes')
        .select('PackageTypeID,PackageTypeName')
        .get(packageTypes => {
            $("#UnitPackageID", $form).view(packageTypes);
            $("#OuterPackageID", $form).view(packageTypes);
        });

    o('Colors')
        .select('ColorID,ColorName')
        .get(colors => $("#ColorID", $form).view(colors));

    $table.on("click", "button.edit",
        e => {
            $form[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('StockItems')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the stock item.'));
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('StockItems')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The stock item is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the stock item.'));
        });

    $("button#save-stock-item").on("click",
        e => {
            var id = $("#StockItemID", $form).val();
            var state = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('StockItems').find(id).put(state);
            } else {
                request = o('StockItems').post(state);
            }

            request
                .save()
                .then(model => {
                    toastr.success('The stock item is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the stock item.'));
        }
    );
});