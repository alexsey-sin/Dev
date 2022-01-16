// var asyncSuccessMessage = [
//     "<div ",
//     "style='position:fixed;top:0;z-index:10000;width:100%;border-radius:0;' ",
//     "class='alert alert-icon alert-success alert-dismissible fade show mb-0' role='alert'>",
//     "Success: Book was updated.",
//     "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>",
//     "<span aria-hidden='true'>&times;</span>",
//     "</button>",
//     "</div>",
//     "<script>",
//     "$('.alert').fadeTo(2000, 500).slideUp(500, function () {$('.alert').slideUp(500).remove();});",
//     "<\/script>",
// ].join();
// document.querySelector("#update-book").onclick = function(){
//     // modalForm({formURL: "{% url 'app:create_book' %}"});
//     // alert("Вы нажали на кнопку");
//     $(this).modalForm({
//         formURL: $(this).data("form-url"),
//         asyncUpdate: true,
//         asyncSettings: {
//           closeOnSubmit: false,
//           successMessage: asyncSuccessMessage,
//           dataUrl: "books/",
//           dataElementId: "#books-table",
//           dataKey: "table",
//           addModalFormFunction: updateBookModalForm,
//         }
//       });
// }
// $(document).ready(function() {

//     $("#create-book").modalForm({
//         formURL: "{% url 'app:create_book' %}"
//     });

// });
// $(function () {

    // # asyncSettings.successMessage

    // # asyncSettings.addModalFormFunction
    // function updateBookModalForm() {
    //   $("#update-book").each(function () {
    //     alert("Вы нажали на кнопку");
        // $(this).modalForm({
        //   formURL: $(this).data("form-url"),
        //   asyncUpdate: true,
        //   asyncSettings: {
        //     closeOnSubmit: false,
        //     successMessage: asyncSuccessMessage,
        //     dataUrl: "books/",
        //     dataElementId: "#books-table",
        //     dataKey: "table",
        //     addModalFormFunction: updateBookModalForm,
        //   }
        // });
    //   });
    // }
    // updateBookModalForm();

    // ...
// });
// $(document).ready(function(){
//     $(".btn").click(function() {
  
//      var id = this.id;
//      var userName = $('.editUser' + id).val();
  
  
//      $('#myModal .userId').data('id', id);
//      $('#myModal .userName').data('userName', value);
  
  
//      $("#myModal").modal('show');
//    });
//   });
// var $editRow = null;

// $(".edit").click(function(e){
//     alert("hhhh")
//     $editRow = $(this).closest("tr");
    
//     $("#uid").val($editRow.data('user-id'));
//     $("#uname").val($editRow.find(".uname").text());
    
//     $("#myModal").modal('show');
// });


// $("#save").click(function(){
//     $editRow.find(".uname").text( $("#uname").val() );
//     $(this).closest('.modal').modal('hide');
// });
function newVal(jjj){
    $("#myModal").modal('show');
    // alert("hhhh")
    // var res = $(t).attr('value');
    // $('#butOk').val(res); return false;
    $('#myModal .userId').val(jjj);
    // $('#myModal .userName').data('userName', value);
}
// function editRowNames(){
//     // document.getElementById('frameEditNames').modal('show');
//     alert("hhhh");
//     // $("#frameEditNames").modal('show');
//     // alert("hhhh")jjj, kkk '{{ row.text }}','{{ row.sex }}'
//     // var res = $(t).attr('value');
//     // $('#butOk').val(res); return false;
//     // $('#editFrame .text_name').val(text);
//     // $('#myModal .userId').val(jjj);
//     // $('#myModal .userName').data('userName', value);
//     // $('#editFrame .userName').data('userName', value);
// }
