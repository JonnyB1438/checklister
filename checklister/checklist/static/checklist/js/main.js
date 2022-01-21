var elementListDirectoryClassName = '.directory';
var menu_image = '/static/checklist/img/menu.webp'

$(document).ready(function () {

    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log("Starting...");

    //delete opened context menu
    $(document).mouseup(function(e) {
        let menu_element = $('.menu_img');
        console.log("Menu element: " + menu_element);
        console.log("Target element: " + e.target);
        if (!menu_element.is(e.target)) {
            $('.context-menu').remove();
        };
    });

    // Entry into the directory
    $(document).on("click", ".directory_name", function(){
        console.log('Click! - ' + $(this).text());
        if ($(this).parent().hasClass('delete')) {}
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

    // creation a new directory into the current directory
    $(document).on("click", "#add_dir", function(){
        console.log('Click adding directory! - ' + $(this).text());
        let dir_name = $("#entered_name").val();
//        console.log(dir_name);
//        console.log(csrf);
        if (dir_name) {
            $("#entered_name").val("");
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
        var checklist_name = $("#entered_name").val();
        if (checklist_name) {
            $("#entered_name").val("");
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

//     open menu
//    $(document).on("click", ".menu_img", function() {
//        console.log("The menu is opening...")
//    });

    // Entry into deletion mode and normal mode
    $(document).on("click", "#delete_mode", function(){
        console.log('Click Delete Mode!');
//        console.log($(this).attr('value'));
        if ($(this).attr('value') == '0') {
            $(this).attr('value', '1');
            $(this).text('Set Normal Mode');
            $(this).removeClass("delete_mode")
            $(this).addClass("normal_mode")
            $(".directory").addClass("delete")
            $(".checklist").addClass("delete")
            $(".adding").addClass("hide")
            $(".parent_dir").addClass("hide")
            $(".menu_img").addClass("hide")
        }
        else {
            $(this).attr('value', '0');
            $(this).text('Set Delete Mode');
            $(this).removeClass("normal_mode")
            $(this).addClass("delete_mode")
            $(".directory").removeClass("delete")
            $(".checklist").removeClass("delete")
            $(".adding").removeClass("hide")
            $(".parent_dir").removeClass("hide")
            $(".menu_img").removeClass("hide")
        };
    });

    // Deletion directory or checklist (not tested)
    $(document).on("click", ".delete", function(){
        console.log("We will delete" + $(this).attr('innerHtml'));
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        if ($(this).hasClass('checklist')){
            dict['delete_checklist_id'] = $(this).children('.checklist_name').attr('value');
        }
        else if ($(this).hasClass('directory')){
            dict['delete_directory_id'] = $(this).children('.directory_name').attr('value');
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

    //loading checklist information
    $(document).on("click", ".checklist_name", function(){
        if ($(this).parent().hasClass('delete')) {}
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

    //add checklist string on web-form
    $(document).on("click", "#add_string_btn", function(){
        console.log("Adding string...");
        let new_string = $("#add_string_input").val();
        if (new_string) {
            console.log(new_string);
            $('#checklist_data').append('<div class="flex_container"><input type="checkbox" class="flex_end_item"><label class="checkbox_label flex_item">' + new_string + '</label></div>');
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
               updated_checklist_id: $('h2', '#content_block').attr('value'),
                     checklist_name: $('h2', '#content_block').text(),
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
        console.log($('.active .checkbox_label').text());
        let label = $('.active .checkbox_label');
        label.addClass('hide');
        $('.active').append('<input type=text id="edit_string_input" class="flex_item">');
        $('.active').append('<div class="flex_end_item" id="save_string_btn">Save</div>');
        $('#edit_string_input').val(label.text()).select();
    });

    //saving checkbox string changing
    $(document).on('click', '#save_string_btn', function(){
        console.log("Saving string...");
        $(this).remove();
        $('.active .checkbox_label').removeClass('hide').text($('#edit_string_input').val());
        $('#edit_string_input').remove();
    });

    //delete checkbox string
    $(document).on("click", "#delete_label_btn", function(){
        console.log("Delete string...");
        $('.active').remove();
        $('#editing_div').children().addClass('hide');
    });

 //adding menu on directory lists (not tested)
    $(document).on('click', '.menu_img', function(event) {
        console.log("OnClick menu img...");
        console.log("Event: " + event.target);
        console.log("Event: " + event.pageX);
        console.log("Event: " + event.pageY);
        $('.context-menu').remove();
        let move_menu = '';
        if ($('.parent_dir').text() != '/') {
            move_menu += '<li><a href="#" value="' + $('.parent_dir').attr('value') + '">Move one Level Up</a></li>';
        };
        if ($(this).prev().is($('.directory_name'))) {
            $(this).parent().siblings().each(function(index, element) {
                console.log("Printing dir index: " + index);
                move_menu += '<li><a href="#" value="' + $(element).children('.directory_name').attr('value') + '">Move to "' + $(element).children('.directory_name').text() + '"</a></li>';
            });
        }
        else if ($(this).prev().is($('.checklist_name'))) {
            $('.directory').each(function(index, element) {
                console.log("Printing checklist index: " + index);
                move_menu += '<li><a href="#" value="' + $(element).children('.directory_name').attr('value') + '">Move to "' + $(element).children('.directory_name').text() + '"</a></li>';
            });
        };
        console.log(event);
        $('<div/>', {
                class: 'context-menu' // Присваиваем блоку наш css класс контекстного меню:
            })
            .css({right: $(document).width() - event.target.offsetLeft - event.target.width +'px', // Задаем позицию меню на X
                   top: event.target.offsetTop + event.target.width+'px' // Задаем позицию меню по Y
            })
            .appendTo('body') // Присоединяем наше меню к body документа:
            .append($('<ul/>').append('<li><a href="#">Edit name</a></li>')
                              .append(move_menu)
                              .append('<li><a href="#">Remove</a></li>')
            )
            .show('fast'); // Показываем меню с небольшим стандартным эффектом jQuery. Как раз очень хорошо подходит для меню
    });

});

// load directory and checklist lists on the from ajax response
// response{'parent_directory{'id', 'name'}', 'directories{numeric:{'id', 'name'}}', 'checklists{numeric:{'id', 'name'}}'}
function load_json_data(response) {
    $("#directory_list").empty();
    $("#checklist_list").empty();
    console.log('Path:' + response['parent_directory']['id'] +
                '; value: ' + response['parent_directory']['name']);
    $(".parent_dir").html(response['parent_directory']['name'])
                    .attr('value', response['parent_directory']['id']);
    for (let key in response['directories']) {
        console.log('Directory:' + response['directories'][key]['id'] +
                    '; value: ' + response['directories'][key]['name']);
        $("#directory_list").append('<div class="directory flex_container"><div class="directory_name flex_item" value="' +
                                    response['directories'][key]['id'] + '">' + response['directories'][key]['name'] +
                                    '</div><img class="menu_img flex_end_item" src="' + menu_image + '"></div>');
    };
    for (let key in response['checklists']) {
            console.log('Checklist:' + response['checklists'][key]['id'] +
                        '; value: ' + response['checklists'][key]['name']);
            $("#checklist_list").append('<div class="checklist flex_container"><div class="checklist_name flex_item" value="' + response['checklists'][key]['id'] + '">' +
                                    response['checklists'][key]['name'] + '</div><img class="menu_img flex_end_item" src="' + menu_image + '"></div>');
    };
};

// load checklist data in .content block
// response{'id', 'name', 'data'}
function load_checklist_data(response) {
    let data;
    $("#content_block").empty();
    console.log("Checklist data:" + response);
    $('#content_block').append('<h2 value="' + response['id'] + '">' + response['name'] + '</h2>')
                 .append('<div id="checklist_data"></div>');
    if (response['data']) {
        data = JSON.parse(response['data']);
    };
    console.log("Data: " + data);
    for (let key in data) {
        if (data[key]['status']) {
            $('#checklist_data').append('<div class="flex_container"><input type="checkbox" class="flex_end_item" checked><label class="checkbox_label flex_item">' + data[key]['text'] + '</label></div>');
        }
        else {
            $('#checklist_data').append('<div class="flex_container"><input type="checkbox" class="flex_end_item"><label class="checkbox_label flex_item">' + data[key]['text'] + '</label></div>');
        };
    };
    $('#content_block').append('<div id="editing_div" class="flex_container">' +
                            '<div id="move_up_btn" class="flex_item button hide">Move Up</div>' +
                            '<div id="move_down_btn" class="flex_item button hide">Move Down</div>' +
                            '<div id="edit_label_btn" class="flex_item button hide">Edit String</div>' +
                            '<div id="delete_label_btn" class="flex_item button hide">Delete String</div>' +
                         '</div>');
    $('#content_block').append('<div id="add_string_div" class="flex_container adding"></div>');
    $('#add_string_div').append('<input type="text" id="add_string_input" class="flex_item" value="" placeholder="Enter a new string...">');
    $('#add_string_div').append('<div id="add_string_btn" class="flex_end_item button">Add</div>');
    $('#content_block').append('<div id="save_checklist_btn" class="button">Save checklist</div>');
};

//actions after successful saving checklist
function saved_checklist(response) {
    console.log("checklist_saved");
};