function myFunction(){
    var x = document.getElementById("myFile");
    var txt = "";
    if ('files' in x) {
        if (x.files.length == 0) {
            txt = "Select one or more files.";
        } else {
            for (var i = 0; i < x.files.length; i++) {
                txt += (i+1) + ". file";
                var file = x.files[i];
                if ('name' in file) {
                    txt += "name: " + file.name + "";
                }
                if ('size' in file) {
                    txt += "size: " + file.size + " bytes ";
                }
            }
        }
    } 
    else {
        if (x.value == "") {
            txt += "Select one or more files.";
        } else {
            txt += "The files property is not supported by your browser!";
            txt  += "The path of the selected file: " + x.value; // If the browser does not support the files property, it will return the path of the selected file instead. 
        }
    }
    document.getElementById("input-id").innerHTML = x.value;
}

