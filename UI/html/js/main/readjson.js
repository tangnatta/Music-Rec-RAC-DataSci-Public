
$(document).ready(function () {
    console.log(data[0]["id"]);
    var content = "<tr>"+
        "<th scope = 'col'>No.</th>" +
        "<th scope='col'>Title</th>" +
        "<th scope='col'>Authors</th>" + "</tr >"

    for (i = 0; i < data.length; i++) {
        const words = data[i]["Authors"].split(';');
        var title = data[i]["title"]
        var line_ref = "abstract.html?id=" + data[i]["id"]
        var authors = ""
        console.log(words)
        for (j = 0; j < words.length; j++) {
            authors +=words[j]+"<br>"
        }
        content += "<tr>" +
            "<th scope = 'row'>" + data[i]["id"] + "</th>" +
            "<td><a href=" + line_ref+">" + title + "</a></td>" +
            "<td>" + authors + "</td>" + "</tr >"
            

    }
                                              
                                            
	$('#papers').html(content);
});
