var thing = document.getElementsByTagName("form");
var body = document.getElementsByTagName("body");
var form = document.getElementsByTagName("input");
var count = 0;
var error = false;


form[0].addEventListener('focus', func);
form[0].addEventListener('focusout', unfunc);
function func(){
    body[0].classList.add("hello");
}
function unfunc(){
    body[0].classList.remove("hello");
}
function adderror(){
    body[0].classList.add("error");
}
function removerror(){
    body[0].classList.remove("error");
}
document.getElementById("button").addEventListener("click", function(event){
    error();
    displayDay();
});
function error(){
    if(form[0].value === ""){
        adderror()
    }else{
        removerror()
    }
}
function displayDay(){
    var thedate;
    thedate = form[0].value;

   if(thedate){
        if(count === 0){
            count++;
            var div = document.createElement("div");
            div.className = "daystring";
            body[0].appendChild(div);
            if(error) {
                removerror();
                error = false;
            }
        }
        document.getElementsByClassName("daystring")[0].innerHTML = "These events happened on your birthday";
    }
    break;
}
