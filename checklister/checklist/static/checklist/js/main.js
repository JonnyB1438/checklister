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
//        console.log($(this).attr('value'))
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
        if ($(this).hasClass('delete')) {}
        else {
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
        };
    });

    // creation a new directory into the current directory
    $(document).on("click", "#add_dir", function(){
        console.log('Click adding directory! - ' + $(this).text());
        let dir_name = $("#dir_name").val();
//        console.log(dir_name);
//        console.log(csrf);
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
//        console.log(checklist_name);
//        console.log(csrf);
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
//        console.log($(this).attr('value'));
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
        let dict = {};
        let element;
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

    //add checklist string on web-form
    $(document).on("click", "#add_string_btn", function(){
        console.log("Adding string...");
        let new_string = $("#add_string_input").val();
        if (new_string) {
            console.log(new_string);
            $('#checklist_data').append('<div><input type="checkbox"><label class="checkbox_label">' + new_string + '</label></div>');
            $("#add_string_input").val('');
        }
    });

    //save checklist
    $(document).on("click", "#save_checklist_btn", function(){
        console.log("Starting checklist saving...");
        let data = {}
        $("#checklist_data").children().each(function(index, element){
            data[index] = {'text': $('label', element).text(),
                         'status': $('input', element).is(':checked')};
        });
        $.ajax({
            url: '',
            type: 'post',
            data: {
               updated_checklist_id: $('h2', '#content').attr('value'),
                     checklist_name: $('h2', '#content').text(),
                     checklist_data: JSON.stringify(data),
                csrfmiddlewaretoken: csrf,
            },
            success: saved_checklist,
            error: function(response) {location.reload();},
        });
    });

    //choosing checklist string
    $(document).on("click", ".checkbox_label", function(){
        if ($(this).parent().hasClass('active')) {
            $(this).parent().removeClass('active');
            $('#editing_div').children().addClass('hide');
        }
        else {
            $("#checklist_data").children().removeClass('active');
            $(this).parent().addClass('active');
            $('#editing_div').children().removeClass('hide');
        };
    });

    //move checkbox string upper
    $(document).on("click", "#move_up_btn", function(){
        console.log("Move Up...");
        let previous = $('.active').prev();
        $('.active').insertBefore(previous);
    });

    //move checkbox string downer
    $(document).on("click", "#move_down_btn", function(){
        console.log("Move Down...");
        let next_one= $('.active').next();
        $('.active').insertAfter(next_one);
    });

    //edit checkbox string
    $(document).on("click", "#edit_label_btn", function(){
        console.log("Edit string...");

    });

    //delete checkbox string
    $(document).on("click", "#delete_label_btn", function(){
        console.log("Delete string...");
        $('.active').remove();
        $('#editing_div').children().addClass('hide');
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
    for (let key in response['directories']) {
        console.log('Directory:' + response['directories'][key]['id'] +
                    '; value: ' + response['directories'][key]['name']);
        $("#list").append('<li class="list" value="' + response['directories'][key]['id'] +
                          '">' + response['directories'][key]['name'] + '</li>');
    };
    for (let key in response['checklists']) {
            console.log('Checklist:' + response['checklists'][key]['id'] +
                        '; value: ' + response['checklists'][key]['name']);
            $("#check_list").append('<li class="check_list" value="' + response['checklists'][key]['id'] + '">' +
                                    response['checklists'][key]['name'] + '</li>');
    };
};

// load checklist data in .content block
// response{'id', 'name', 'data'}
function load_checklist_data(response) {
    let data;
    $("#content").empty();
    console.log("Checklist data:" + response);
    $('#content').append('<h2 value="' + response['id'] + '">' + response['name'] + '</h2>');
    $('#content').append('<div id="checklist_data"></div>');
    if (response['data']) {
        data = JSON.parse(response['data']);
    };
    console.log("Data: " + data);
    for (let key in data) {
//        console.log(key + ' = ' + data[key]);
//        console.log(data[key]['text'] + ' : ' + data[key]['status']);
        if (data[key]['status']) {
            $('#checklist_data').append('<div><input type="checkbox" checked><label class="checkbox_label">' + data[key]['text'] + '</label></div>');
        }
        else {
            $('#checklist_data').append('<div><input type="checkbox"><label class="checkbox_label">' + data[key]['text'] + '</label></div>');
        };
    };
    $('#content').append('<div id="editing_div">' +
                            '<div id="move_up_btn" class="button hide">Move Up</div>' +
                            '<div id="move_down_btn" class="button hide">Move Down</div>' +
                            '<div id="edit_label_btn" class="button hide">Edit String</div>' +
                            '<div id="delete_label_btn" class="button hide">Delete String</div>' +
                         '</div>');
    $('#content').append('<div id="add_string_div" class="adding"></div>');
    $('#add_string_div').append('<input type="text" id="add_string_input" value="" placeholder="Enter a new string...">');
    $('#add_string_div').append('<div id="add_string_btn" class="button">Add</div>');
    $('#content').append('<div id="save_checklist_btn" class="button">Save checklist</div>');
};

//actions after successful saving checklist
function saved_checklist(response) {
    console.log("checklist_saved");
};