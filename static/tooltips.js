<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(element){
        return new bootstrap.Tooltip(element);
    });
=======
document.addEventListener("DOMContentLoaded", function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(element){
        return new bootstrap.Tooltip(element);
    });
>>>>>>> 1c4bb1d554e1787639bd741b2ae2402151fd51a2
});