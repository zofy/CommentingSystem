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
var a;
    comments.nextAjax = function(){
        comments.idx ++;
        $.ajax({
                type: 'POST',
                url: '/listComments/',
                data: {'move': 'next', 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
                success: function(json){
                    console.log('comments' in json);
                    // refresh comments on page
                    for(var i = 0; i < json.comments.length; i++){
                        a = json.comments;
                        //console.log(a);
                        console.log(json.comments[i]);
                    }
                    //console.log(json.comments);
                },
                dataType: 'json'
            });
    };

comments.setUp();
