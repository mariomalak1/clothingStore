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

function update_plot(data = "", place = "") {
  let shown_data = [];
  if (data) {
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

  let layout = {
    barmode: 'group'
  };
  Plotly.newPlot('myPlot', shown_data, layout);
}

function makeAjaxRequest(url, method, data, successCallback, errorCallback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        update_plot(JSON.parse(xhr.responseText), "from_one_year")
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
  makeAjaxRequest("/store/admin_panel/ajax_request/get_data_specific_year_for_statistics/?specific_year=" + value, "get", {
    "specific_year": value
  });
}
