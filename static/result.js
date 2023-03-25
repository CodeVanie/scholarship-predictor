const submitButton = document.getElementById('btnButton');

const form = document.getElementById('modelform');

submitButton.addEventListener('click', function(){
    form.submit();
});

function ShowResult(){
    $('#ShowResultModal').modal('show');
}