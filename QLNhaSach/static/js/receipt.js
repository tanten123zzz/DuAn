//{1:["Thanh toán","Chờ thanh toán"]}

function getUniqueValuesFromColumn(){
    var unique_col_values_dict = {}

    allFilters = document.querySelectorAll(".table-filter")
    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute("col-index");
//        alert(col_index)
        const rows = document.querySelectorAll(".table > tr > td")
        rows.forEach((row)=>{
           cell_value = row.querySelector("td:nth-child("+col_index+")").innerHTML;

           if (col_index in unique_col_values_dict){
                if(unique_col_values_dict[col_index].includes(cell_value)) {
//                    alert(cell_value + "Hullllleee" + unique_col_values_dict[col_index])
                }
                else{
                    unique_col_values_dict[col_index].push(cell_value)
//                    alert("Hellooooo " + unique_col_values_dict[col_index])
                }
           }
           else{
                unique_col_values_dict[col_index] = new Array(cell_value)
           }
        });
    });
    for (i in unique_col_values_dict){
        alert("Column index: " + i +  "Has unique: \n" + unique_col_values_dict[i]);
    }
    updateSelectOptions(unique_col_values_dict)
};

function updateSelectOptions(unique_col_values_dict){
     allFilters = document.querySelectorAll(".table-filter")

     allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute('col-index')

        unique_col_values_dict[col_index].forEach((i) => {
            filter_i.innerHTML = filter_i.innerHTML + `\n<option value="$[i]"> $[i]</option>`
        });
     });
};

function filter_rows(){
     allFilters = document.querySelectorAll(".table-filter")
     var filter_value_dict = {}

     allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute('col-index')

        value = filter_i.value
        if (value != "all"){
            filter_value_dict[col_index] = value;
        }
     });
     var col_cell_value_dict = {};

     const rows = document.querySelectorAll(".table tr td");
     rows.forEach((row) => {
        var display_row = true;

        allFilter.forEach((filter_i) => {
            col_index = filter_i.parentElement.getAttribute('col-index')
            col_cell_value_dict[col_index] = row.querySelector("td:nth-child("+ col_index + ")").innerHTML
        })

        for (var col_i in filter_value_dict){
            filter_value = filter_value_dict[col_i]
            row_cell_value = col_cell_value_dict[col_i]

            if (row_cell_value.indexOf(filter_value) == -1 && filter_value != "all") {
                display_row = false;
                break;
            }
        }
        if (display_row == true){
            row.style.display = "table-row"

        }else{
            row.style.display = "none"
        }
     });
}
