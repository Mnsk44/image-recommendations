$(document).ready(function() {

    let tags = ["nature", "mountain", "all"];
    let select = $("#search-field");
    
    select.append('<option selected="true" disabled>Choose tag</option>');
    select.prop('selectedIndex', 0);

    $.each(tags, function(i) {
        select.append(`<option value="${i}">${tags[i]}</option>`);
    })
})

//var selectedTags = [];

$("#search-btn").click(function(event) {
    searchImages($("#search-field").val());
})

function searchImages(label) {
    //selectedTags.push(label);
    //console.log(selectedTags);
    $.ajax({
        type : "POST",
        url : "search",
        data : {data:label},
        dataType : "json",
        success : function(data) {
            console.log("palautus :", data);
            var newCont = "";
            for (let i = 0; i < data.length; i++) {
                newCont += `<div class="image"><img src="/static/images/${data[i]}"></div>`;
            }
            $("#image-container").html(newCont);
        },
        error: function (req, status, error) {
            console.log(req, status, error);
        }
    })
}