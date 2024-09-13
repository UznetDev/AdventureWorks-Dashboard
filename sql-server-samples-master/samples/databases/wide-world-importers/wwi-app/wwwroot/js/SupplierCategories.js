$(() => {
    var $table =
        $("#supplierCategories")
            .DataTable({
                "ajax": {
                    "url": "/OData/SupplierCategories",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "SupplierCategoryName" },
                    {
                        data: "SupplierCategoryID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        },
                        width: "100px"
                    },
                    {
                        data: "SupplierCategoryID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-danger btn-sm delete glyphicon glyphicon-trash"> Delete</button>';
                        },
                        width: "100px"
                    }
                ]
            });

    var $form = $("#EditForm");
    var $dlg = $("#modalDialog");

    $("button#add").on("click", e => $form[0].reset());

    $table.on("click", "button.edit",
        e => {
            $form[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('SupplierCategories')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the supplier category.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('SupplierCategories')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The supplier category is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the supplier category.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#SupplierCategoryID", $form).val();
            var model = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('SupplierCategories').find(id).put(model);
            } else {
                request = o('SupplierCategories').post(model);
            }

            request
                .save()
                .then(e => {
                    toastr.success('The supplier category is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the supplier category.'));
        }
    );
});