/**
 * Created by alvaro on 9/23/17.
 */
function analyze() {
    var calc_input = $("input[name=display]").val();
    var data = JSON.stringify({"calc_input": calc_input});
    $.ajax({
        url: "/contentanalysis",
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8'
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        update_dictionary_buttons(dict_labels,active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
        $('#table').html(response['result_table']);
    });
 }
function upload_dictionaries() {
    var formData = new FormData($('form')[0]);
    $.ajax({
        url: '/uploaddictionaries',
        type: 'POST',
        processData: false, // important
        contentType: false, // important
        data: formData,
        error: function (jqXHR, textStatus, errorThrown) {
          $('#error-modal-message').html('Lexos could not apply the analysis content actions.');
          $('#error-modal').modal();
          console.log('bad: ' + textStatus + ': ' + errorThrown)
        }
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        var toggle_all = response['toggle_all'];
        update_check_all_checkbox(toggle_all);
        update_dictionary_buttons(dict_labels,active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
    })
}
function toggle_checkbox(i) {
    var data = "";
    if(i == -1){
        data = JSON.stringify({"toggle_all": true});
    } else {
        var dict_names = [];
        $("input[name=dictionary]").each(function(){ dict_names.push(this.value); });
        var dict_name = dict_names[i];
        data = JSON.stringify({"dict_name": dict_name, "toggle_all": false});
    }
    $.ajax({
        url: "/toggledictionary",
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8'
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        var toggle_all = response['toggle_all'];
        $('#display').val("");
        update_check_all_checkbox(toggle_all);
        update_dictionary_buttons(dict_labels,active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
    })
}
function delete_dictionary(i) {
    var dict_names = [];
    $("input[name=dictionary]").each(function(){ dict_names.push(this.value); });
    var dict_name = dict_names[i];
    var data = JSON.stringify({"dict_name": dict_name});
    $.ajax({
        url: "/deletedictionary",
        type: "POST",
        data: data,
        contentType: 'application/json;charset=UTF-8'
    }).done(function (response) {
        response = JSON.parse(response);
        var dict_labels = response['dictionary_labels'];
        var active_dicts = response['active_dictionaries'];
        $('#display').val("");
        if(dict_labels.length == 0){
            $('#forAllCheckBox').empty();
        }
        update_dictionary_buttons(dict_labels, active_dicts);
        update_dictionary_checkboxes(dict_labels, active_dicts);
    })
}
function backspace(calc){
    var content = calc.display.value;
    var length = content.length;
    if(content[length -1] == "]"){
        content = content.substring(0,content.lastIndexOf("["));
    }else if(content.endsWith("sin(") || content.endsWith("cos(") ||
            content.endsWith("tan(") || content.endsWith("log(")){
        content = content.substring(0,length - 4);
    }else if(content.endsWith("^(") || content.endsWith("√(") ){
        content = content.substring(0,length - 2);
    }else{
        content = content.substring(0,length - 1);
    }
    calc.display.value = content;
}
function update_dictionary_buttons(dict_labels, active_dicts) {
    $('#dictionaryButtons').empty();
    for (var i = 0; i < dict_labels.length; i++) {
        if(active_dicts[i]) {
            var button = "<input type='button' value='" + dict_labels[i] + "'" +
                " onClick='" + "this.form.display.value+=\"[" + dict_labels[i] + "]\"'>";
            $('#dictionaryButtons').append(button);
        }
    }
}
function update_dictionary_checkboxes(dict_labels, active_dicts) {
    $('#checkboxes').empty();
    for (var i = 0; i < dict_labels.length; i++) {
        var checkbox = "<div class='forAllCheckBox' align='left'>" +
            "<input type='hidden' name='dictionary' value='"+dict_labels[i]+"'>" +
            "<label class='icon-checkbox";
        if(active_dicts[i]){
            checkbox += " checked";
        }
        checkbox += "'><input type='checkbox' id='dict_checkbox' onclick='toggle_checkbox("+i+")'>"+dict_labels[i]+ "</label>";
        checkbox += "<a role='button'><span class='glyphicon glyphicon-remove delete' onclick='delete_dictionary(" + i + ")'></span></a>";
        $('#checkboxes').append(checkbox);
    }
}
function update_check_all_checkbox(toggle_all) {
    $('#forAllCheckBox').empty();
    var check_all = "<label class='icon-checkbox";
    if(toggle_all) {
        check_all += " checked";
    }
    check_all += "'><input type='checkbox' id='allCheckBoxSelector' onclick='toggle_checkbox(-1)'>Check/Uncheck All</label>";
    $('#forAllCheckBox').append(check_all);
}
