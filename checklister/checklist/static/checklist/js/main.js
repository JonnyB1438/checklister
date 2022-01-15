$(document).ready(function () {

    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log("Starting...");

    $(document).on("click", ".list", function(){
        console.log('Click!' + $(this).text());
        console.log($(this).attr('value'))
        $.ajax({
            url: '',
            type: 'get',
            data: {
                element_id: $(this).attr('value'),
            },
            success: load_json_data,
            error: function(response) {location.reload();},
        });
    });

    $(document).on("click", "#parent_dir", function(){
        console.log('Click back! - ' + $(this).text());
        console.log($(this).attr('value'))
        $.ajax({
            url: '',
            type: 'get',
            data: {
                element_id: $(this).attr('value'),
                go_level_up: 1,
            },
            success: load_json_data,
            error: function(response) {location.reload();},
        });
    });

    $(document).on("click", "#add_dir", function(){
        console.log('Click adding directory! - ' + $(this).text());
        var dir_name = $("#dir_name").val();
        console.log(dir_name);
        console.log(csrf);
        if (dir_name) {
            $("#dir_name").val("");
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    current_directory_id: $("#parent_dir").attr('value'),
                    new_directory_name: dir_name,
                    csrfmiddlewaretoken: csrf,
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

    $(document).on("click", "#add_checklist", function(){
        console.log('Click adding checklist!');
        var checklist_name = $("#checklist_name").val();
        console.log(checklist_name);
        console.log(csrf);
        if (checklist_name) {
            $("#checklist_name").val("");
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    current_directory_id: $("#parent_dir").attr('value'),
                    new_checklist_name: checklist_name,
                    csrfmiddlewaretoken: csrf,
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

});

function load_json_data(response) {
    $("#list").empty();
    for (var key in response) {
        if (key == 0) {
            console.log('Path:' + response[key]['id'] + '; value: ' + response[key]['name']);
            $("#parent_dir").html(response[key]['name']);
            $("#parent_dir").attr('value', response[key]['id']);
        }
        else {
            console.log('String:' + response[key]['id'] + '; value: ' + response[key]['name']);
            $("#list").append('<li class="list" value="' + response[key]['id'] + '">' + response[key]['name'] + '</li>');
        };
    };
};
