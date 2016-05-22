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
            var idComment = listOfComments[i][6];
            html = '<li id="' + idComment + '" class="c" style="margin-left:' + depth + 'em;">' +
                '<p class="poster">Anonymous - ' + date + '</p>' +
                '<p>' + content + '</p>' +
                '<p><i class="fa fa-plus" aria-hidden="true"></i> <i class="fa fa-minus" aria-hidden="true"></i> <a class="reply">reply</a></p>' +
                '</li>'
            $('#commenters').append(html);
            console.log(listOfComments[i]);
            console.log(listOfComments[i][4]);
        }
    }


    comments.vote = function(id, vote){
        $.ajax({
                type: 'POST',
                url: '/rateComment/',
                data: {'id': id, 'vote': vote, 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
                success: function(json){
                    // rates comment
                    console.log('You voted!');
                },
                dataType: 'json'
        });
    }
comments.setUp();
