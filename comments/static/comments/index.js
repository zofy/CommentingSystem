    var comments = {};

    comments.page = 0;

    comments.setUp = function(){
        // add a click listener on prev resp. next button
        $('#next').click(function(){
            console.log('You clicked next');
            comments.listComments('next');
        });
        $('#prev').click(function(){
            console.log('You clicked previous');
            comments.listComments('previous');
        });
    };


    comments.listComments = function(direction){
        if(direction === 'next') {
            comments.page++;
        }else if(direction === 'previous'){
            comments.page--;
        }
        $.ajax({
                type: 'POST',
                url: '/listComments/',
                data: {'move': direction, 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
                success: function(json){
                    // refresh comments on page
                    if('comments' in json) {
                        comments.refreshComments(json.comments);
                        //for (var i = 0; i < json.comments.length; i++) {
                        //    console.log(json.comments[i]);
                        //}
                    }
                },
                dataType: 'json'
        });
    };


    comments.refreshComments = function(listOfComments){
        $('#commenters').html('');
        var html = '';
        for(var i = 0; i < listOfComments.length; i++){
            var content = listOfComments[i][4];
            var date = listOfComments[i][5];
            var depth = listOfComments[i][2];
            html = '<li class="c" style="margin-left:' + depth + 'em;">' +
                '<p class="poster">Anonymous - ' + date + '</p>' +
                '<p>' + content + '</p>' +
                '<p><i class="fa fa-plus" aria-hidden="true"></i> <i class="fa fa-minus" aria-hidden="true"></i> <a class="reply">reply</a></p>' +
                '</li>'
            $('#commenters').append(html);
            console.log(listOfComments[i]);
            console.log(listOfComments[i][4]);
        }
    }

comments.setUp();
