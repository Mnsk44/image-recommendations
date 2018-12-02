
let imgCont = $("#image-container");
var selectedTags = new Set();

$("#tag-container").on("click", ".tag", function(event) {
    removeTag(event);
})

function addTag(id, value) {
    if (!selectedTags.has(value) && value !== null) {
        selectedTags.add(value);
        $("#tag-container").append(`<div data-index="${value}" class="tag"><p>${value}</p></div>`);
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
                console.log("palautus :", data);
                imgCont.empty();
                for (let i = 0; i < data.length; i++) {
                    imgCont.append(`<div class="gallery__image"><a href="/image/${data[i].url}"><img src="/static/images/${data[i].url}"></a></div>`);
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