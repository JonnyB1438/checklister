var menu_image = '/static/checklist/img/menu.png'
var csrf;
var loaded_checklist;
var path_start = 'Path: ';

var classMenuEditDirectoryName = 'edit_directory_name';
var classMenuMoveDirectoryUp = 'move_directory_up';
var classMenuMoveDirectoryTo = 'move_directory_to';
var classMenuRemoveDirectory = 'remove_directory';
var classMenuEditChecklistName = 'edit_checklist_name';
var classMenuMoveChecklistUp = 'move_checklist_up';
var classMenuMoveChecklistTo = 'move_checklist_to';
var classMenuRemoveChecklist = 'remove_checklist';

var classParentDirectory = '.parent_directory';
var classParentDirectoryLabel = '.parent_dir';
var classDirectory = '.directory';
var classDirectoryLabel = '.directory_name';
var classChecklist = '.checklist';
var classChecklistLabel = '.checklist_name';
var classCheckbox = '.checkbox';
var classCheckboxLabel = '.checkbox_label';

var classElementEditor = '.editing';
var classContextMenu = '.context-menu';
var classContextMenuIcon = '.menu_img';

var idAddDirectoryButton = '#add_dir';
var idAddChecklistButton = '#add_checklist';
var idEnteredNameInput = '#entered_name';
var idAddNewCheckboxBlock = '#add_string_div';
var idAddNewCheckboxButton = '#add_string_btn';
var idAddNewCheckboxInput = '#add_string_input';
var idContentBlock = '#content_block';
var idChecklistContentBlock = '#content';
var idChecklistData = '#checklist_data';
var idCheckboxEditorBlock = '#editing_div';
var idMoveCheckboxUpButton = '#move_up_btn';
var idMoveCheckboxDownButton = '#move_down_btn';
var idEditCheckboxButton = '#edit_label_btn';
var idDeleteCheckboxButton = '#delete_label_btn';
var idCheckboxEditorInput = '#edit_string_input';
var idDirectoryEditorInput = '#directory_name_editing';
var idChecklistEditorInput = '#checklist_name_editing';
var idChecklistPathLabel = '#checklist_path';
var idDirectoryList = '#directory_list';
var idChecklistList = '#checklist_list';

var classActiveElement = '.active';
var classHideElement = '.hide';

var classFlexContainer = 'flex_container';
var classFlexItem = 'flex_item';
var classFlexEndItem = 'flex_end_item';
var classH2Header = '.h2check';

$(document).ready(function () {
    csrf = $("input[name=csrfmiddlewaretoken]").val();

    //delete opened context menu
    $(document).mouseup(function(e) {
        let element = $(e.target);
        if (element.hasClass(classMenuEditDirectoryName)) {
            edit_directory_name(element.attr('value'));
        }
        else if (element.hasClass(classMenuMoveDirectoryUp)) {
            move_directory_up(element.attr('value1'), element.attr('value2'));
        }
        else if (element.hasClass(classMenuMoveDirectoryTo)) {
            move_directory_to(element.attr('value1'), element.attr('value2'));
        }
        else if (element.hasClass(classMenuRemoveDirectory)) {
            remove_directory(element.attr('value'));
        }
        else if (element.hasClass(classMenuEditChecklistName)) {
            edit_checklist_name(element.attr('value'))
        }
        else if (element.hasClass(classMenuMoveChecklistUp)) {
            move_checklist_up(element.attr('value1'), element.attr('value2'))
        }
        else if (element.hasClass(classMenuMoveChecklistTo)) {
            move_checklist_to(element.attr('value1'), element.attr('value2'))
        }
        else if (element.hasClass(classMenuRemoveChecklist)) {
            remove_checklist(element.attr('value'))
        }
        else if ($(classElementEditor).length > 0 && !$(classElementEditor).is(e.target)) {
            end_editing($(classElementEditor).attr('id'));
        };

        if (!$(classContextMenuIcon).is(e.target)) {
            $(classContextMenu).remove();
        };
    });

    // Entry into the directory
    $(document).on("click", classDirectoryLabel, function(){
        $.ajax({
            url: '',
            type: 'get',
            data: { directory_id: $(this).attr('value'),},
            success: load_json_data,
            error: function(response) {location.reload();},
        });
    });

    // Entry into the parent directory
    $(document).on("click", classParentDirectory, function(){
        $.ajax({
            url: '',
            type: 'get',
            data: { parent_id: $(this).children(classParentDirectoryLabel).attr('value'),},
            success: load_json_data,
            error: function(response) {location.reload();},
        });
    });

    // creation a new directory into the current directory
    $(document).on("click", idAddDirectoryButton, function(){
        let dir_name = $(idEnteredNameInput).val();
        if (dir_name) {
            $(idEnteredNameInput).val("");
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    current_directory_id: $(classParentDirectoryLabel).attr('value'),
                    new_directory_name: dir_name,
                    csrfmiddlewaretoken: csrf,
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

    // creation a new checklist into the current directory
    $(document).on("click", idAddChecklistButton, function(){
        var checklist_name = $(idEnteredNameInput).val();
        if (checklist_name) {
            $(idEnteredNameInput).val("");
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    current_directory_id: $(classParentDirectoryLabel).attr('value'),
                    new_checklist_name: checklist_name,
                    csrfmiddlewaretoken: csrf,
                },
                success: load_json_data,
                error: function(response) {location.reload();},
            });
        };
    });

    //loading checklist information
    $(document).on("click", classChecklistLabel, function(){
        if (loaded_checklist && !(loaded_checklist == $(idChecklistContentBlock)[0].innerHTML)) {
            save_checklist_data();
        };
        $.ajax({
            url: '',
            type: 'get',
            data: { checklist_id: $(this).attr('value'), },
            success: load_checklist_data,
            error: function(response) {location.reload();},
        });
    });

    //add checklist string on web-form
    $(document).on("click", idAddNewCheckboxButton, function(){
        add_checklist_string();
        $(idAddNewCheckboxInput).focus();
    });

    //choosing checklist string
    $(document).on("click", classCheckboxLabel, function(){
        if ($(this).parent().hasClass(classActiveElement.slice(1))) {
            $(this).parent().removeClass(classActiveElement.slice(1));
            $(idCheckboxEditorBlock).addClass(classHideElement.slice(1));
        }
        else {
            $(idChecklistData).children().removeClass(classActiveElement.slice(1));
            $(this).parent().addClass(classActiveElement.slice(1));
            $(idCheckboxEditorBlock).removeClass(classHideElement.slice(1));
        };
    });

    //move checkbox string upper
    $(document).on("click", idMoveCheckboxUpButton, function(){
        let previous = $(classActiveElement).prev();
        $(classActiveElement).insertBefore(previous);
    });

    //move checkbox string downer
    $(document).on("click", idMoveCheckboxDownButton, function(){
        let next_one= $(classActiveElement).next();
        $(classActiveElement).insertAfter(next_one);
    });

    //edit checkbox string
    $(document).on("click", idEditCheckboxButton, function(){
        let label = $(classActiveElement + ' ' + classCheckboxLabel);
        label.addClass(classHideElement.slice(1));
        let editor = $('<input/>', {id: idCheckboxEditorInput.slice(1),
                                    class: classElementEditor.slice(1),
                                    addClass: classFlexItem,
                                    type: 'text'})
            .val(label.text());
        $(label).after(editor);
        editor.select();
    });

    //delete checkbox string
    $(document).on("click", idDeleteCheckboxButton, function(){
        $(classActiveElement).remove();
        $(idCheckboxEditorBlock).addClass(classHideElement.slice(1));
    });

 //adding menu on directory lists
    $(document).on('click', classContextMenuIcon, function(event) {
        $(classContextMenu).remove();
        let move_menu = [];
        let move_up = '';
        if ($(this).prev().is($(classDirectoryLabel))) {
            let this_value = $(this).prev().attr('value')
            move_menu.push($('<li/>').append($('<p/>', {class: classMenuEditDirectoryName,
                                                    value: this_value})
                                                    .append('Edit name')));
            if ($(classParentDirectoryLabel).text() != '/') {
                move_menu.push($('<li/>').append($('<p/>', {class: classMenuMoveDirectoryUp,
                                                            value1: this_value,
                                                            value2: $(classParentDirectoryLabel).attr('value')})
                                                            .append('Move one Level Up')));
            };
            $(this).parent().siblings().each(function(index, element) {
                if ($(element).is(':visible')) {
                    move_menu.push($('<li/>')
                        .append($('<p/>', {class: classMenuMoveDirectoryTo,
                                           value1: this_value,
                                           value2: $(element).children(classDirectoryLabel).attr('value')})
                                           .append('Move to "' + $(element).children(classDirectoryLabel).text() + '"')));
                };
            });
            move_menu.push($('<li/>').append($('<p/>', {class: classMenuRemoveDirectory,
                                                        value: this_value})
                                                        .append('Remove')));
        }
        else if ($(this).prev().is($(classChecklistLabel))) {
            let this_value = $(this).prev().attr('value')
            move_menu.push($('<li/>').append($('<p/>', {class: classMenuEditChecklistName,
                                                        value: this_value})
                                                        .append('Edit name')));
            if ($(classParentDirectoryLabel).text() != '/') {
                move_menu.push($('<li/>').append($('<p/>', {class: classMenuMoveChecklistUp,
                                                            value1: this_value,
                                                            value2: $(classParentDirectoryLabel).attr('value')})
                                                            .append('Move one Level Up')));
            };
            $(classDirectory).each(function(index, element) {
                if ($(element).is(':visible')) {
                    move_menu.push($('<li/>')
                        .append($('<p/>', {class: classMenuMoveChecklistTo,
                                           value1: this_value,
                                           value2: $(element).children(classDirectoryLabel).attr('value')})
                                           .append('Move to "' + $(element).children(classDirectoryLabel).text() + '"')));
                };
            });
            move_menu.push($('<li/>').append($('<p/>', {class: classMenuRemoveChecklist,
                                                        value: $(this).prev().attr('value')})
                                                        .append('Remove')));
        };
        $('<div/>', {class: classContextMenu.slice(1)})
            .css({right: $(document).width() - event.target.offsetLeft - event.target.width +'px',
                   top: event.target.offsetTop + event.target.width+'px'
            })
            .appendTo('body')
            .append($('<ul/>').append(move_menu))
            .show('fast');
    });

    //pressing Enter handler for checklist changed name
    $(document).keyup(function(e) {
        if(e.key == "Enter") {
            end_editing($(':focus').attr('id'));
        }
        else if(e.key == "Escape") {
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
        if (loaded_checklist && !(loaded_checklist == $(idChecklistContentBlock)[0].innerHTML)) {
            save_checklist_data();
        };
    });

});

//end editing when change cursor focus or press Enter
function end_editing(id, status=true) {
    if (id == idChecklistEditorInput.slice(1)) {
        let input = $('#'+id);
        let label = input.prev();
        if (status && input.val() && (input.val() != label.text())) {
            label.text(input.val());
            let checklist_id = label.attr('value');
            save_checklist(checklist_id, label.text(), "");
            if (checklist_id == $(classH2Header, idChecklistContentBlock).attr('value')) {
                $(classH2Header, idChecklistContentBlock).text(label.text());
            };
        };
        label.removeClass(classHideElement.slice(1));
        input.remove();
    }
    else if (id == idDirectoryEditorInput.slice(1)) {
        let input = $('#'+id);
        let label = input.prev();
        if (status && input.val() && (input.val() != label.text())) {
            directory_path = path_start + $(classParentDirectoryLabel).text() + label.text() + '/';
            new_directory_path = path_start + $(classParentDirectoryLabel).text() + input.val() + '/';
            checklist_path = $(idChecklistPathLabel).text();
            new_checklist_path = checklist_path.replace(directory_path, new_directory_path);
            label.text(input.val());
            save_directory_name(label.attr('value'));
            if (checklist_path.indexOf(directory_path) == 0) {
                $(idChecklistPathLabel).text(new_checklist_path);
            };
        }
        label.removeClass(classHideElement.slice(1));
        input.remove()
    }
    else if (id == idCheckboxEditorInput.slice(1)) {
        let input = $('#'+id);
        let label = input.prev();
        if (status && input.val()) {
            label.text(input.val());
        }
        label.removeClass(classHideElement.slice(1));
        input.remove()
    }
    else if (id == idAddNewCheckboxInput.slice(1)) {
        add_checklist_string();
    }
};

//add checklist string
function add_checklist_string() {
    let new_string = $(idAddNewCheckboxInput).val();
    if (new_string) {
        $(idChecklistData).append($('<div>', {class: classFlexContainer})
                                .append($('<input>', {type: "checkbox",
                                                      class: classCheckbox.slice(1),
                                                      addClass: classFlexEndItem}))
                                .append($('<label>', {class: classCheckboxLabel.slice(1),
                                                      addClass: classFlexItem})
                                    .append(new_string)));
        $(idAddNewCheckboxInput).val('');
    }
};

//Save checklist
function save_checklist(checklist_id, checklist_name, checklist_data) {
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
        let data = {};
        $(idChecklistData).children().each(function(index, element){
            data[index] = {'text': $('label', element).text(),
                         'status': $('input', element).is(':checked')};
        });
        save_checklist($(classH2Header, idChecklistContentBlock).attr('value'), "", JSON.stringify(data));
};

//Save directory name
function save_directory_name(directory_id) {
    $.ajax({
        url: '',
        type: 'post',
        data: {
             updated_directory_id: directory_id,
             directory_name: $(classDirectoryLabel +  '[value="' + directory_id + '"]').text(),
             csrfmiddlewaretoken: csrf,
        },
        error: function(response) {location.reload();},
    });
};

// load directory and checklist lists on the from ajax response
// response{'parent_directory{'id', 'name'}', 'directories{numeric:{'id', 'name'}}', 'checklists{numeric:{'id', 'name'}}'}
function load_json_data(response) {
    $(idDirectoryList).empty();
    $(idChecklistList).empty();
    $(classParentDirectoryLabel).html(response['parent_directory']['name'])
                    .attr('value', response['parent_directory']['id']);
    for (let key in response['directories']) {
        $(idDirectoryList).append($('<div>', {class: classDirectory.slice(1),
                                                addClass: classFlexContainer})
                                .append($('<div>', {class: classDirectoryLabel.slice(1),
                                                    addClass: classFlexItem,
                                                    value: response['directories'][key]['id']})
                                    .append(response['directories'][key]['name']))
                                .append($('<img>', {class: classFlexEndItem,
                                                    addClass: classContextMenuIcon.slice(1),
                                                    src: menu_image})));
    };
    for (let key in response['checklists']) {
        $(idChecklistList).append($('<div>', {class: classChecklist.slice(1),
                                                addClass: classFlexContainer})
                                .append($('<div>', {class: classChecklistLabel.slice(1),
                                                    addClass: classFlexItem,
                                                    value: response['checklists'][key]['id']})
                                    .append(response['checklists'][key]['name']))
                                .append($('<img>', {class: classFlexEndItem,
                                                    addClass: classContextMenuIcon.slice(1),
                                                    src: menu_image})));
    };
};

// load checklist data in .content block
// response{'id', 'name', 'data'}
function load_checklist_data(response) {
    let data;
    $(idContentBlock).css({'min-height': '85vh',});
    $(idChecklistContentBlock).empty();
    $(idChecklistContentBlock).append($('<p>', {id: idChecklistPathLabel.slice(1)})
                                    .append(path_start + $(classParentDirectoryLabel).text()));
    $(idChecklistContentBlock).append($('<h2>', {class: classH2Header.slice(1),
                                                 value: response['id']})
                                                 .append(response['name']))
                              .append($('<div>', {id: idChecklistData.slice(1)}));
    if (response['data']) {
        data = JSON.parse(response['data']);
    };
    for (let key in data) {
        if (data[key]['status']) {
            $(idChecklistData).append($('<div>', {class: classFlexContainer})
                                    .append($('<input>', {type: "checkbox",
                                                          class: classCheckbox.slice(1),
                                                          addClass: classFlexEndItem,
                                                          checked: true}))
                                    .append($('<label>', {class: classCheckboxLabel.slice(1),
                                                          addClass: classFlexItem})
                                        .append(data[key]['text'])));
        }
        else {
            $(idChecklistData).append($('<div>', {class: classFlexContainer})
                                    .append($('<input>', {type: "checkbox",
                                                          class: classCheckbox.slice(1),
                                                          addClass: classFlexEndItem}))
                                    .append($('<label>', {class: classCheckboxLabel.slice(1),
                                                          addClass: classFlexItem})
                                        .append(data[key]['text'])));
        };
    };
    $(idCheckboxEditorBlock).addClass(classHideElement.slice(1));
    $(idAddNewCheckboxBlock).removeClass(classHideElement.slice(1));
    loaded_checklist = $(idChecklistContentBlock)[0].innerHTML;
    $('html, body').stop().animate({scrollTop: $(idChecklistContentBlock).offset().top}, 800);
};

//actions after successful saving checklist
function saved_checklist(response) {
};

function edit_directory_name(directory_id) {
        let element = $(classDirectoryLabel + '[value="' + directory_id + '"]');
        $(element).addClass(classHideElement.slice(1));
        let editor = $('<input/>', { id: idDirectoryEditorInput.slice(1),
                                  class: classFlexItem,
                                  addClass: classElementEditor.slice(1)})
            .val(element.text());
        $(element).after(editor);
        editor.select();
};

function move_directory_up(directory_id, current_directory_id) {
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_directory_id'] = directory_id;
        dict['current_directory_id'] = current_directory_id;
        element = $(classDirectoryLabel + '[value="' + directory_id + '"]').parent();
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: function() {
                element.fadeOut();
                directory_path = path_start + $(classParentDirectoryLabel).text() +
                                            $(classDirectoryLabel + '[value="' + directory_id + '"]').text() + '/';
                if ($(idChecklistPathLabel).text().indexOf(directory_path) == 0) {
                    clear_checklist_data();
                };
            },
            error: function(response) {location.reload();},
        });
};

function move_directory_to(directory_id, target_directory_id) {
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_directory_id'] = directory_id;
        dict['target_directory_id'] = target_directory_id;
        element = $(classDirectoryLabel + '[value="' + directory_id + '"]').parent();
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: function() {
                element.fadeOut();
                directory_path = path_start + $(classParentDirectoryLabel).text() +
                                            $(classDirectoryLabel + '[value="' + directory_id + '"]').text() + '/';
                if ($(idChecklistPathLabel).text().indexOf(directory_path) == 0) {
                    clear_checklist_data();
                };
            },
            error: function(response) {location.reload();},
        });
};

function remove_directory(directory_id) {
        let directory_name = $(classDirectoryLabel + '[value="' + directory_id + '"]').text();
        if (confirm('Are you sure you want to delete the directory("' + directory_name + '") with all its contents?')) {
            let dict = {};
            let element;
            dict['csrfmiddlewaretoken'] = csrf;
            dict['delete_directory_id'] = directory_id;
            element = $(classDirectoryLabel + '[value="' + directory_id + '"]').parent();
            $.ajax({
                url: '',
                type: 'post',
                data: dict,
                success: function() {
                    element.fadeOut();
                    directory_path = path_start + $(classParentDirectoryLabel).text() +
                                            $(classDirectoryLabel + '[value="' + directory_id + '"]').text() + '/';
                    if ($(idChecklistPathLabel).text().indexOf(directory_path) == 0) {
                        clear_checklist_data();
                    };
                },
                error: function(response) {location.reload();},
            });
        };
};

function edit_checklist_name(checklist_id) {
        let element = $(classChecklistLabel + '[value="' + checklist_id + '"]');
        $(element).addClass(classHideElement.slice(1));
        let editor = $('<input/>', { id: idChecklistEditorInput.slice(1),
                                  class: classFlexItem,
                                  addClass: classElementEditor.slice(1)})
            .val(element.text());
        $(element).after(editor);
        editor.select();
};

function move_checklist_up(checklist_id, current_directory_id) {
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_checklist_id'] = checklist_id;
        dict['current_directory_id'] = current_directory_id;
        element = $(classChecklistLabel + '[value="' + checklist_id + '"]').parent();
        if (checklist_id == $(classH2Header, idChecklistContentBlock).attr('value')) {
            let path = $(idChecklistPathLabel).text();
            path = path.slice(0, -1);
            path = path.slice(0, path.lastIndexOf('/') + 1);
            $(idChecklistPathLabel).text(path);
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
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['moving_checklist_id'] = checklist_id;
        dict['target_directory_id'] = target_directory_id;
        element = $(classChecklistLabel + '[value="' + checklist_id + '"]').parent();
        if (checklist_id == $(classH2Header, idChecklistContentBlock).attr('value')) {
            $(idChecklistPathLabel).append($(classDirectoryLabel + '[value="' + target_directory_id + '"').text() + '/');
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
        let checklist_name = $(classChecklistLabel + '[value="' + checklist_id + '"]').text();
        if (confirm('Are you sure you want to delete the checklist("' + checklist_name + '")?')) {
        let dict = {};
        let element;
        dict['csrfmiddlewaretoken'] = csrf;
        dict['delete_checklist_id'] = checklist_id;
        element = $(classChecklistLabel + '[value="' + checklist_id + '"]').parent();
        $.ajax({
            url: '',
            type: 'post',
            data: dict,
            success: function() {
                element.fadeOut();
                if (checklist_id == $(classH2Header, idChecklistContentBlock).attr('value')) {
                    clear_checklist_data();
                };
            },
            error: function(response) {location.reload();},
        });
        };
};

// clear loaded checklist data from DOM
function clear_checklist_data() {
    $(idChecklistContentBlock).empty();
    $(idCheckboxEditorBlock).addClass(classHideElement.slice(1));
    $(idAddNewCheckboxBlock).addClass(classHideElement.slice(1));
};
