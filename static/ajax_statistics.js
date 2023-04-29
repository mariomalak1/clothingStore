function makeAjaxRequest(url, method, data, successCallback, errorCallback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                successCallback(xhr.responseText);
            } else {
                errorCallback(xhr.status);
            }
        }
    };
    xhr.send(JSON.stringify(data));
}


function get_value_of_year_and_call_server(){
    let select_element = document.getElementById("date_select_year");
    let selected_option = select_element.options[select_element.selectedIndex];
    let value = selected_option.value;
    makeAjaxRequest("/store/admin_panel/ajax_request/get_data_specific_year_for_statistics/?specific_year="+ value, "get", {"specific_year":value});
}