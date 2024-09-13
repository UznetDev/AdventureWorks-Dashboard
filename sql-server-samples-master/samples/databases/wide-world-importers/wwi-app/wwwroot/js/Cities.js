$(() => {
    var $table =
        $("#cities")
            .DataTable({
                serverSide: true,
                processing: true,
                ajax: {
                    url: "/Table/Cities",
                    data: function (d) {
                        if ($("#cities").data("$systemat") !== null)
                            d.$systemat = $("#cities").data("$systemat");
                    }
                },
                columns: [
                    { data: "CityName" },
                    { data: "LatestRecordedPopulation", type: "numeric", defaultContent: "" },
                    { data: "StateProvinceName", defaultContent: "" },
                    {
                        data: "CityID",
                        "sortable": false,
                        "searchable": false,
                        "render": function (data) {
                            return '<button data-id="' + data + '" class="btn btn-primary btn-sm edit glyphicon glyphicon-edit" data-toggle="modal" data-target="#modalDialog"> Edit</button>';
                        },
                        width: "100px"
                    },
                    {
                        data: "CityID",
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

    o('StateProvinces')
        .select('StateProvinceID,StateProvinceName')
        .get(provinces => $("#StateProvinceID",$form).view(provinces) );

    $("button#add").on("click", e => $form[0].reset());

    $table.on("click", "button.edit",
        e => {
            $form[0].reset();
            var id = e.target.attributes["data-id"].value;
            o('Cities')
                .find(id)
                .get()
                .then(model => $form.view(model.data))
                .fail(e => toastr.error('An error occured while trying to get the city.') );
        });

    $table.on("click", "button.delete",
        e => {
            try {
                var id = e.target.attributes["data-id"].value;
                o('Cities')
                    .find(id).remove()
                    .save()
                    .then(model => {
                        toastr.success('The city is successfully deleted.');
                        $table.ajax.reload();
                    })
                    .fail(e => toastr.error('An error occured while trying to delete the city.'));
            } catch (ex) {
                alert(ex);
            }
        });

    $("button#save").on("click",
        e => {
            var id = $("#CityID", $form).val();
            var city = $form.serializeJSON({ checkboxUncheckedValue: "false", parseAll: true });
            var request;
            if (id) {
                request = o('Cities').find(id).put(city);
            } else {
                request = o('Cities').post(city);
            }

            request
                .save()
                .then(model => {
                    toastr.success('The city is successfully saved.');
                    $dlg.modal('hide');
                    $table.ajax.reload();
                })
                .fail(e => toastr.error('An error occured while trying to save the city.'));
        }
    );
});