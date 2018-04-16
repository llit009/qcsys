$(function() {
    $('#qcnum').blur(function() {
        var qcnum = $('#qcnum').val();
        $.ajax({
            url: "/admin/uniquecheck",
            data: {'qcnum':qcnum},
            type: 'GET',
            success: function(response) {
                console.log(response.errormsg);
                msg = response.errormsg
                if (response.errormsg == 1){
                    $('#checkqc_num').empty();
                    $('#checkqc_num').removeClass("hidden_mark").addClass("show_mark_error");
                    $('#checkqc_num').append("<span>&#10006; 编号重复，请重新输入</span>");
                    $('#opencasesubmit').attr("disabled", true);
                } else if (response.errormsg == 0) {
                    $('#checkqc_num').empty();
                    if ($('#checkqc_num').hasClass('show_mark_error')){
                        $('#checkqc_num').removeClass("hidden_mark show_mark_error").addClass("show_mark_check");
                        $('#opencasesubmit').removeAttr("disabled");
                    } else {
                        $('#checkqc_num').removeClass("hidden_mark").addClass("show_mark_check");
                        $('#opencasesubmit').removeAttr("disabled");
                    }
                    $('#checkqc_num').append("<span>&#10004;</span>");
                } else {
                    $('#checkqc_num').empty();
                    $('#checkqc_num').removeClass("hidden_mark").addClass("show_mark_error");
                    $('#checkqc_num').append("<span>&#10006; "+ msg +"</span>");
                    $('#opencasesubmit').attr("disabled", true);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});


$(function() {
    $("#item-username").autocomplete({
        source:function(request, response) {
            $.getJSON("/admin/staffinput",{
                q: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                response(data.matching_result); // matching_results from jsonify
            });
        },
        minLength: 1,
        select: function(event, ui) {
//            console.log(ui.item.value); // not in your question, but might help later
        }
    });
});

$(function() {
    $("#item-labels").autocomplete({
        source:function(request, response) {
            $.getJSON("/admin/labelinput",{
                labeldata: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                response(data.matching_result); // matching_results from jsonify
            });
        },
        minLength: 1,
        select: function(event, ui) {
//            console.log(ui.item.value); // not in your question, but might help later
        }
    });
});

$(function() {
    $("#under_label").autocomplete({
        source:function(request, response) {
            $.getJSON("/admin/underlabelinput",{
                q: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                response(data.matching_result); // matching_results from jsonify
            });
        },
        minLength: 1,
        select: function(event, ui) {
//            console.log(ui.item.value); // not in your question, but might help later
        }
    });
});