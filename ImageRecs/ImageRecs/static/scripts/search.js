
//let select = $("#search-field");
let imgCont = $("#image-container");
var selectedTags = new Set();

//let images = ["dragonfly", "moss", "mountain", "mountain2", "mountain3", "guitar"];

$(document).ready(function() {
    /*select.append('<option selected="true" disabled>Choose tag</option>');
    select.prop('selectedIndex', 0);
    $.each(tags, function(i) {
        select.append(`<option value="${tags[i].id}">${tags[i].name}</option>`);
    })
    */
})

/*
$("#search-btn").click(function(event) {
    addTag(select.val());
})
*/

$("#tag-container").on("click", ".tag", function(event) {
    removeTag(event);
})

function addTag(id, name) {
    if (!selectedTags.has(id) && id !== null) {
        selectedTags.add(id);
        $("#tag-container").append(`<div data-index="${id}" class="tag"><p>${name}</p></div>`);
        searchImages(selectedTags);
    }
}

function removeTag(e) {
    index = e.currentTarget.dataset.index;
    selectedTags.delete(index);
    $(`*[data-index="${e.currentTarget.dataset.index}"]`).remove();
    searchImages(selectedTags);
}

function searchImages(tags) {
    if (tags.size > 0) {
        arr = Array.from(tags)
        console.log("lähetettävä data: ", arr);
        $.ajax({
            type : "POST",
            url : "search",
            data : {data:arr},
            dataType : "json",
            success : function(data) {
                //window.history.pushState("object or string", "Title", "/search");
                console.log("palautus :", data);
                imgCont.empty();
                for (let i = 0; i < data.length; i++) {
                    imgCont.append(`<div class="gallery__image"><a href="/image/${data[i].url}"><img src="/static/images/${data[i].url}.jpg"></a></div>`);
                }
            },
            error: function (req, status, error) {
                console.log("ERROR: ", req, status, error);
            }
        })
    }
    else imgCont.empty();
}

$('#autocomplete').autocomplete({
    lookup: tags,
    onSelect: function (suggestion) {
        addTag(suggestion.data, suggestion.value)
    }
});