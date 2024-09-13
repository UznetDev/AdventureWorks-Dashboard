var TODAY = new Date();
var ONE_DAY = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
var DIFF_DAYS = Math.round(Math.abs((TODAY.getTime() - (new Date("2016-05-01T00:00:00.0000Z")).getTime()) / ONE_DAY));

$(function () {
    $("#slider").slider({
        value: 0,
        min: -DIFF_DAYS,
        max: 0,
        slide: function (event, ui) {

            var d = new Date();
            var $dt = $("table.temporal").DataTable();
            if (ui.value === 0) {
                $("table.temporal").data("$systemat", null);
                $("table.temporal").DataTable().ajax.reload();
            } else {
                d.setDate(d.getDate() + ui.value);
                $("table.temporal").data("$systemat", d.toISOString());
                $("table.temporal").DataTable().ajax.reload();
            }
            $("#snapshot").val(d.toISOString().split('T')[0]);
        }
    });
    $("#snapshot").change(e => {
        var d = new Date(e.currentTarget.value);
        var now = new Date();
        var diff = (now.getTime() - d.getTime()) / ONE_DAY;
        if (diff < 0) {
            toastr.warning('Cannot go to the future');
            e.preventDefault();
            $("table.temporal").data("$systemat", null);
            $("table.temporal").DataTable().ajax.reload();
            return false;
        } else {
            $("#slider").slider('value', - diff);
            $("table.temporal").data("$systemat", d.toISOString());
            $("table.temporal").DataTable().ajax.reload();
        }
    });
});
