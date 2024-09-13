﻿$(() => {
    var $table =
        $("#customerCategories")
            .DataTable({
                "ajax": {
                    "url": "/OData/CustomerCategories",
                    "dataSrc": "value"
                },
                "columns": [
                    { data: "CustomerCategoryName" },
                    {
                        data: "CustomerCategoryID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        },
                        width: "100px"
                    },
                    {
                        data: "CustomerCategoryID",
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
            o('CustomerCategories')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the customer category.') );
        });

    $table.on("click", "button.delete",
        e => {
            var id = e.target.attributes["data-id"].value;
            o('CustomerCategories')
                .find(id).remove()
                .save()
                .then(model => {
                    toastr.success('The customer category is successfully deleted.');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to delete the customer category.'));
        });

    $("button#save").on("click",
        e => {
            var id = $("#CustomerCategoryID", $form).val();
            var model = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('CustomerCategories').find(id).put(model);
            } else {
                request = o('CustomerCategories').post(model);
            }

            request
                .save()
                .then(e => {
                    toastr.success('The customer category is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the customer category.'));
        }
    );
});