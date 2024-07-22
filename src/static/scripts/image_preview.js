function getImagePreview(event, id_img){
    var image = URL.createObjectURL(event.target.files[0]);
    var imagediv = document.getElementById(id_img);
    var newimage = document.createElement('img');
    
    console.log("UNO");
    console.log(imagediv)

    imagediv.innerHTML = '';
    newimage.src = image;
    newimage.height = '210';
    console.log("dos");
    console.log(newimage);
    
    imagediv.appendChild(newimage);
    console.log("trES y fin");
}