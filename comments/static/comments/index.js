    var comments = {};

    comments.idx = 0;

    comments.setUp = function(){
        // add a click listener on prev resp. next button
        $('#next').click(function(){
            alert('efefef');
            comments.nextAjax();
        });
        $('#prev').click(function(){
            alert('efefef');
        });
    };

    comments.nextAjax = function(){
        comments.idx ++;
        $.ajax({
                type: 'POST',
                url: '/listComments/',
                data: {'move': 'next', 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
                success: function(json){
                    // refresh comments on page
                    //$.each(json.comments, function(comment){
                    //    console.log(comment);
                    //});
                    console.log(json.comments);
                },
                dataType: 'json'
            });
    };

comments.setUp();
