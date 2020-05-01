$(document).ready(function() {
    $("#new_category_form").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            $("#add_result").html("Added!");
            $("#add_result").fadeOut(3000);
            }
        });
    });


    $(".update_category_form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            var id = data["_id"];
            var category = data["category"];
            document.getElementById(id).getElementsByTagName("td")[0].innerText = category;
            }
        });
    });

    $(".delete_category_form").submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            var id = data["_id"];
            $('#' + id).remove();
            }
        });
    });
});

