function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#avatarimage').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function() {
    $("#handle").popover({placement:'right', trigger:'focus'});
    $("#playername").popover({placement:'right', trigger:'focus'});
    $("#pass1").popover({placement:'right', trigger:'focus'});
    $("#pass2").popover({placement:'right', trigger:'focus'});
    $("#bpass").popover({placement:'right', trigger:'focus'});
    $("#team-name").popover({placement:'right', trigger:'focus'});
    $("#team-code").popover({placement:'right', trigger:'focus'});
    $("#motto").popover({placement:'right', trigger:'focus'});
    $("#regtoken").popover({placement:'right', trigger:'focus'});

    /* Avatar */
    $(".useravatarimg").click(function() {
        var filename = $(this).attr('value');
        $("#user_avatar_select").val(filename);
        $("#avatarimage").attr("src", "/avatars/" + $(this).attr('value'));
        $("#avatarclose").click();
    });
    $("#user-avatar").change(function(){
        $("#user_avatar_select").val("");
        readURL(this);
    });

    $("#uploadbutton").click(function(){
        $("#user-avatar").click();
    });
});