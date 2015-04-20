var timeout = 500;
var closetimer  = 0;
var ddmenuitem  = 0;
var room_name = "{{room_name}}";
// open hidden layer
function mopen(id)
{ // cancel close timer
    mcancelclosetime();
    // close old layer
    if(ddmenuitem) ddmenuitem.style.visibility = 'hidden';
    // get new layer and show it
    ddmenuitem = document.getElementById(id);
    ddmenuitem.style.visibility = 'visible';
}

// close showed layer
function mclose()
{
    if(ddmenuitem) ddmenuitem.style.visibility = 'hidden';
}

// go close timer
function mclosetime()
{
    closetimer = window.setTimeout(mclose, timeout);
}

// cancel close timer
function mcancelclosetime()
{
if(closetimer){
    window.clearTimeout(closetimer);
    closetimer = null;
    }
}

// close layer when click-out
document.onclick = mclose; 
$(document).ready(function(){

    $("#run").click(function () { 
        $("#effect").toggle("blind"); 
        $("#run").val("Show IT news");
    });  
      
    $(".room" ).click(function( event ) {

        event.preventDefault();
        alert('You need to login')
       console.info('Prevent default')    
    });

    namespace = '/room-socket'; // change to an empty string to use the global namespace

        
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
   
    $('#send_chat_message').click ( function(){
        console.info("send_chat_message");
        
        var user_message =  $('#user_message').val()
        console.info(user_message, "messs")
        
        socket.emit('client message sent', {data: user_message, room: room_name});

        console.info("send_chat_message_after");
        return false;
    });
    
    socket.on('server message sent', function(data) {
        console.info("server message sent: ", data);
        if ((data.room == room_name) || (data.room == '*')) {
            $('#messages').append('[' + data.time_received + '] <u>'+ '<a href=/user/'+data.user +'>'+ data.user + '</a>' + '</u>: <b>' + data.message + '</b><br>');
        }
    });
    $(window).on('beforeunload', function(){
    socket.close();
});



});   
