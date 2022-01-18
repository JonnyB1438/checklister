$(document).ready(function () {

    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log("Starting...");

    // Entry into the directory
    $(document).on("click", ".list", function(){
        console.log('Click! - ' + $(this).text());
        if ($(this).hasClass('delete')) {}
        else {
            console.log($(this).attr('value'))
            $.ajax({
                url: '',
                type: 'get',
                data: {
                    directory_id: $(this).attr('value'),
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

    // Enter into the parent directory
    $(document).on("click", ".parent_dir", function(){
        console.log('Click back! - ' + $(this).text());
        console.log($(this).attr('value'))
        $.ajax({
            url: '',
            type: 'get',
            data: {
                parent_id: $(this).attr('value'),
            },
            success: load_json_data,
            error: function(response) {location.reload();},
        });
    });

    //loading checklist information
    $(document).on("click", ".check_list", function(){
        console.log("Choosen checklist ID:" + $(this).attr('value'));
        $.ajax({
            url: '',
            type: 'get',
            data: {
                checklist_id: $(this).attr('value'),
            },
            success: load_checklist_data,
            error: function(response) {location.reload();},
        });
    });

    // creation a new directory into the current directory
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
                    current_directory_id: $(".parent_dir").attr('value'),
                    new_directory_name: dir_name,
                    csrfmiddlewaretoken: csrf,
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

    // creation a new checklist into the current directory
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
                    current_directory_id: $(".parent_dir").attr('value'),
                    new_checklist_name: checklist_name,
                    csrfmiddlewaretoken: csrf,
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

    // Entry into deletion mode and normal mode
    $(document).on("click", "#delete_mode", function(){
        console.log('Click Delete Mode!');
        console.log($(this).attr('value'));
        if ($(this).attr('value') == '0') {
            $(this).attr('value', '1');
            $(this).text('Set Normal Mode');
            $(this).removeClass("delete_mode")
            $(this).addClass("normal_mode")
            $(".list").addClass("delete")
            $(".check_list").addClass("delete")
            $(".adding").addClass("hide")
            $(".parent_dir").addClass("hide")
        }
        else {
            $(this).attr('value', '0');
            $(this).text('Set Delete Mode');
            $(this).removeClass("normal_mode")
            $(this).addClass("delete_mode")
            $(".list").removeClass("delete")
            $(".check_list").removeClass("delete")
            $(".adding").removeClass("hide")
            $(".parent_dir").removeClass("hide")
        };
    });

    // Deletion directory or checklist
    $(document).on("click", ".delete", function(){
        console.log("We will delete" + $(this).attr('innerHtml'));
        var dict = {};
        var element;
        dict['csrfmiddlewaretoken'] = csrf;
        if ($(this).hasClass('check_list')){
            dict['delete_checklist_id'] = $(this).attr('value');
        }
        else if ($(this).hasClass('list')){
            dict['delete_directory_id'] = $(this).attr('value');
        };
        console.log("Data for sending: " + dict);
        element = $(this);
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: element.fadeOut(),
            error: function(response) {location.reload();},
        });
    });

    $(document).on("click", "#add_string_btn", function(){
        console.log("Adding string...");
        new_string = $("#add_string_input").val();
        if (new_string) {
            console.log(new_string);
            $('#checklist_data').append('<div><input type="checkbox"><label>' + new_string + '</label></div>');
        }

    });

});

// load directory and checklist lists on the from ajax response
// response{'parent_directory{'id', 'name'}', 'directories{numeric:{'id', 'name'}}', 'checklists{numeric:{'id', 'name'}}'}
function load_json_data(response) {
    $("#list").empty();
    $("#check_list").empty();
    console.log('Path:' + response['parent_directory']['id'] +
                '; value: ' + response['parent_directory']['name']);
    $(".parent_dir").html(response['parent_directory']['name']);
    $(".parent_dir").attr('value', response['parent_directory']['id']);
    for (var key in response['directories']) {
        console.log('Directory:' + response['directories'][key]['id'] +
                    '; value: ' + response['directories'][key]['name']);
        $("#list").append('<li class="list" value="' + response['directories'][key]['id'] +
                          '">' + response['directories'][key]['name'] + '</li>');
    };
    for (var key in response['checklists']) {
            console.log('Checklist:' + response['checklists'][key]['id'] +
                        '; value: ' + response['checklists'][key]['name']);
            $("#check_list").append('<li class="check_list" value="' + response['checklists'][key]['id'] + '">' +
                                    response['checklists'][key]['name'] + '</li>');
    };
};

// load checklist data in .content block
// response{'id', 'name', 'data'}
function load_checklist_data(response) {
    $("#content").empty();
    console.log("Checklist data:" + response);
    $('#content').append('<h2 value="' + response['id'] + '">' + response['name'] + '</h2>');
    $('#content').append('<div id="checklist_data">' + response['data'] + '</div>');
    $('#content').append('<div id="add_string_div" class="adding"></div>');
    $('#add_string_div').append('<input type="text" id="add_string_input" value="" placeholder="Enter a new string...">');
    $('#add_string_div').append('<div id="add_string_btn" class="add_btn">Add</div>');
    $('#content').append('<div>Save checklist</div>');
};
