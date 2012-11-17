function img_auto_load ()
 {
   var links = document.getElementsByTagName('a');
   var newImage, newBR

   for ( var i in links )
     {
       if ( typeof( links[i ].href ) == 'string' )
         {
           var imageLink = links[i ].href+'';
           if (( imageLink.indexOf('.jpg') != -1 ) ||( imageLink.indexOf('.gif') != -1 ) ||( imageLink.indexOf('.png') != -1 ) ||( imageLink.indexOf('.bmp') != -1 )||( imageLink.indexOf('.BMP') != -1 )||( imageLink.indexOf('.JPG') != -1 ) ||( imageLink.indexOf('.GIF') != -1 ) ||( imageLink.indexOf('.PNG') != -1 ))
             {
               newImage = document.createElement('img');
               newBR = document.createElement('br');
               newImage.src = links[i].href;
               links[i].innerHTML = '';
               links[i ].appendChild(newImage);                                        
             }
         }
     }
 }
setInterval('img_auto_load()', 1000);
