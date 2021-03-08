//$(document).on('click', 'p', function() {alert("rect clicked");})
//var annotations = [];
// if (annotations.length != details.length){
//   console.log("Wot");
// }

class Highlighter {
  constructor(){}

  static init(){

  Highlighter.doc = $("#my-wikipedia")[0].contentWindow.document;
 Highlighter.title = $(Highlighter.doc).find('#firstHeading').text()//.replaceAll(' ','-')//.replaceAll('(', '\\(').replaceAll(')', '\\)').replaceAll("'", "\\'").replaceAll('.', '\\.');
 if(Highlighter.title != 'Search-results' &&  Highlighter.title != 'Search'){
    $(Highlighter.doc).find('#firstHeading').append('<span style="visibility: hidden;font-size:1px">' + Highlighter.title + '_title</span>');
 }

  $('.evidence-set').removeClass('btn-outline-danger');
  localStorage.setItem("active_annotation_set", 1);
  $('body').find('button').filter(function() {
    var id = $(this).attr('id');
    if(id != null && id.slice(-1) == Highlighter.get_active_annotation_set()){
      $(this).addClass('btn-outline-danger');
    }
  });

  // Highlighter.apply_to_all_elements(Highlighter.highlight);
  // Highlighter.apply_to_all_elements(Highlighter.mouseover_highlight_in);
  // Highlighter.apply_to_all_elements(Highlighter.mouseover_highlight_out);
  // Highlighter.apply_to_all_elements(Highlighter.redraw_annotations);


  Highlighter.identifier = ['_title', '_sentence_', '_cell_', '_item_', '_section_', 'table_caption', '_sentence_in_table_', '_item_in_table_'];
  Highlighter.elements = 'h1, h2, h3, h4, h5, p, li, caption, td, th';
  // Highlighter.elements_list = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li', 'caption', 'td', 'th'];
  // Highlighter.identifier_list = ['_title', '_section_', '_section_','_section_','_section_', '_sentence_', '_item_',  'table_caption', '_cell_', '_sentence_in_table_', '_item_in_table_'];


  Highlighter.mouseover_highlight_in();
  Highlighter.mouseover_highlight_out();
  Highlighter.highlight();

  Highlighter.apply_to_all_elements(Highlighter.redraw_annotations);
  Highlighter.apply_to_all_elements(Highlighter.mouseover_highlight_in)
  Highlighter.apply_to_all_elements(Highlighter.mouseover_highlight_out)
  Highlighter.apply_to_all_elements(Highlighter.mouseover_highlight_out)
  Highlighter.apply_to_all_elements(Highlighter.highlight)
  }

  static redraw_annotations(type, identifier){
    var annotations, details = [];
     [annotations, details] = Highlighter.get_annotations();
      if (annotations != null){
     for (var i = 0; i < annotations.length; i++) {
         $(Highlighter.doc).find(type).filter(function() {
           var raw_id= $(this).find("span").text();
            if(identifier.includes('_section_')){
          var is_right = Highlighter.title + '_section_' +  raw_id.substring(raw_id.lastIndexOf("_") + 1,  raw_id.length) === annotations[i];
        }else if(raw_id.includes("_cell_") &&  raw_id.includes("_item_in_table_")){
           var raw_id= $(this).find("span").text();
            var is_right = Highlighter.title + raw_id.split(Highlighter.title)[1] == annotations[i];
        }
        else{
           var is_right = raw_id === annotations[i];
         }
          if (is_right){
           $(this).css( "background-color", 'yellow').css('outline', '2px solid black');//css('border', '2px solid black');
         }
        //.find("span").text());//.css( "background-color", 'yellow').css('border', '2px solid black');
     });
     }// $(type).filter(function() { return $(this).find("span").text() === annotations[i];}).css( "background-color", 'yellow');
   }
 }//
 //    var annotations, details = [];
 //     [annotations, details] = Highlighter.get_annotations();
 //      if (annotations != null){
 //     for (var i = 0; i < annotations.length; i++) {
 //       for (var j = 0; j < Highlighter.identifier.length; j++) {
 //         $(Highlighter.elements_list[j]).filter(function() {
 //           if(Highlighter.identifier[j].includes('_section_')){
 //             onsole.log('ya');
 //         var is_right = Highlighter.title+ '_section_' +  $(this).find("span").text().substring($(this).find("span").text().lastIndexOf("_") + 1,  $(this).find("span").text().length) === annotations[i];
 //       }else{
 //          var is_right = $(this).find("span").text() === annotations[i];
 //        }
 //          if (is_right){
 //           console.log($(this).find("span").text());
 //           $(this).css( "background-color", 'yellow').css('border', '2px solid black');
 //         }
 //        //.find("span").text());//.css( "background-color", 'yellow').css('border', '2px solid black');
 //     });
 //     }// $(type).filter(function() { return $(this).find("span").text() === annotations[i];}).css( "background-color", 'yellow');
 //   }
 // }
 //     }//
       // $(type + ':contains(' + annotations[i] +  ')').css('border', '2px solid black');

  static apply_to_all_elements(func){
  func('h1', '_title');
  func('p', '_sentence');
  func('td', '_cell_');
  func('th', '_cell_');
  func('li', '_item_');
  func('dt', '_item_');
  func('h2', '_section_');
  func('h3', '_section_');
  func('h4', '_section_');
  func('h5', '_section_');
  func('caption', 'table_caption');
  func('p', '_sentence_in_table_');
  func('li', '_item_in_table_');

  }


static undraw_all_annotations(){
  Highlighter.apply_to_all_elements(Highlighter.undraw_annotations);
}

// static destroy(){
//   Highlighter.undraw_all_annotations();
//   Highlighter.apply_to_all_elements(Highlighter.unbind_element);
// }

static unbind_element(element){
  $(element).unbind();
}

static undraw_annotations(type, identifier){
  var annotations, details = [];
   [annotations, details] = Highlighter.get_annotations();
    if (annotations != null){
   for (var i = 0; i < annotations.length; i++) {
      $(Highlighter.doc).find(type).filter(function() {
        var raw_id= $(this).find("span").text();
        if(identifier.includes('_section_')){
       var is_right = Highlighter.title + '_section_' +  raw_id.substring(raw_id.lastIndexOf("_") + 1,  raw_id.length) === annotations[i];
     }
     else{
        var is_right = raw_id === annotations[i];
      }
        if (is_right){
         $(this).css( "background-color", '').css('outline', 'none');//.css('border', '');
       }
      //.find("span").text());//.css( "background-color", 'yellow').css('border', '2px solid black');
   });
   }// $(type).filter(function() { return $(this).find("span").text() === annotations[i];}).css( "background-color", 'yellow');
 }
}//


static substring_in_list(list, string){
    length = list.length;
while(length--) {
   if (string.indexOf(list[length])!=-1) {
      return true;
       // one of the substrings is in yourstring
   }
}
return false;
}

 static evidence_highlighter_delete(id){
   var annotations, details = [];
   [annotations, details] = Highlighter.get_annotations();
   $(Highlighter.doc).find(Highlighter.elements).filter(function() {
     var raw_id= $(this).find("span").text();
     if(id.includes('_section_')){
       var is_right = Highlighter.title + '_section_' +  raw_id.substring(raw_id.lastIndexOf("_") + 1,  raw_id.length) === id;
     }else{
        is_right = raw_id === id;
      }
      if (is_right){
       $(this).css( "background-color", '').css('outline', 'none');//.css('border', '');
     }
   });

   const index = annotations.indexOf(id);
   annotations.splice(index, 1);
   details.splice(index, 1);
   Highlighter.set_annotations(annotations, details)

   var times = JSON.parse(localStorage.getItem('times'));
   var order = JSON.parse(localStorage.getItem('order'));
   order.push('Highlighting deleted: ' + id);
   times.push(new Date().getTime());
   localStorage.setItem('times', JSON.stringify(times));
   localStorage.setItem("order", JSON.stringify(order));
 }

  static reset_annotations(){
    localStorage.setItem("annotations", null);
    localStorage.setItem("details", null);
    return [[], []];
  }

  static get_active_annotation_set(){
    var ann = localStorage.getItem('active_annotation_set');
    if (ann == null){
      localStorage.setItem('active_annotation_set', 1);
      ann = 1;
    }
    return ann;
  }

  static get_annotations(){
   var annotations = JSON.parse(localStorage.getItem('annotations'))
   var details = JSON.parse(localStorage.getItem('details'))
   if(annotations != null){
    annotations =  annotations[localStorage.getItem('active_annotation_set')];
    details = details[localStorage.getItem('active_annotation_set')];
  }
 return [annotations, details];
 }

 static get_selected_annotations(index){
  var annotations = JSON.parse(localStorage.getItem('annotations'))
  var details = JSON.parse(localStorage.getItem('details'))
  if(annotations != null){
   annotations =  annotations[index];
   details = details[index];
 }
return [annotations, details];
}


  static set_annotations(annotations, details){
    var index = Highlighter.get_active_annotation_set();
    var annotations_full = JSON.parse(localStorage.getItem('annotations'));
    var details_full = JSON.parse(localStorage.getItem('details'));
    if (annotations_full == null){
      annotations_full = {1: [], 2:[], 3:[]};
      details_full = {1:[], 2:[], 3:[]};
    }
    annotations_full[index] = annotations;
    details_full[index] = details;
    localStorage.setItem("annotations", JSON.stringify(annotations_full));
    localStorage.setItem("details", JSON.stringify(details_full));
  }

  static highlight(type, identifier){
    $(Highlighter.doc).on('click', type, function(event) {
      event.stopPropagation();
      if(!$(event.target).closest('a').length){ // Skips annotation if clicked on href
      var id_span =$(this).find("span");
      var id = id_span.text();
      if (id.includes("_section_")){ //breaks down section since include edit text
        id = Highlighter.title+ '_section_' +  id.substring(id.lastIndexOf("_") + 1,  id.length);
      }
      else if(id.includes("_cell_") &&  id.includes("_item_in_table_")){
        id = Highlighter.title + id.split(Highlighter.title)[1];
      }
      if (id.includes(identifier)){ //check whether the identifier is included in id
      //if (Highlighter.substring_in_list(Highlighter.identifier,id)){ //check whether the identifier is included in id
        var annotations, details = [];
        [annotations, details] = Highlighter.get_annotations();
        if (annotations === null){
          [annotations, details] = Highlighter.reset_annotations();
        }
        if (!annotations.includes(id)){
          if (id.includes("_section_")){
            var detail = id_span.text();
            var comb = (id + id);
            detail = detail.substring(0, detail.indexOf(id + id));
          }else{
          var detail = id_span.parent().text(); //TODO ADD LIST ID TO LISTS IN TABLES!!!!
          detail = detail.substring(0, detail.indexOf(id));
          }
          annotations.push(id);
          details.push(detail);
          add_evidence_to_interface(id.replaceAll(' ', '-'), detail); // The calling process is weird. change.
          $( this ).css( "background-color", 'yellow');
          $( this ).css('outline', '2px solid black');//css('border', '2px solid black');

          //BAD STYLE should be in evidence_annotation but oh welll.....
          var times = JSON.parse(localStorage.getItem('times'));
          var order = JSON.parse(localStorage.getItem('order'));
          order.push('Highlighting: ' + id);
          times.push(new Date().getTime());
          localStorage.setItem('times', JSON.stringify(times));
          localStorage.setItem("order", JSON.stringify(order));


        }else{
          $( this ).css( "background-color", '');
          $( this ).css('outline', '2px solid black');//.css('border', '');
          const index = annotations.indexOf(id);
          annotations.splice(index, 1);
          details.splice(index, 1);
          var element_trans =  id.replaceAll(' ', '-').replaceAll('.', '\\.').replaceAll('(', '\\(').replaceAll(')', '\\)').replaceAll("'", "\\'").replaceAll('&', '\\&').replaceAll('!', '\\!').replaceAll('?', '\\?');
          if (id.indexOf('\\') >=0){
            $("#" + id +  '.evidence-element').remove();
          }else{
          // console.log(element_trans);
         $("#" + element_trans.replaceAll(' ', '-') +  '.evidence-element').remove();
       }

         var times = JSON.parse(localStorage.getItem('times'));
         var order = JSON.parse(localStorage.getItem('order'));
         order.push('Highlighting deleted: ' + id);
         times.push(new Date().getTime());
         localStorage.setItem('times', JSON.stringify(times));
         localStorage.setItem("order", JSON.stringify(order));

        }
        Highlighter.set_annotations(annotations, details)
      }
    }
    })
    }


  static mouseover_highlight_in(type, identifier){
    $(Highlighter.doc).on('mouseover',  type, function(event) {
      //console.log('hi')
      var id = $(this).find("span").text();
    if (id.includes(identifier)){
     //if (Highlighter.substring_in_list(Highlighter.identifier,id)){
        //$(this).css('border', '2px solid black');
        $(this).css('outline', '2px solid black');
        //$(this).addClass('highlight-candidate');
      }
    })
    }

 static mouseover_highlight_out(type, identifier){
    $(Highlighter.doc).on('mouseout',  type, function(event) {
      var id = $(this).find("span").text();
       //alert($(this).css("background-color"))
       if (id.includes(identifier) && $(this).css("background-color") != 'rgb(255, 255, 0)'){ //yellow
        // $(this).css('border','none');
          $(this).css('outline', 'none');
      }
    })
    }

}
