function create_empty_plot(){
  let trace1 = {
    x : 0,
    y : 0,
  }
  let shown_data = [trace1]
  let layout = {barmode: 'group'};
  Plotly.newPlot('myPlot', shown_data, layout);
}

function get_month_names() {
  return ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
}

function months_total_return(data) {
  let list_total_in_months = [];
  for (let branch of data) {
    let total_for_branch = [];
    for (let month of branch[Object.keys(branch)[0]]) {
      total_for_branch.push(month[Object.keys(month)[0]]);
    }
    list_total_in_months.push(total_for_branch);
  }
  return list_total_in_months;
}


function get_all_branches(data) {
  let all_branches = [];
  for (let i of data) {
    all_branches.push(Object.keys(i)[0]);
  }
  return all_branches;
}

function get_days_range_for_month(data){
  let days = [];
  for (let key in data[0]) {
    if (data[0].hasOwnProperty(key)) {
      days.push(key);
    }
  }
  return days;
}

function total_in_days(data){
  let list_total_in_days = []
  for(let branch in data){
    for (let i in branch){
      if (branch.hasOwnProperty(i)) {
        list_total_in_days.push(branch[i]);
      }
    }
  }
  return list_total_in_days;
}

function update_plot(data = "", place = "") {
  let shown_data = [];
  if (data) {
    if (place === "from_one_year") {
      let all_branches = get_all_branches(data)
      let all_month_names = get_month_names();
      let all_months_total = months_total_return(data);
      for (let i = 0; i < all_branches.length; i++) {
        let trace = {
          x: all_month_names,
          y: all_months_total[i],
          name: all_branches[i],
          type: 'bar'
        };
        shown_data.push(trace)
      }
    }
    else if(place === "from_month_year"){
      let range_month_days = get_days_range_for_month(data);
      let all_branches = get_all_branches(data)
      let all_total_in_day = total_in_days(data);
      for (let i = 0; i < all_branches.length; i++) {
        let trace = {
          x: range_month_days,
          y: all_total_in_day[i],
          name: all_branches[i],
          type: 'bar'
        };
        shown_data.push(trace);
      }
    }
  }
  let layout = {
    barmode: 'group'
  };
  console.log(shown_data);
  Plotly.newPlot('myPlot', shown_data, layout);
}

function makeAjaxRequest(url, method, data, place_from, successCallback, errorCallback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        update_plot(JSON.parse(xhr.responseText), place_from)
      } else {
        errorCallback(xhr.status);
      }
    }
  };
  xhr.send(JSON.stringify(data));
}

function get_value_of_year_and_call_server() {
  let select_element = document.getElementById("date_select_year");
  let selected_option = select_element.options[select_element.selectedIndex];
  let value = selected_option.value;
  if (value !== "0") {
    makeAjaxRequest("/store/admin_panel/ajax_request/get_data_specific_year_for_statistics/?specific_year=" + value, "get", {
      "specific_year": value
    }, "from_one_year");
  }else{
    create_empty_plot();
  }
}

function get_value_of_year_month_and_call_server() {
  let year_select_element = document.getElementById("date_select_year");
  let month_select_element = document.getElementById("date_select_month");
  let year_selected_option = year_select_element.options[year_select_element.selectedIndex];
  let month_selected_option = month_select_element.options[month_select_element.selectedIndex];
  let year_value = year_selected_option.value;
  let month_value = month_selected_option.value;
  if (year_value !== "0" && month_value !== "0") {
    makeAjaxRequest("/store/admin_panel/ajax_request/get_data_by_year_month_for_statistics/?year=" + year_value + "&month=" + month_value, "get", {
      "year": year_value,
      "month": month_value,
    }, "from_month_year");
  }else{
    create_empty_plot();
  }
}

function put_years_in_select_element(year_date_select){
  let currentYear = new Date().getFullYear();
  let earliestYear = 1970;
  let dateOption = document.createElement('option');
  dateOption.text = "-------";
  dateOption.value = 0;
  dateOption.selected = true;
  year_date_select.add(dateOption)
  while (currentYear >= earliestYear) {
    dateOption = document.createElement('option');
    dateOption.text = currentYear;
    dateOption.value = currentYear;
    year_date_select.add(dateOption);
    currentYear -= 1;
  }
}

function put_month_names_in_select_element(month_date_select){
  let month_names = get_month_names()
  let dateOption = document.createElement('option');
  dateOption.text = "-------";
  dateOption.value = 0;
  dateOption.selected = true;
  month_date_select.add(dateOption)
  for(let i = 0; i < month_names.length; i++) {
    dateOption = document.createElement('option');
    dateOption.text = month_names[i];
    dateOption.value = i + 1;
    month_date_select.add(dateOption);
  }
}

function put_days_in_select_element(year_date_select, month_date_select){

}

function with_specific_year_only(year_date_select, myDiv){
  year_date_select.className = "form-select";
  year_date_select.onchange = get_value_of_year_and_call_server;
  year_date_select.id = "date_select_year";
  put_years_in_select_element(year_date_select);
  myDiv.appendChild(year_date_select);
}

function with_month_year(year_date_select, myDiv){
    let month_date_select = document.createElement("select");
    year_date_select.className = "form-select";
    month_date_select.className = "form-select";
    year_date_select.onchange = get_value_of_year_month_and_call_server;
    month_date_select.onchange = get_value_of_year_month_and_call_server;
    year_date_select.id = "date_select_year";
    month_date_select.id = "date_select_month";
    put_years_in_select_element(year_date_select);
    put_month_names_in_select_element(month_date_select);
    myDiv.appendChild(year_date_select);
    myDiv.appendChild(month_date_select);
}

function with_day_month_year(year_date_select, myDiv){
    let month_date_select = document.createElement("select");
    let day_date_select = document.createElement("select");
    year_date_select.className = "form-select";
    month_date_select.className = "form-select";
    day_date_select.className = "form-select";
    // year_date_select.onchange = get_value_of_year_and_call_server;
    // month_date_select.onchange = get_value_of_year_and_call_server;
    year_date_select.id = "date_select_year";
    month_date_select.id = "date_select_month";
    put_years_in_select_element(year_date_select);
    put_month_names_in_select_element(year_date_select);
    put_days_in_select_element(year_date_select, month_date_select);
    myDiv.appendChild(year_date_select);
    myDiv.appendChild(month_date_select);
}

function select_the_date(select_element, myDiv){
  let year_date_select = document.createElement("select");
  // if the user choose with specific year
  if (select_element.options[select_element.selectedIndex].value === "1"){
    with_specific_year_only(year_date_select, myDiv)
  }
  // if the user choose with specific year and month
  else if (select_element.options[select_element.selectedIndex].value === "2"){
    with_month_year(year_date_select, myDiv);
  }
  // if the user choose With Specific Day and Month And Year
  else if (select_element.options[select_element.selectedIndex].value === "3"){
    with_day_month_year(year_date_select, myDiv);
  }
}