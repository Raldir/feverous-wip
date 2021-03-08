var base_url = 'http://mediawiki.feverous.co.uk/index.php/';
$.ajaxSetup({async:false});

$(window).on('load', function() {

  //$( document ).ready(function() {

  var status_page = localStorage.getItem('status-page');
  if (status_page == 'open'){
    $('body').remove();
  }else{
    run_page();
  }



  function run_page(){
    localStorage.setItem('status-page', 'open');
    $("body").append('<iframe id="my-wikipedia"></iframe>');
    $("#my-wikipedia").prop('src', localStorage.getItem('last-url')) ;

    $('#my-wikipedia').on("load", function() {
      Processor.reload_elements();
    });


    $(function () {
      $('[data-toggle="popover"]').popover();
    })

    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    })

    // $('#go-back').prop('disabled', false);

    Processor.init();
    $('select').selectpicker();

    $(window).on('beforeunload', function(){
      localStorage.setItem('status-page', 'reload');
      if (localStorage.getItem('back-counter') > 0){
        Processor.reset_evidence_menu();
        localStorage.setItem('back-counter', 0);
      }
    });
    // $(window).onpopstate = function(event) {
    //     // make the parent window go back
    //     alert('yao');
    //     top.history.back();
    //   };

    $(".logout").on('click', function(e) {
      $.ajax({
        url: "annotation-service/logout.php",
        type: "GET",
        success: function(data){
          localStorage.clear();
          window.location.reload();
        }
      });
    });

    function prepare_submission(){

      [evidence1, details1] = Highlighter.get_selected_annotations(1);
      [evidence2, details2] = Highlighter.get_selected_annotations(2);
      [evidence3, details3] = Highlighter.get_selected_annotations(3);
      // var evidence = JSON.parse(localStorage.getItem('annotations'));
      evidence1 = JSON.stringify(evidence1);
      details1 = JSON.stringify(details1);
      evidence2 = JSON.stringify(evidence2);
      details2 = JSON.stringify(details2);
      evidence3 = JSON.stringify(evidence3);
      details3 = JSON.stringify(details3);
      var search = JSON.parse(localStorage.getItem('search'));
      search = JSON.stringify(search);
      var hyperlinks = JSON.parse(localStorage.getItem('hyperlinks'));
      hyperlinks = JSON.stringify(hyperlinks);
      var order = JSON.parse(localStorage.getItem('order'));
      //order = JSON.stringify(order);
      var page_search = JSON.parse(localStorage.getItem('page_search'));
      page_search = JSON.stringify(page_search);

      // var questions_form = $(".generated-claim-question");//.text().split(",");
      // var questions = [];
      // for (var i = 0; i < questions_form.length; i++) {
      //   var q_text = $(questions_form[i]).val()
      //   if (q_text !=''){
      //     questions.push(q_text);}
      //   }
      //   var answers_form = $(".generated-claim-answer");//.text().split(",");
      //   var answers = [];
      //   for (var i = 0; i < answers_form.length; i++) {
      //     var a_text = $(answers_form[i]).val();
      //     if (a_text != ''){
      //       answers.push(a_text);}
      //     }
      //     var questions_enough =  $( "#question-enough-selector option:selected").text();
      //     if (answers.length != questions.length){
      //       alert("The number of given questions does not match the number of answers! Please give an answer for every question and vice versa.");
      //       return
      //     }else if (questions.length === 0){
      //       $( "#generated-question1").attr('style', "border-radius: 5px; border:#FF0000 1px solid;");
      //       return;
      //     }
      //     else if (questions_enough == 'Nothing selected'){
      //       $("#question-enough-selector").parent().addClass('border border-danger');
      //       return;
      //     }
      //     else{
      //       questions.push('[ENOUGH] ' + questions_enough);
      //       answers.push('[ENOUGH] ' + questions_enough);
      //     }
      //
      //     questions = JSON.stringify(questions);
      //     answers = JSON.stringify(answers);

      questions = JSON.stringify(['NA']);
      answers = JSON.stringify(['NA']);

      var verdict = $( "#evidence-annotation-verdict-selector option:selected").text();
      console.log(verdict);
      var challenge_el = $("#evidence-annotation-challenge-selector option:selected");//.text().split(",");
      var challenge = [];
      for (var i = 0; i < challenge_el.length; i++) {
        challenge.push($(challenge_el[i]).text());
      }
      console.log(verdict);
      console.log(challenge);
      challenge = JSON.stringify(challenge);
      if (verdict == 'Nothing selected'){
        $("#evidence-annotation-verdict-selector").parent().addClass('border border-danger');//parent().parent().attr('style', "border-radius: 5px; border:#FF0000 1px solid;");
      }
      // else if (evidence1 == '[]' && evidence2 == '[]' && evidence3 == '[]'){
      //   $(".annotated-evidence-div").addClass('border border-danger');
      // }
      else if(evidence1 == evidence2  && evidence2 == evidence3 && evidence1 != '[]' && evidence1 !== 'null'){
        alert('All evidence sets are identical. Please do not submit identical annotation sets!');
      }
      else if (challenge == '[]' | challenge == '[""]'){
        $( "#evidence-annotation-challenge-selector").parent().addClass('border border-danger');
      }
      else{
        if (evidence1 == 'null'){
          evidence1 = JSON.stringify([]);
          details1 = JSON.stringify([]);
        }
        order.push('finish');
        order= JSON.stringify(order);
        var times = JSON.parse(localStorage.getItem('times'));
        times.push(new Date().getTime());
        times = times.map(function(element){
          return ((parseInt(element) - parseInt(times[0])) / 1000).toString();
        });
        var total_time = times[times.length-1];
        times = JSON.stringify(times);

        var submission_dict =   { user_id: Processor.user_id, claim_id: Processor.claim_id, evidence1: evidence1, details1: details1, evidence2: evidence2, details2: details2, evidence3: evidence3, details3: details3, verdict: verdict, challenge: challenge, search: search, hyperlinks: hyperlinks, order: order, page_search: page_search, times: times, total_time:total_time, questions:questions, answers:answers}

        console.log(submission_dict);

        return submission_dict;
      }
    }

    $(document.body).on('click', '.evidence-annotation-resubmit-button', function(event) {
      var submission_dict = prepare_submission();
      if (submission_dict == null){
        return;
      }

      submission_dict.request = 'evidence-resubmission'


      $.post('annotation-service/evidence_annotation_api.php',submission_dict,
      function(data,status,xhr){
        if(status !='success'){
          alert("Some error while communicating with the server... Please note the associated claim down and the time it occured.")
        }
          Processor.reset_evidence_menu();
          localStorage.setItem('back-counter', 0);
          Processor.get_next_claim_for_evidence_annotation();
            $(document.body).find(".evidence-annotation-resubmit-button").replaceWith('<button class="evidence-annotation-submit-button fa fa-check btn btn-success"> Submit Annotation </button>');
        }
      ,'text');
    });

    $(document.body).on('click', '.evidence-annotation-submit-button', function(event) {
      var submission_dict = prepare_submission();
      if (submission_dict == null){
        return;
      }
      submission_dict.request = 'evidence-submission';

      $.post('annotation-service/evidence_annotation_api.php', submission_dict,
      function(data,status,xhr){
        if(status !='success'){
          alert("Some error while communicating with the server... Please note the associated claim down and the time it occured.")
        }
        Processor.reset_evidence_menu();
        localStorage.setItem('back-counter', 0);
        Processor.get_next_claim_for_evidence_annotation();
      }
      ,'text');
    });

    $(document.body).on('click', '.report-item', function(event) {
      if($(this).hasClass("active")){
        $(this).removeClass("active");
        // $(this).selectpicker("refresh");
      }else{
        $(this).addClass("active");
      }
    });

    $(document.body).on('click', '#go-back', function(event) {
      [evidence1, details1] = Highlighter.get_selected_annotations(1);
      [evidence2, details2] = Highlighter.get_selected_annotations(2);
      [evidence3, details3] = Highlighter.get_selected_annotations(3);
      var back_counter = localStorage.getItem('back-counter');
      console.log(back_counter)
      if( back_counter == 0 && (evidence1 != null && evidence1.length > 0 || evidence2 != null && evidence2.length > 0 || evidence3 !=null && evidence3.length > 0)){
        alert('Cannot go back to other claims during annotation! Finish your current annotation to move back to other claims.')
        return;
      }

      $.get('annotation-service/evidence_annotation_api.php', {user_id: Processor.user_id, request: 'reload-evidence',
      back_count:back_counter},function(data,status,xhr){
        if (status == 'error'){
          alert('Server problem');
        }
        if(data[0] != -1){
          var claim_id = data[0];
          var claim = data[1];
          var verdict = data[2];
          if (data[3] == null || data[3][0] == "" || data[3] == ""){
            var evidence1 = [];
            var details1 = [];
          }else{
              var evidence1 = data[3].split(" [SEP] ");
              var details1 = data[4].split(" [SEP] ");
          }

          if (data[5] == null || data[5][0] == "" || data[5] == ""){
            var evidence2 = [];
            var details2 = [];
          }else{
              var evidence2 = data[5].split(" [SEP] ");
              var details2 = data[6].split(" [SEP] ");
          }

          if (data[7] == null || data[7][0] == "" || data[7] == ""){
            var evidence3 = [];
            var details3 = [];
          }else{
              var evidence3 = data[7].split(" [SEP] ");
              var details3 = data[8].split(" [SEP] ");
          }

          // var evidence3 = data[7].split(" [SEP] ")
          // if (evidence3[0] == [""]){
          //   evidence3 = [];
          //   var details3 = [];
          // }else{
          //   var details3 = data[8].split(" [SEP] ");
          // }
          if (data[9] != null){
            var search = data[9].split(" [SEP] ");
          }else{
            var search = null;
          }
          if (data[10] != null){
            var hyperlinks = data[10].split(" [SEP] ");
          }else{
            var hyperlinks = null;
          }
          var search_order = data[11].split(" [SEP] ");
          if (data[12] != null){
            var page_search = data[12].split(" [SEP] ");
          }else{
            var page_search = null;
          }
          var total_annotation_time = data[13].split(" [SEP] ");
          if (data[14] != null){
            var annotation_time_events = data[14].split(" [SEP] ");
          }else{
            var annotation_time_events = null;
          }
          var challenges = data[15].split(" [SEP] ");
          var questions = data[16].split(" [SEP] ");
          var answers = data[17].split(" [SEP] ");

          Processor.reset_evidence_menu();

          var evidence = {1: evidence1, 2: evidence2, 3: evidence3};
          var details = {1: details1, 2: details2, 3:details3};

          localStorage.setItem('annotations', JSON.stringify(evidence));
          localStorage.setItem('details', JSON.stringify(details));

          [evidence, details] = Highlighter.get_annotations();


          console.log(evidence)
          for (var i = 0; i < evidence.length; i++) {
            add_evidence_to_interface(evidence[i].replaceAll(' ', '-'), details[i]);
          }

          if (evidence.length > 0){
          $("#my-wikipedia").prop('src', base_url + evidence[0].split('_')[0]);
          }
          Highlighter.init()


          localStorage.setItem("search", JSON.stringify(search));
          localStorage.setItem("hyperlinks", JSON.stringify(hyperlinks));
          localStorage.setItem("page-search", JSON.stringify(page_search));
          localStorage.setItem("order", JSON.stringify(search_order));
          localStorage.setItem('times', JSON.stringify(annotation_time_events));

          Processor.claim_id = claim_id;
          Processor.claim_text = claim;

          console.log(parseInt(localStorage.getItem('back-counter')));
          var back_counter = parseInt(localStorage.getItem('back-counter')) + 1;
          localStorage.setItem('back-counter', back_counter);
          localStorage.setItem("jump-url", 0);
          $("#evidence-annotation-verdict-selector").val(verdict);
          $("#evidence-annotation-verdict-selector").selectpicker("refresh");
          $("#evidence-annotation-challenge-selector").val(challenges);
          $("#evidence-annotation-challenge-selector").selectpicker("refresh");
          $('#current-claim').text(claim);

          $(document.body).find(".evidence-annotation-submit-button").replaceWith('<button class="evidence-annotation-resubmit-button fa fa-refresh btn btn-primary"> Resubmit Annotation </button>');


          // $("#question-enough-selector").val('default');
          // $("#question-enough-selector").selectpicker('refresh');
          // $(".report-item").removeClass('active');
          // $('#report-note').prop('value', '');
          // $('.generated-claim-question').prop('value','');
          // $('.generated-claim-answer').prop('value', '');

          $('#go-forward').prop('disabled', false);
        }else{
          alert('No previously annotated evidence found.');
        }
      }, 'json');
    });

    $(document.body).on('click', '#go-forward', function(event) {
      var back_counter = localStorage.setItem('back-counter', 0);
      Processor.reset_evidence_menu();
      localStorage.setItem('back-counter', 0);
      location.reload();
    });


    $(document.body).on('click', '#report-button', function(event) {
      var active_text = [];
      tags = $('.report-item');
      for(var i = 0; i < tags.length; i++){
        if ($(tags[i]).hasClass("active")){
          active_text.push($(tags[i]).text());
        }
      }
      var custom_note = $('.dropdown-item#report-note').val();
      active_text.push(custom_note);
      active_text = JSON.stringify(active_text);
      if (active_text == '[""]'){
        alert('Please specify why you want to report this claim.');
      }else{
        $.post('annotation-service/evidence_annotation_api.php', { user_id: Processor.user_id, claim_id: Processor.claim_id, request: "report-claim", report_text: active_text},
        function(data,status,xhr){
          Processor.reset_evidence_menu();
          Processor.get_next_claim_for_evidence_annotation();
        }
        ,'text');
      }});

      $(document.body).on('click', '.evidence-delete-button', function(event) {
        id = $(this).parent().text().split(' ')[0];
        Highlighter.evidence_highlighter_delete(id);
        if (id.indexOf('\\') >=0){
          $('#' + id + '.evidence-element').remove();
        }
        else{
          var ele_trans = id.replaceAll('.', '\\.').replaceAll('(', '\\(').replaceAll(')', '\\)').replaceAll("'", "\\'").replaceAll('&', '\\&').replaceAll('!', '\\!').replaceAll('?', '\\?');
          $('#' + ele_trans + '.evidence-element').remove();
        }
        //console.log(ele_trans);
      });
      $(document.body).on('click', '.evidence-set', function(event) {
        $('body').find('button').filter(function() {
          Highlighter.undraw_all_annotations();
          $('.evidence-element').remove();
          var id = $(this).attr('id');
          if(id != null && id.slice(-1) == Highlighter.get_active_annotation_set()){
            $(this).removeClass('btn-outline-danger');
          }
        });
        var set_id = $(this).attr('id').slice(-1);
        localStorage.setItem('active_annotation_set', set_id);
        $(this).addClass('btn-outline-danger');
        Highlighter.apply_to_all_elements(Highlighter.redraw_annotations);
        var evidence, details = [];
        [evidence, details] = Highlighter.get_annotations();
        if (evidence != null){
          for (var i = 0; i < evidence.length; i++) {
            add_evidence_to_interface(evidence[i].replaceAll(' ', '-'), details[i]);
          }
        }
      });
    }
  });

  class Processor {

    static init(){

      console.log("INIT");
      //Variables loaded from localStorage
      Processor.annotation_type = localStorage.getItem('annotation-type');
      Processor.user_id = localStorage.getItem('user');

      var evidence, details = [];
      [evidence, details] = Highlighter.get_annotations();
      // var evidence = JSON.parse(localStorage.getItem('annotations'));
      // var details = JSON.parse(localStorage.getItem('details'));
      var search = JSON.parse(localStorage.getItem('search'));
      var hyperlinks = JSON.parse(localStorage.getItem('hyperlinks'));

      localStorage.setItem("order", JSON.stringify(['start']));
      localStorage.setItem('times', JSON.stringify([new Date().getTime()]));
      localStorage.setItem('back-counter', 0);
      $('#go-forward').prop('disabled', true);

      Processor.claim_id = null;
      Processor.claim_text = null;

      Processor.get_next_claim_for_evidence_annotation();

      if (evidence != null){
        for (var i = 0; i < evidence.length; i++) {
          add_evidence_to_interface(evidence[i].replaceAll(' ', '-'), details[i]);
        }
      }
      // if (search != null){
      //   for (var i = 0; i < search.length; i++) {
      //     Processor.add_search_to_interface(search[i]);
      //   }
      // }
      // if (hyperlinks != null){
      //   for (var i = 0; i < hyperlinks.length; i++) {
      //     Processor.add_hyperlink_to_interface(hyperlinks[i]);
      //   }}
    }

    static reload_elements(){

      var iframeDoc = $("#my-wikipedia")[0].contentWindow.document;
      Processor.doc = iframeDoc;
      //var $jqObject = $(iframeDoc).find("body");

      $(iframeDoc).find('#mw-indicator-mw-helplink').remove();
      $(iframeDoc).find('.mw-editsection').remove();
      $(iframeDoc).find('#mw-search-top-table').hide();
      //$(iframeDoc).find('#mw-head').hide();
      $(iframeDoc).find('.mw-search-profile-tabs').remove();
      $(iframeDoc).find('#mw-indicator-mw-helplink').remove();

      Processor.adjust_searchbar();
      $(Processor.doc).find('#p-search').append("<input type='text' id='page-search' placeholder='Page search'>");

      if (localStorage.getItem('first-load') == 'false') {
        localStorage.setItem('last-url', $("#my-wikipedia")[0].contentWindow.location.href);
      }else{
        localStorage.setItem('first-load', 'false');
      }
      setTimeout(function(){$('#my-wikipedia').css('visibility', 'visible');}, 100);
      $(Processor.doc).find('body').hide(0).show(0);
      //localStorage.setItem("jump-url", 0);

      Highlighter.init();
      Processor.add_search_listeners();
    }

    static add_search_listeners(){

      $(Processor.doc).on('click', '.searchButton', function(event){
        var search_text = $(Processor.doc).find('#searchInput').val();
        // Processor.add_search_to_interface(search_text);
        Processor.log_search(search_text);
        $('#my-wikipedia').css('visibility', 'hidden');
      });


      $(Processor.doc).on('click', '.suggestions-result', function(event){
        var search_text = $(Processor.doc).find('#searchInput').val();
        // Processor.add_search_to_interface(search_text);
        Processor.log_search(search_text);
        $('#my-wikipedia').css('visibility', 'hidden');
      });

      $(Processor.doc).on('click', 'a', function(event){
        var href = $(this).attr("href");
        var check = $(this).attr("class");
        // console.log(check);
        if(href!= null && check != 'mw-searchSuggest-link'){
          var href_text = $(this).text();
          Processor.add_hyperlink_to_interface(href_text);
          Processor.log_hyperlinks(href_text);
          //$('#my-wikipedia').css('visibility', 'hidden');
          // setTimeout(function(){$('#my-wikipedia').css('visibility', 'visible');}, 100);
          //  $(Processor.doc).find('body').hide(0).show(0);
        }
      });

      $(Processor.doc).on('keypress', '.searchButton', (function (e) {
        if (e.which == 13) {
          var search_text = $('#searchInput').val();
          // Processor.add_search_to_interface(search_text);
          Processor.log_search(search_text);
          $('#my-wikipedia').css('visibility', 'hidden');
        }
      }));

      // $("#my-wikipedia")[0].contentWindow.document;
      $(Processor.doc).find("#page-search").on('keypress', function(e) {
        var page_search = JSON.parse(localStorage.getItem('page_search'));
        var order = JSON.parse(localStorage.getItem('order'));
        if (e.which == 13) {
          var v = $(this).val();
          $(Processor.doc).find(".results").css('background','#ffffff');
          $(Processor.doc).find(".results").removeClass("results");
          if(v!='') {
            if (page_search == null){
              page_search = [];
            }
            page_search.push(v);
            if (order == null){
              order = [];
            }
            order.push('page-search');
            localStorage.setItem("page_search", JSON.stringify(page_search));
            localStorage.setItem("order", JSON.stringify(order));
            $(Processor.doc).find(Highlighter.elements).each(function () {
              if (v != "" && $(this).text().search(new RegExp(v,'gi')) != -1) {
                $(this).addClass("results");
                $(Processor.doc).find(".results").css('background', '#7b8596');
                // color: white;addClass("results");
              }
            });
          }
          var times = JSON.parse(localStorage.getItem('times'));
          var order = JSON.parse(localStorage.getItem('order'));
          order.push('Page search: ' + v);
          times.push(new Date().getTime());
          localStorage.setItem('times', JSON.stringify(times));
          localStorage.setItem("order", JSON.stringify(order));
        }
      });

    }

    static add_search_to_interface(element){
      //text =  '<input type="text" class="search-term-element" value= ' + element + '> ';
      var text =  '<p class="search-term-element"> Search: ' + element + '</p> ';
      $(".search-terms-annotation-div").append(text);
    }

    static add_hyperlink_to_interface(element){
      //text =  '<input type="text" class="search-term-element" value= ' + element + '> ';
      var text =  '<p class="search-term-element"> Hyperlink: ' + element + '</p> ';
      $(".search-terms-annotation-div").append(text);
    }

    static adjust_searchbar(){
      var ele = $(Processor.doc).find('#p-search');
      ele.prependTo($(Processor.doc).find('body'));
      ele.css("position", "relative");
      ele.css("left", "75%");
      ele.css("top", "15%");

      $(Processor.doc).find('#mw-head').remove();

    }

    static log_search(element){
      var search = JSON.parse(localStorage.getItem('search'));
      var order = JSON.parse(localStorage.getItem('order'));
      var times = JSON.parse(localStorage.getItem('times'));
      if (search == null){
        search = [];
      }
      search.push(element);
      order.push('search: ' + element);
      times.push(new Date().getTime());

      localStorage.setItem('times', JSON.stringify(times));
      localStorage.setItem("search", JSON.stringify(search));
      localStorage.setItem("order", JSON.stringify(order));
    }

    static log_hyperlinks(element){
      var hyperlinks = JSON.parse(localStorage.getItem('hyperlinks'));
      var order = JSON.parse(localStorage.getItem('order'));
      var times = JSON.parse(localStorage.getItem('times'));
      if (hyperlinks == null){
        hyperlinks = [];
      }
      hyperlinks.push(element);
      order.push('hyperlink: ' + element);
      times.push((new Date().getTime()));

      localStorage.setItem('times',  JSON.stringify(times));
      localStorage.setItem("hyperlinks", JSON.stringify(hyperlinks));
      localStorage.setItem("order", JSON.stringify(order));
    }


    static get_next_claim_for_evidence_annotation(){
      $.get('annotation-service/evidence_annotation_api.php', { user_id: Processor.user_id, request: 'next-claim'},function(data,status,xhr){
        if (status != 'success'){
          alert("Some error while communicating with the server... Please note the associated claim down and the time it occured.");
        }else{
          if (data[0] === 'finished-calibration'){
            window.location.replace("calibration_evaluation.php");
          }
          Processor.claim_id = data[0];
          Processor.claim_text = data[1];
          $('#current-claim').text(Processor.claim_text);
        }
        $('.login-input').attr('style', "border-radius: 5px; border:#FF0000 1px solid;");
      }, 'json');

      var jump_url = localStorage.getItem("jump-url");
      if (jump_url == 0){
        //window.location.href = data_url;
        $("#my-wikipedia").prop('src', base_url + '?search=');
        localStorage.setItem("jump-url", 1);
      }

    }


    static reset_evidence_menu(){
      $('.evidence-element').remove();
      Highlighter.undraw_all_annotations();
      Highlighter.reset_annotations();
      $('.search-term-element').remove();
      localStorage.setItem("search", null);
      localStorage.setItem("hyperlinks", null);
      localStorage.setItem("page-search", null);
      localStorage.setItem("order", JSON.stringify(['start']));
      localStorage.setItem('times', JSON.stringify([new Date().getTime()]));
      //localStorage.setItem('first-load', true);
      localStorage.setItem("jump-url", 0);
      $('#go-forward').prop('disabled', true);
      //localStorage.setItem("jump-url", 0);
      $("#evidence-annotation-verdict-selector").val('default');
      $("#evidence-annotation-verdict-selector").selectpicker("refresh");
      $("#evidence-annotation-challenge-selector").val('default');
      $("#evidence-annotation-challenge-selector").selectpicker("refresh");

      $('#current-claim').text('Nothing fetched.');
      $("#question-enough-selector").val('default');
      $("#question-enough-selector").selectpicker('refresh');

      $(".report-item").removeClass('active');

      $('#report-note').prop('value', '');

      $('.generated-claim-question').prop('value','');
      $('.generated-claim-answer').prop('value', '');
      //  $( "#dropdown-toggle option:contains('Nothing selected')").prop('selected',true);//text('Choose here');
      //$(".option").removeClass('active');
      //$( "#evidence-annotation-verdict-selector").prop('value',null);//text('Choose here');
      //localStorage.setItem("jump-url", 0);
    }

  }

  function add_evidence_to_interface(element, details){
    var text = '<span class="evidence-element" id="' +  element + '">';
    text += '<details>';
    text += "<summary>" + element +'<button style="float:right; font-size:12px" class="evidence-delete-button btn btn-sm btn-danger"> delete </button> </summary>';
    text +=  '<p class="evidence-details">' + details + '</p>';
    text += "</details>";
    // text = '<label for="evidence-element">' + element + '</label>';
    var element_trans = element.replaceAll('(', '\\(').replaceAll(')', '\\)').replaceAll("'", "\\'").replaceAll('.', '\\.').replaceAll('&', '\\&').replaceAll('!', '\\!').replaceAll('?', '\\?');
    if (element.indexOf('\\') >=0){
      text += "<hr width=" + $('#' + element).css("width") + '\%>';
    }else{
      text += "<hr width=" + $('#' + element_trans).css("width") + '\%>';
    }
    text += '</span>';
    $(".annotated-evidence-div").append(text);
    return text
  }
