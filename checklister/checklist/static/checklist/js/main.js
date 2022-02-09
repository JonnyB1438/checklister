var elementListDirectoryClassName = '.directory';
var menu_image = '/static/checklist/img/menu.webp'
var csrf;
var loaded_checklist;
var path_start = 'Path: ';

$(document).ready(function () {
    csrf = $("input[name=csrfmiddlewaretoken]").val();

    console.log("Starting...");

    //delete opened context menu
    $(document).mouseup(function(e) {
        let element = $(e.target);
        if (element.hasClass('edit_directory_name')) {
            edit_directory_name(element.attr('value'));
        }
        else if (element.hasClass('move_directory_up')) {
            move_directory_up(element.attr('value1'), element.attr('value2'));
        }
        else if (element.hasClass('move_directory_to')) {
            move_directory_to(element.attr('value1'), element.attr('value2'));
        }
        else if (element.hasClass('remove_directory')) {
            remove_directory(element.attr('value'));
        }
        else if (element.hasClass('edit_checklist_name')) {
            edit_checklist_name(element.attr('value'))
        }
        else if (element.hasClass('move_checklist_up')) {
            move_checklist_up(element.attr('value1'), element.attr('value2'))
        }
        else if (element.hasClass('move_checklist_to')) {
            move_checklist_to(element.attr('value1'), element.attr('value2'))
        }
        else if (element.hasClass('remove_checklist')) {
            remove_checklist(element.attr('value'))
        }
        else if ($('.editing').length > 0 && !$('.editing').is(e.target)) {
            console.log('Editing ID:' + $('.editing').attr('id'));
            end_editing($('.editing').attr('id'));
        };

        if (!$('.menu_img').is(e.target)) {
            $('.context-menu').remove();
        };
    });

    // Entry into the directory
    $(document).on("click", ".directory_name", function(){
        console.log('Click! - ' + $(this).text());
        $.ajax({
            url: '',
            type: 'get',
            data: {
                directory_id: $(this).attr('value'),
            },
            success: load_json_data,
            error: function(response) {location.reload();},
        });
    });

    // Entry into the parent directory
    $(document).on("click", ".parent_dir", function(){
        console.log('Click back! - ' + $(this).text());
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

    //loading checklist information
    $(document).on("click", ".checklist_name", function(){
        console.log("Choosen checklist ID:" + $(this).attr('value'));
        if (loaded_checklist && !(loaded_checklist == $('#content')[0].innerHTML)) {
            console.log('We needed to save current checklist!');
            save_checklist_data();
        };
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

    //add checklist string on web-form
    $(document).on("click", "#add_string_btn", function(){
        console.log("Adding string...");
        add_checklist_string();
    });

    //choosing checklist string
    $(document).on("click", ".checkbox_label", function(){
        if ($(this).parent().hasClass('active')) {
            $(this).parent().removeClass('active');
            $('#editing_div').addClass('hide');
        }
        else {
            $("#checklist_data").children().removeClass('active');
            $(this).parent().addClass('active');
            $('#editing_div').removeClass('hide');
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
        let label = $('.active .checkbox_label');
        label.addClass('hide');
        let editor = $('<input/>', { id: 'edit_string_input',
                                  class: 'flex_item editing',
                                   type: 'text'})
            .val(label.text());
        $(label).after(editor);
        editor.select();
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
        $('.context-menu').remove();
        let move_menu = '';
        let move_up = '';
        if ($(this).prev().is($('.directory_name'))) {
            let this_value = $(this).prev().attr('value')
            move_menu += '<li><p class="edit_directory_name" value="' + this_value + '">Edit name</p></li>';
            if ($('.parent_dir').text() != '/') {
                move_menu += '<li><p class="move_directory_up" value1="' + this_value +
                             '"value2="' + $('.parent_dir').attr('value') + '">Move one Level Up</p></li>';
            };
            $(this).parent().siblings().each(function(index, element) {
                if ($(element).is(':visible')) {
                    move_menu += '<li><p class="move_directory_to" value1="' + this_value +
                                 '" value2="' + $(element).children('.directory_name').attr('value') +
                                 '">Move to "' + $(element).children('.directory_name').text() + '"</p></li>';
                };
            });
            move_menu += '<li><p class="remove_directory" value="' + this_value + '">Remove</p></li>';
        }
        else if ($(this).prev().is($('.checklist_name'))) {
            let this_value = $(this).prev().attr('value')
            move_menu += '<li><p class="edit_checklist_name" value="' + this_value + '">Edit name</p></li>';
            if ($('.parent_dir').text() != '/') {
                move_menu += '<li><p class="move_checklist_up" value1="' + this_value +
                             '"value2="' + $('.parent_dir').attr('value') + '">Move one Level Up</p></li>';
            };
            $('.directory').each(function(index, element) {
                if ($(element).is(':visible')) {
                    move_menu += '<li><p class="move_checklist_to" value1="' + this_value +
                                '" value2="' + $(element).children('.directory_name').attr('value') +
                                '">Move to "' + $(element).children('.directory_name').text() + '"</p></li>';
                };
            });
            move_menu += '<li><p class="remove_checklist" value="' + $(this).prev().attr('value') + '">Remove</p></li>';
        };
        $('<div/>', {
                class: 'context-menu' // Присваиваем блоку наш css класс контекстного меню:
            })
            .css({right: $(document).width() - event.target.offsetLeft - event.target.width +'px', // Задаем позицию меню на X
                   top: event.target.offsetTop + event.target.width+'px' // Задаем позицию меню по Y
            })
            .appendTo('body') // Присоединяем наше меню к body документа:
            .append($('<ul/>').append(move_menu))
            .show('fast'); // Показываем меню с небольшим стандартным эффектом jQuery. Как раз очень хорошо подходит для меню
    });

    //pressing Enter handler for checklist changed name
    $(document).keyup(function(e) {
        if(e.key == "Enter") {
            console.log("Enter");
            console.log("ID=" + $(':focus').attr('id'));
            end_editing($(':focus').attr('id'));
        }
        else if(e.key == "Escape") {
            console.log("Enter");
            console.log("ID=" + $(':focus').attr('id'));
            end_editing($(':focus').attr('id'), false);
        };
    });

    //add or remove checkbox 'checked' parameter in html
    $(document).on('click', 'input[type="checkbox"]', function() {
	    if ($(this).is(':checked')){
	        $(this).attr('checked', 'checked');
	    }
	    else {
	        $(this).removeAttr('checked');
	    };
    });

    $(window).bind("beforeunload", function() {
        if (loaded_checklist && !(loaded_checklist == $('#content')[0].innerHTML)) {
            console.log('We needed to save current checklist!');
            save_checklist_data();
        };
//        return confirm("Do you really want to close?")
    });

});

//end editing when change cursor focus or press Enter
function end_editing(id, status=true) {
    if (id == 'checklist_name_editing') {
        let input = $('#'+id);
        let label = input.prev();
        if (status && input.val() && (input.val() != label.text())) {
            label.children('a').text(input.val());
            let checklist_id = label.attr('value');
            save_checklist(checklist_id, label.children('a').text(), "");
            if (checklist_id == $('h2', '#content').attr('value')) {
                $('h2', '#content').text(label.text());
            };
        };
        label.removeClass('hide');
        input.remove();
    }
    else if (id == 'directory_name_editing') {
        let input = $('#'+id);
        let label = input.prev();
        if (status && input.val() && (input.val() != label.text())) {
            directory_path = path_start + $('.parent_dir').text() + label.text() + '/';
            new_directory_path = path_start + $('.parent_dir').text() + input.val() + '/';
            checklist_path = $('#checklist_path').text();
            new_checklist_path = checklist_path.replace(directory_path, new_directory_path);
            label.text(input.val());
            save_directory_name(label.attr('value'));
            if (checklist_path.indexOf(directory_path) == 0) {
                $('#checklist_path').text(new_checklist_path);
            };
        }
        label.removeClass('hide');
        input.remove()
    }
    else if (id == 'edit_string_input') {
        let input = $('#'+id);
        let label = input.prev();
        if (status && input.val()) {
            label.text(input.val());
        }
        label.removeClass('hide');
        input.remove()
    }
    else if (id == 'add_string_input') {
        add_checklist_string();
    }
};

//add checklist string
function add_checklist_string() {
    let new_string = $("#add_string_input").val();
    if (new_string) {
        console.log(new_string);
        $('#checklist_data').append('<div class="flex_container"><input type="checkbox" class="checkbox flex_end_item"><label class="checkbox_label flex_item">' + new_string + '</label></div>');
        $("#add_string_input").val('');
    }
};

//Save checklist
function save_checklist(checklist_id, checklist_name, checklist_data) {
    console.log("Saving checklist with ID:" + checklist_id);
    $.ajax({
        url: '',
        type: 'post',
        data: {
             updated_checklist_id: checklist_id,
             checklist_name: checklist_name,
             checklist_data: checklist_data,
             csrfmiddlewaretoken: csrf,
        },
        error: function(response) {location.reload();},
    });
};

function save_checklist_data() {
        let data = {}
        $("#checklist_data").children().each(function(index, element){
            data[index] = {'text': $('label', element).text(),
                         'status': $('input', element).is(':checked')};
        });
        save_checklist($('h2', '#content').attr('value'), "", JSON.stringify(data))
};

//Save directory name
function save_directory_name(directory_id) {
    console.log("Saving directory name with ID:" + directory_id);
    $.ajax({
        url: '',
        type: 'post',
        data: {
             updated_directory_id: directory_id,
             directory_name: $('.directory_name[value="' + directory_id + '"]').text(),
             csrfmiddlewaretoken: csrf,
        },
        error: function(response) {location.reload();},
    });
};

// load directory and checklist lists on the from ajax response
// response{'parent_directory{'id', 'name'}', 'directories{numeric:{'id', 'name'}}', 'checklists{numeric:{'id', 'name'}}'}
function load_json_data(response) {
    $("#directory_list").empty();
    $("#checklist_list").empty();
    $(".parent_dir").html(response['parent_directory']['name'])
                    .attr('value', response['parent_directory']['id']);
    for (let key in response['directories']) {
        $("#directory_list").append('<div class="directory flex_container"><div class="directory_name flex_item" value="' +
                                    response['directories'][key]['id'] + '">' + response['directories'][key]['name'] +
                                    '</div><img class="menu_img flex_end_item" src="' + menu_image + '"></div>');
    };
    for (let key in response['checklists']) {
            $("#checklist_list").append('<div class="checklist flex_container"><div class="checklist_name flex_item" value="' + response['checklists'][key]['id'] + '">' +
                                    '<a href="#content">' + response['checklists'][key]['name'] + '</a></div><img class="menu_img flex_end_item" src="' + menu_image + '"></div>');
    };
};

// load checklist data in .content block
// response{'id', 'name', 'data'}
function load_checklist_data(response) {
    let data;
    $("#content").empty();
    $('#content').append('<p id="checklist_path">' + path_start + $('.parent_dir').text() + '</p>');
//    $('#content').append('<p id="checklist_path"></p>');
    $('#content').append('<h2 class="h2check" value="' + response['id'] + '">' + response['name'] + '</h2>')
                 .append('<div id="checklist_data"></div>');
    if (response['data']) {
        data = JSON.parse(response['data']);
    };
    for (let key in data) {
        if (data[key]['status']) {
            $('#checklist_data').append('<div class="flex_container"><input type="checkbox" class="checkbox flex_end_item" checked><label class="checkbox_label flex_item">' + data[key]['text'] + '</label></div>');
        }
        else {
            $('#checklist_data').append('<div class="flex_container"><input type="checkbox" class="checkbox flex_end_item"><label class="checkbox_label flex_item">' + data[key]['text'] + '</label></div>');
        };
    };
    $('#editing_div').addClass('hide');
    $('#add_string_div').removeClass('hide');
//    $('#save_checklist_btn').removeClass('hide');
    loaded_checklist = $('#content')[0].innerHTML;
};

//actions after successful saving checklist
function saved_checklist(response) {
    console.log("checklist_saved");
};

function edit_directory_name(directory_id) {
        console.log('Edit directory name with ID=' + directory_id);
        let element = $('.directory_name[value="' + directory_id + '"]');
        $(element).addClass('hide');
        let editor = $('<input/>', { id: 'directory_name_editing',
                                  class: 'flex_item editing'})
            .val(element.text());
        $(element).after(editor);
        editor.select();
};

function move_directory_up(directory_id, current_directory_id) {
        console.log('Move directory:' + directory_id + ' up into directory:' + current_directory_id);
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_directory_id'] = directory_id;
        dict['current_directory_id'] = current_directory_id;
        element = $('.directory_name[value="' + directory_id + '"]').parent();
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: function() {
                element.fadeOut();
                directory_path = path_start + $('.parent_dir').text() +
                                            $('.directory_name[value="' + directory_id + '"]').text() + '/';
                console.log('Path = ' + directory_path);
                if ($('#checklist_path').text().indexOf(directory_path) == 0) {
                    clear_checklist_data();
                };
            },
            error: function(response) {location.reload();},
        });
};

function move_directory_to(directory_id, target_directory_id) {
        console.log('Move directory:' + directory_id + ' to directory:' + target_directory_id);
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_directory_id'] = directory_id;
        dict['target_directory_id'] = target_directory_id;
        element = $('.directory_name[value="' + directory_id + '"]').parent();
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: function() {
                element.fadeOut();
                directory_path = path_start + $('.parent_dir').text() +
                                            $('.directory_name[value="' + directory_id + '"]').text() + '/';
                console.log('Path = ' + directory_path);
                if ($('#checklist_path').text().indexOf(directory_path) == 0) {
                    clear_checklist_data();
                };
            },
            error: function(response) {location.reload();},
        });
};

function remove_directory(directory_id) {
        console.log('Remove directory with ID=' + directory_id);
        let directory_name = $('.directory_name[value="' + directory_id + '"]').text();
        if (confirm('Are you sure you want to delete the directory("' + directory_name + '") with all its contents?')) {
            let dict = {};
            let element;
            dict['csrfmiddlewaretoken'] = csrf;
            dict['delete_directory_id'] = directory_id;
            element = $('.directory_name[value="' + directory_id + '"]').parent();
            $.ajax({
                url: '',
                type: 'post',
                data: dict,
                success: function() {
                    element.fadeOut();
                    directory_path = path_start + $('.parent_dir').text() +
                                            $('.directory_name[value="' + directory_id + '"]').text() + '/';
                    console.log('Path = ' + directory_path);
                    if ($('#checklist_path').text().indexOf(directory_path) == 0) {
                        clear_checklist_data();
                    };
                },
                error: function(response) {location.reload();},
            });
        };
};

function edit_checklist_name(checklist_id) {
        console.log('Edit checklist name with ID=' + checklist_id);
        let element = $('.checklist_name[value="' + checklist_id + '"]');
        $(element).addClass('hide');
        let editor = $('<input/>', { id: 'checklist_name_editing',
                                  class: 'flex_item editing'})
            .val(element.children('a').text());
        $(element).after(editor);
        editor.select();
};

function move_checklist_up(checklist_id, current_directory_id) {
        console.log('Move checklist:' + checklist_id + ' up into directory:' + current_directory_id);
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_checklist_id'] = checklist_id;
        dict['current_directory_id'] = current_directory_id;
        element = $('.checklist_name[value="' + checklist_id + '"]').parent();
        if (checklist_id == $('h2', '#content').attr('value')) {
            let path = $('#checklist_path').text();
            path = path.slice(0, -1);
            path = path.slice(0, path.lastIndexOf('/') + 1);
            $('#checklist_path').text(path);
        };
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: element.fadeOut(),
            error: function(response) {location.reload();},
        });
};

function move_checklist_to(checklist_id, target_directory_id) {
        console.log('Move checklist:' + checklist_id + ' to directory:' + target_directory_id);
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_checklist_id'] = checklist_id;
        dict['target_directory_id'] = target_directory_id;
        element = $('.checklist_name[value="' + checklist_id + '"]').parent();
        if (checklist_id == $('h2', '#content').attr('value')) {
            $('#checklist_path').append($('.directory_name[value="' + target_directory_id + '"').text() + '/');
        };
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: element.fadeOut(),
            error: function(response) {location.reload();},
        });
};

function remove_checklist(checklist_id) {
        console.log('Remove checklist with ID=' + checklist_id);
        let checklist_name = $('.checklist_name[value="' + checklist_id + '"]').text();
        if (confirm('Are you sure you want to delete the checklist("' + checklist_name + '")?')) {
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['delete_checklist_id'] = checklist_id;
        element = $('.checklist_name[value="' + checklist_id + '"]').parent();
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: function() {
                element.fadeOut();
                if (checklist_id == $('h2', '#content').attr('value')) {
                    clear_checklist_data();
                };
            },
            error: function(response) {location.reload();},
        });
        };
};

// clear loaded checklist data from DOM
function clear_checklist_data() {
    $('#content').empty();
    $('#editing_div').addClass('hide');
    $('#add_string_div').addClass('hide');
};
